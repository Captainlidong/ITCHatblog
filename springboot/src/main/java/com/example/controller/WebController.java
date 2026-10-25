package com.example.controller;

import cn.hutool.core.util.ObjectUtil;
import cn.hutool.core.util.StrUtil;
import cn.hutool.json.JSONUtil;
import com.example.common.Result;
import com.example.common.enums.ResultCodeEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.Account;
import com.example.exception.CustomException;
import com.example.service.AdminService;
import com.example.service.RateLimitService;
import com.example.service.UserService;
import org.springframework.core.io.ClassPathResource;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * 基础前端接口
 */
@RestController
public class WebController {

    @Resource
    private AdminService adminService;

    @Resource
    private UserService userService;

    @Resource
    private RateLimitService rateLimitService;

    /**
     * 前端打包产物嵌入后端（classpath:/static/index.html 存在）时，根路径转发到前端首页；纯后端模式保持原样返回 JSON
     */
    @GetMapping("/")
    public void hello(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        if (new ClassPathResource("static/index.html").exists()) {
            request.getRequestDispatcher("/index.html").forward(request, response);
            return;
        }
        response.setContentType("application/json;charset=utf-8");
        response.getWriter().write(JSONUtil.toJsonStr(Result.success("访问成功")));
    }

    /**
     * 登录/注册页路由（GET）：前端嵌入后端时转发到前端页面，
     * 否则浏览器直接访问 /login、/register 会因只存在 POST 接口映射而返回 405
     */
    @GetMapping("/login")
    public void loginPage(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        if (new ClassPathResource("static/index.html").exists()) {
            request.getRequestDispatcher("/index.html").forward(request, response);
            return;
        }
        response.setContentType("application/json;charset=utf-8");
        response.getWriter().write(JSONUtil.toJsonStr(Result.success("login")));
    }

    @GetMapping("/register")
    public void registerPage(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        if (new ClassPathResource("static/index.html").exists()) {
            request.getRequestDispatcher("/index.html").forward(request, response);
            return;
        }
        response.setContentType("application/json;charset=utf-8");
        response.getWriter().write(JSONUtil.toJsonStr(Result.success("register")));
    }

    /**
     * 登录（服务端验证码 + 同IP失败次数限制）
     */
    @PostMapping("/login")
    public Result login(@RequestBody Account account, HttpServletRequest request) {
        String ip = RateLimitService.clientIp(request);
        if (rateLimitService.isLoginBlocked(ip)) {
            return Result.error("429", "登录失败次数过多，请15分钟后再试");
        }
        if (ObjectUtil.isEmpty(account.getUsername()) || ObjectUtil.isEmpty(account.getPassword())
                || ObjectUtil.isEmpty(account.getRole())) {
            return Result.error(ResultCodeEnum.PARAM_LOST_ERROR);
        }
        if (!CaptchaController.verify(account.getCaptchaId(), account.getCaptchaCode())) {
            return Result.error("400", "验证码错误或已过期");
        }
        try {
            if (RoleEnum.ADMIN.name().equals(account.getRole())) {
                account = adminService.login(account);
            }else if (RoleEnum.USER.name().equals(account.getRole())) {
                account =userService.login(account);
            }else {
                return Result.error(ResultCodeEnum.PARAM_ERROR);
            }
        } catch (CustomException e) {
            // 账号或密码错误才计入失败次数（验证码错误不计）
            rateLimitService.recordLoginFailure(ip);
            throw e;
        }
        rateLimitService.resetLoginFailures(ip);
        return Result.success(account);
    }

    /**
     * 用户注册（服务端验证码 + 同IP频率限制）
     */
    @PostMapping("/register")
    public Result register(@RequestBody Account account, HttpServletRequest request) {
        String ip = RateLimitService.clientIp(request);
        String deny = rateLimitService.checkRegister(ip);
        if (deny != null) {
            return Result.error("429", deny);
        }
        if (StrUtil.isBlank(account.getUsername()) || StrUtil.isBlank(account.getPassword())
                || ObjectUtil.isEmpty(account.getRole())) {
            return Result.error(ResultCodeEnum.PARAM_LOST_ERROR);
        }
        if (!CaptchaController.verify(account.getCaptchaId(), account.getCaptchaCode())) {
            return Result.error("400", "验证码错误或已过期");
        }
        if (RoleEnum.USER.name().equals(account.getRole())) {
            userService.register(account);
        }else {  //只允许用户注册
            return Result.error(ResultCodeEnum.PARAM_ERROR);
        }
        return Result.success();
    }

    /**
     * 修改密码
     */
    @PutMapping("/updatePassword")
    public Result updatePassword(@RequestBody Account account) {
        if (StrUtil.isBlank(account.getUsername()) || StrUtil.isBlank(account.getPassword())
                || ObjectUtil.isEmpty(account.getNewPassword())) {
            return Result.error(ResultCodeEnum.PARAM_LOST_ERROR);
        }
        if (RoleEnum.ADMIN.name().equals(account.getRole())) {
            adminService.updatePassword(account);
        }else if(RoleEnum.USER.name().equals(account.getRole())) {
            userService.updatePassword(account);
        }
        return Result.success();
    }

}
