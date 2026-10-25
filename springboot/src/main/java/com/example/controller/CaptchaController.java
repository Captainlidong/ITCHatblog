package com.example.controller;

import cn.hutool.core.lang.Dict;
import com.example.common.Result;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.imageio.ImageIO;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Iterator;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 图形验证码（服务端生成 + 服务端校验）
 * 流程：前端 GET /captcha/generate 拿到 captchaId 和图片 → 提交登录/注册时带上 captchaId + 用户输入
 * → 服务端比对内存中的验证码原文（忽略大小写、一次性使用、2 分钟过期）
 */
@RestController
@RequestMapping("/captcha")
public class CaptchaController {

    /** 验证码有效期（毫秒） */
    private static final long EXPIRE_MS = 2 * 60 * 1000L;
    /** 去掉易混淆字符：0 O 1 I l */
    private static final String CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
    private static final SecureRandom RANDOM = new SecureRandom();

    private static final Map<String, Entry> STORE = new ConcurrentHashMap<>();

    private static class Entry {
        final String code;
        final long time;
        Entry(String code, long time) { this.code = code; this.time = time; }
    }

    @GetMapping("/generate")
    public Result generate() {
        cleanExpired();

        String code = randomCode();
        String id = UUID.randomUUID().toString().replace("-", "");
        STORE.put(id, new Entry(code, System.currentTimeMillis()));

        BufferedImage img = draw(code);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            ImageIO.write(img, "png", baos);
        } catch (Exception e) {
            return Result.error("500", "验证码图片生成失败");
        }
        String image = "data:image/png;base64," + Base64.getEncoder().encodeToString(baos.toByteArray());

        return Result.success(Dict.create()
                .set("captchaId", id)
                .set("captchaImage", image));
    }

    /**
     * 校验并销毁验证码（供登录/注册调用）。任何异常输入都返回 false。
     */
    public static boolean verify(String captchaId, String captchaCode) {
        if (captchaId == null || captchaCode == null || captchaCode.trim().isEmpty()) {
            return false;
        }
        Entry entry = STORE.remove(captchaId.trim());
        return entry != null
                && System.currentTimeMillis() - entry.time <= EXPIRE_MS
                && entry.code.equalsIgnoreCase(captchaCode.trim());
    }

    /** 清理过期验证码，防止内存无限增长 */
    private static void cleanExpired() {
        long now = System.currentTimeMillis();
        Iterator<Map.Entry<String, Entry>> it = STORE.entrySet().iterator();
        while (it.hasNext()) {
            if (now - it.next().getValue().time > EXPIRE_MS) {
                it.remove();
            }
        }
    }

    private static String randomCode() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 4; i++) {
            sb.append(CHARS.charAt(RANDOM.nextInt(CHARS.length())));
        }
        return sb.toString();
    }

    /** AWT 绘制验证码图片：浅紫底 + 干扰线 + 逐字符随机颜色/旋转 */
    private static BufferedImage draw(String code) {
        int w = 130, h = 48;
        BufferedImage img = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        g.setColor(new Color(243, 232, 255));
        g.fillRect(0, 0, w, h);

        Color[] palette = {
                new Color(139, 92, 246), new Color(232, 97, 156),
                new Color(74, 154, 232), new Color(52, 168, 138), new Color(232, 162, 60)
        };

        // 干扰线
        for (int i = 0; i < 8; i++) {
            g.setColor(new Color(200 + RANDOM.nextInt(40), 180 + RANDOM.nextInt(50), 235));
            g.setStroke(new BasicStroke(1.4f));
            g.drawLine(RANDOM.nextInt(w), RANDOM.nextInt(h), RANDOM.nextInt(w), RANDOM.nextInt(h));
        }

        // 验证码字符
        g.setFont(new Font("Arial", Font.BOLD, 30));
        for (int i = 0; i < code.length(); i++) {
            double theta = (RANDOM.nextInt(44) - 22) * Math.PI / 180.0;
            int x = 10 + i * 29, y = 36;
            java.awt.geom.AffineTransform old = g.getTransform();
            g.rotate(theta, x + 10, y - 10);
            g.setColor(palette[RANDOM.nextInt(palette.length)]);
            g.drawString(String.valueOf(code.charAt(i)), x, y);
            g.setTransform(old);
        }

        // 噪点
        for (int i = 0; i < 40; i++) {
            g.setColor(new Color(220 + RANDOM.nextInt(35), 210 + RANDOM.nextInt(45), 245));
            g.fillRect(RANDOM.nextInt(w), RANDOM.nextInt(h), 2, 2);
        }

        g.dispose();
        return img;
    }
}
