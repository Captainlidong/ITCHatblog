package com.example.service;

import cn.hutool.core.util.StrUtil;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 登录/注册频率限制（内存实现，防自动化脚本批量注册与密码暴力破解）
 * - 注册：同一 IP 每小时最多 3 次（无论成功失败，都消耗配额）
 * - 登录：同一 IP 15 分钟内失败 5 次（验证码错误不计，账号密码错误才计）→ 封禁 15 分钟；成功登录即清零
 * 纯内存实现，重启即清零；数据量大时可换 Redis
 */
@Component
public class RateLimitService {

    private static final int REGISTER_MAX_PER_HOUR = 3;
    private static final long REGISTER_WINDOW_MS = 60 * 60 * 1000L;
    private static final int LOGIN_MAX_FAILS = 5;
    private static final long LOGIN_WINDOW_MS = 15 * 60 * 1000L;
    private static final long LOGIN_BLOCK_MS = 15 * 60 * 1000L;

    /** ip -> 最近一小时的注册时间戳 */
    private static final Map<String, List<Long>> REGISTER_LOG = new ConcurrentHashMap<>();
    /** ip -> 登录失败状态 */
    private static final Map<String, LoginFailState> LOGIN_FAIL = new ConcurrentHashMap<>();

    private static class LoginFailState {
        int count;
        long windowStart;
        long blockedUntil;
    }

    /** 取客户端真实IP（优先 X-Forwarded-For，兼容反向代理） */
    public static String clientIp(HttpServletRequest request) {
        String xff = request.getHeader("X-Forwarded-For");
        if (StrUtil.isNotBlank(xff)) {
            return xff.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }

    /**
     * 注册频率检查：同一 IP 每小时超过上限时返回拒绝提示语，否则记录本次尝试并返回 null（放行）
     */
    public String checkRegister(String ip) {
        long now = System.currentTimeMillis();
        List<Long> list = REGISTER_LOG.computeIfAbsent(ip, k -> new ArrayList<>());
        synchronized (list) {
            list.removeIf(t -> now - t > REGISTER_WINDOW_MS);
            if (list.size() >= REGISTER_MAX_PER_HOUR) {
                return "注册过于频繁，请稍后再试";
            }
            list.add(now);
        }
        return null;
    }

    /** 登录是否已被封禁（失败次数过多） */
    public boolean isLoginBlocked(String ip) {
        LoginFailState s = LOGIN_FAIL.get(ip);
        return s != null && s.blockedUntil > System.currentTimeMillis();
    }

    /** 记录一次登录失败（账号密码错误才计，验证码错误不计）；窗口内累计到上限自动封禁 */
    public void recordLoginFailure(String ip) {
        long now = System.currentTimeMillis();
        LoginFailState s = LOGIN_FAIL.computeIfAbsent(ip, k -> new LoginFailState());
        synchronized (s) {
            if (now - s.windowStart > LOGIN_WINDOW_MS) {
                s.count = 0;
                s.windowStart = now;
            }
            s.count++;
            if (s.count >= LOGIN_MAX_FAILS) {
                s.blockedUntil = now + LOGIN_BLOCK_MS;
                s.count = 0;
            }
        }
    }

    /** 登录成功后清零失败计数 */
    public void resetLoginFailures(String ip) {
        LOGIN_FAIL.remove(ip);
    }
}
