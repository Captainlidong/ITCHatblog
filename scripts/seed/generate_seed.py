# -*- coding: utf-8 -*-
"""
IT技术交流博客系统 演示数据生成器
生成 50 个用户 + 每人覆盖 11 个分类的博客 + 行为数据（浏览/点赞/收藏/评论）
用法: python generate_seed.py > xm-blog-seed.sql
导入: mysql -uroot -p --default-character-set=utf8mb4 xm-blog < xm-blog-seed.sql
"""
import json
import random
from datetime import date, datetime, timedelta

from articles_part1 import ARTICLES_P1
from articles_part2 import ARTICLES_P2
from articles_part3 import ARTICLES_P3
from articles_part4 import ARTICLES_P4

random.seed(20261011)

ARTICLES = ARTICLES_P1 + ARTICLES_P2 + ARTICLES_P3 + ARTICLES_P4

CAT_ID = {"后端": 1, "前端": 2, "大数据": 4, "代码人生": 5, "算法": 6,
          "人工智能": 7, "开发工具": 8, "职场经验": 9, "面试": 10, "AI": 12, "前沿技术": 13}
CATS = list(CAT_ID.keys())

EXISTING_BLOG_IDS = [1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27]
EXISTING_USER_IDS = [4, 6, 7, 8, 10]
USER_ID_START = 11          # 现有 user 最大 id 为 10
BLOG_ID_START = 28          # 现有 blog 最大 id 为 27

COVERS = ["1704877750495-_b9fa8164-e2a0-452f-ab22-37ba1d8c2063.jpg",
          "1704877760623-_e821b874-7fd7-40c1-9f90-5e57f505d74d.jpg",
          "1704877776472-_e821b874-7fd7-40c1-9f90-5e57f505d74d.jpg",
          "1704877796250-_cfdbb03d-c96a-4ab7-a427-c5296d04f82a.jpg",
          "1703155159848-_cfdbb03d-c96a-4ab7-a427-c5296d04f82a.jpg",
          "1703158855376-_cfdbb03d-c96a-4ab7-a427-c5296d04f82a.jpg",
          "1703008560655-_4bc7861d-2771-4869-9893-24d51ee9b7df.jpg",
          "1703008835922-_c6ef0f94-eb1d-4934-8e65-9a10f0ef8408.jpg",
          "1719374165658-1560025270647L1.jpg",
          "1719374487728-yekongzhongzuiliangdexing.jpg",
          "1719374546559-2324367581169008.jpg",
          "1719374714707-1598961549702zenuo.jpeg",
          "1719375027101-109951162869937004.jpg",
          "1697438073596-avatar.png"]
AVATARS = ["1697438073596-avatar.png", "1703008796327-beautiful.jpg",
           "1704877782100-_c6ef0f94-eb1d-4934-8e65-9a10f0ef8408.jpg",
           "1719374546559-2324367581169008.jpg", "1703159595788-_4bc7861d-2771-4869-9893-24d51ee9b7df.jpg"]

USERS = [
    ("wangzihao", "王子豪", "男", "1998-05-12", "后端开发，主攻 Java 微服务"),
    ("linxuanyu", "林轩宇", "男", "1999-09-23", "前端工程师，Vue 技术栈"),
    ("chenshaoyan", "陈少妍", "女", "2000-02-14", "大数据开发工程师"),
    ("zhoumorui", "周慕睿", "男", "1997-11-08", "算法工程师"),
    ("xulingfei", "徐凌菲", "女", "1999-06-30", "AI 应用开发"),
    ("gaoyaowen", "高耀文", "男", "1996-12-17", "运维开发 / Linux 爱好者"),
    ("hesiyin", "何思吟", "女", "2001-04-25", "产品转开发中，正在学 Python"),
    ("luojianhao", "罗健豪", "男", "1998-08-19", "后端开发，关注高并发"),
    ("tangyuchen", "唐宇辰", "男", "2000-01-06", "计算机专业在读，坚持刷题"),
    ("fanqiaoyun", "范巧云", "女", "1997-03-28", "测试开发工程师"),
    ("dengzilong", "邓子龙", "男", "1996-10-11", "Java 后端 / 消息队列"),
    ("yewenxin", "叶雯心", "女", "1999-12-09", "前端开发，喜欢折腾工程化"),
    ("shenmingxuan", "沈明轩", "男", "1998-02-21", "数据仓库工程师"),
    ("caoyuting", "曹雨婷", "女", "2000-07-16", "UI 转前端"),
    ("panjunhao", "潘俊豪", "男", "1997-09-05", "后端开发，写点博客记录成长"),
    ("duanmuqi", "段沐琪", "女", "1999-05-23", "算法方向研究生"),
    ("fengzhiyuan", "冯致远", "男", "1996-08-30", "架构师之路"),
    ("qiuranran", "邱然然", "女", "2001-01-18", "大三学生，目标后端"),
    ("luwenkang", "卢文康", "男", "1998-11-27", "运维 & 容器化"),
    ("baoxiaoman", "包晓曼", "女", "1997-06-14", "数据分析师"),
    ("niehaoran", "聂浩然", "男", "1999-03-03", "后端开发 / Redis 爱好者"),
    ("xiazhiting", "夏芷婷", "女", "2000-09-26", "前端 & 设计"),
    ("mengxiangbei", "孟向北", "男", "1997-12-02", "转行程序员，自学中"),
    ("jiangyuebin", "蒋悦斌", "男", "1998-04-16", "后端开发，关注分布式"),
    ("wengshihan", "翁诗涵", "女", "1999-08-08", "新媒体运营学前端"),
    ("zhuangyichi", "庄逸驰", "男", "1996-02-19", "性能优化爱好者"),
    ("bailusheng", "白鹭生", "男", "1999-10-31", "研二在读，NLP 方向"),
    ("hanxiaotong", "韩晓彤", "女", "2000-06-21", "测试工程师"),
    ("maozeyuan", "毛致远", "男", "1997-07-07", "后端 / 开源贡献者"),
    ("lanruoxi", "蓝若溪", "女", "1998-10-20", "全栈开发"),
    ("peijunyi", "裴俊逸", "男", "1996-05-09", "数据开发"),
    ("shiqingluan", "石青鸾", "女", "1999-11-15", "前端工程师"),
    ("taomuyang", "陶沐阳", "男", "2000-03-27", "AI 爱好者，动手派"),
    ("weiansong", "魏安松", "男", "1998-01-30", "后端开发"),
    ("konglingxi", "孔令熙", "女", "1997-09-12", "技术写作爱好者"),
    ("yanjiahui", "严佳辉", "男", "1999-02-08", "移动端转后端"),
    ("luoyunxi", "罗云汐", "女", "2000-08-24", "平面设计学前端"),
    ("jimuran", "吉沐然", "男", "1997-06-03", "数据库内核爱好者"),
    ("caiyuting", "蔡雨婷", "女", "1998-12-26", "产品经理"),
    ("fangzeheng", "方泽恒", "男", "1996-04-11", "后端开发 / 算法业余选手"),
    ("qinqianyi", "秦芊一", "女", "2001-07-19", "大四求职中"),
    ("lianxinghe", "梁星河", "男", "1998-06-15", "后端 & DevOps"),
    ("ruanmuyao", "阮沐瑶", "女", "1999-04-02", "前端实习生"),
    ("zhoukaitian", "周开天", "男", "1997-10-28", "微服务架构学习者"),
    ("wenxiaoran", "温晓冉", "女", "2000-12-13", "内容运营 & 写代码"),
    ("gulongcheng", "顾隆城", "男", "1998-09-18", "后端开发"),
    ("huaqianmo", "花千漠", "女", "1997-03-06", "视觉设计 / 会一点前端"),
    ("benshengxu", "贲圣旭", "男", "1999-01-22", "大数据开发"),
    ("yuwanqing", "余婉清", "女", "1998-08-11", "测试 & 自动化"),
    ("kuangjianchi", "匡建驰", "男", "1996-11-04", "老程序员，还在写代码"),
]

COMMENTS = ["写得很清楚，收藏了！", "正好最近在学这块，感谢分享", "总结得很到位，受教了",
            " Mark 一下，回头细看", "楼主是这个方向的大佬吧，条理真清晰", "跟着做了一遍，已经跑通了",
            "有几个点之前一直没想明白，看完豁然开朗", "建议加精，内容很扎实", "代码可以直接用，太贴心了",
            "同感！我也是踩过这个坑才明白的", "感谢整理，省了我好多时间", "写得比官方文档还清楚",
            "这篇必须点赞", "公司项目正好要用，参考价值很大", "图文并茂，好评", "期待续篇！",
            "第一个例子举得好，一下子就懂了", "面试刚好被问到，后悔没早点看到这篇", "已转发给同事，都在夸",
            "细节控狂喜，连坑都标注了", "每天来看一眼新文章已成习惯", "思路清晰，逻辑闭环，学习了",
            "这个系列能不能出一本电子书", "跟着练了两周，感觉入门了", "论点有理有据，不是水货文",
            "终于有人把这块讲明白了", "实用性拉满，先赞后看", "收藏=学会，哈哈", "作为新人看得懂，感谢",
            "文末的总结太精辟了", "已三连，求更多干货", "这篇解决了困扰我一周的问题", "点赞，继续加油",
            "看完马上去试了，效果立竿见影", "笔芯，写得太用心了", "团队例会上分享了这篇，大家反响很好"]

BLOG_START_DATE = date(2025, 3, 1)
BLOG_END_DATE = date(2026, 9, 30)
TODAY = date(2026, 10, 10)
BEHAVIOR_START = datetime(2026, 8, 20)


def esc(s):
    return str(s).replace("'", "''")


def rand_dt(base_days=50):
    dt = datetime(2026, 10, 10, random.randint(8, 23), random.randint(0, 59), random.randint(0, 59)) \
        - timedelta(days=random.randint(0, base_days), hours=random.randint(0, 12))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def strip_html(html):
    import re
    text = re.sub(r"<[^>]+>", "", html)
    return text.replace("&nbsp;", " ").strip()


def main():
    import sys, io
    out = io.StringIO()

    # 分类 -> 文章列表
    by_cat = {c: [a for a in ARTICLES if a["cat"] == c] for c in CATS}

    lines = ["SET NAMES utf8mb4;", ""]

    # ---------- 用户 ----------
    lines.append("-- ========== 50 个演示用户 ==========")
    user_rows = []
    for i, (username, name, sex, birth, info) in enumerate(USERS):
        uid = USER_ID_START + i
        avatar = "http://localhost:9090/files/" + AVATARS[i % len(AVATARS)]
        phone = "1" + random.choice("3589") + "".join(random.choice("0123456789") for _ in range(9))
        email = username + random.choice(["@163.com", "@qq.com", "@126.com"])
        user_rows.append(
            "({},'{}','{}','{}','{}','USER','{}','{}','{}','{}','{}')".format(
                uid, esc(username), esc("123"), esc(name), esc(avatar),
                esc(sex), esc(phone), esc(email), esc(info), esc(birth)))
    lines.append("INSERT INTO `user` (`id`,`username`,`password`,`name`,`avatar`,`role`,`sex`,`phone`,`email`,`info`,`birth`) VALUES")
    lines.append(",\n".join(user_rows) + ";")
    lines.append("")

    # ---------- 博客 ----------
    lines.append("-- ========== 博客（每人每分类一篇）==========")
    new_blog_ids = []          # [(blog_id, user_id, cat)]
    blog_rows = []
    blog_id = BLOG_ID_START
    for u_idx, (username, name, sex, birth, info) in enumerate(USERS):
        uid = USER_ID_START + u_idx
        join_date = BLOG_START_DATE + timedelta(days=random.randint(0, (BLOG_END_DATE - BLOG_START_DATE).days - 220))
        for c_idx, cat in enumerate(CATS):
            pool = by_cat[cat]
            art = pool[(u_idx * 7 + c_idx * 3) % len(pool)]
            blog_ids = join_date + timedelta(days=c_idx * random.randint(14, 22) + random.randint(0, 9))
            if blog_ids > TODAY:
                blog_ids = TODAY - timedelta(days=random.randint(1, 60))
            read_count = int(random.expovariate(1 / 900)) + 25
            descr = strip_html(art["content"])[:88]
            cover = "http://localhost:9090/files/" + COVERS[(blog_id) % len(COVERS)]
            content = art["content"].replace("'", "''")
            blog_rows.append(
                "({},'{}','{}','{}','{}','{}','{}','{}',{},{})".format(
                    blog_id, esc(art["title"]), content, esc(descr), cover,
                    esc(json.dumps(art["tags"], ensure_ascii=False)),
                    uid, esc(blog_ids.strftime("%Y-%m-%d")), read_count, CAT_ID[cat]))
            new_blog_ids.append((blog_id, uid, cat))
            blog_id += 1
    for i in range(0, len(blog_rows), 20):
        chunk = blog_rows[i:i + 20]
        lines.append("INSERT INTO `blog` (`id`,`title`,`content`,`descr`,`cover`,`tags`,`user_id`,`date`,`read_count`,`category_id`) VALUES")
        lines.append(",\n".join(chunk) + ";")
    lines.append("")

    all_blogs = [(bid, uid) for bid, uid, _ in new_blog_ids] + \
                [(bid, None) for bid in EXISTING_BLOG_IDS]
    blog_cat = {(bid, uid): cat for bid, uid, cat in new_blog_ids}
    all_user_ids = [USER_ID_START + i for i in range(len(USERS))] + EXISTING_USER_IDS

    # ---------- 行为数据 ----------
    lines.append("-- ========== 行为数据（浏览/点赞/收藏，带偏好聚类）==========")
    behavior_rows, like_rows, collect_rows = [], [], []
    seen_like, seen_collect = set(), set()
    for u_idx, (username, name, sex, birth, info) in enumerate(USERS):
        uid = USER_ID_START + u_idx
        own = {bid for bid, buid in all_blogs if buid == uid}
        pool = [(bid, buid) for bid, buid in all_blogs if bid not in own]
        pref_cats = random.sample(CATS, 3)
        pref_pool = [b for b in pool if blog_cat.get((b[0], b[1])) in pref_cats] or pool
        browsed = set()
        n_browse = random.randint(15, 25)
        while len(browsed) < n_browse:
            src = pref_pool if (random.random() < 0.7 and pref_pool) else pool
            browsed.add(random.choice(src)[0])
        for bid in browsed:
            behavior_rows.append("({},{},1,1,'{}')".format(uid, bid, rand_dt()))
        like_pool = random.sample(sorted(browsed), min(len(browsed), random.randint(6, 12)))
        for bid in like_pool:
            if (uid, bid) in seen_like:
                continue
            seen_like.add((uid, bid))
            behavior_rows.append("({},{},2,1,'{}')".format(uid, bid, rand_dt()))
            like_rows.append("({},{},'博客')".format(bid, uid))
        collect_pool = [b for b in sorted(browsed) if b not in like_pool] or sorted(browsed)
        for bid in random.sample(collect_pool, min(len(collect_pool), random.randint(2, 6))):
            if (uid, bid) in seen_collect:
                continue
            seen_collect.add((uid, bid))
            behavior_rows.append("({},{},3,1,'{}')".format(uid, bid, rand_dt()))
            collect_rows.append("({},{},'博客')".format(bid, uid))
    for i in range(0, len(behavior_rows), 300):
        lines.append("INSERT INTO `user_behavior` (`user_id`,`blog_id`,`behavior_type`,`weight`,`timestamp`) VALUES")
        lines.append(",\n".join(behavior_rows[i:i + 300]) + ";")
    lines.append("")
    if like_rows:
        for i in range(0, len(like_rows), 300):
            lines.append("INSERT INTO `likes` (`fid`,`user_id`,`module`) VALUES")
            lines.append(",\n".join(like_rows[i:i + 300]) + ";")
    lines.append("")
    if collect_rows:
        for i in range(0, len(collect_rows), 300):
            lines.append("INSERT INTO `collect` (`fid`,`user_id`,`module`) VALUES")
            lines.append(",\n".join(collect_rows[i:i + 300]) + ";")
    lines.append("")

    # ---------- 评论 ----------
    lines.append("-- ========== 评论 ==========")
    comment_rows = []
    for bid, buid in all_blogs:
        if random.random() > 0.4:
            continue
        for _ in range(random.randint(1, 3)):
            commenter = random.choice([u for u in all_user_ids if u != buid])
            ct = rand_dt(40)
            comment_rows.append("('{}',{},{},{},'{}',{},'博客')".format(
                esc(random.choice(COMMENTS)), commenter, "NULL", "NULL", ct, bid))
    for i in range(0, len(comment_rows), 200):
        lines.append("INSERT INTO `comment` (`content`,`user_id`,`pid`,`root_id`,`time`,`fid`,`module`) VALUES")
        lines.append(",\n".join(comment_rows[i:i + 200]) + ";")

    print("-- 生成时间: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), file=sys.stderr)
    print("-- 用户: {} 博客: {} 行为: {} 点赞: {} 收藏: {} 评论: {}".format(
        len(USERS), len(blog_rows), len(behavior_rows), len(like_rows), len(collect_rows), len(comment_rows)),
        file=sys.stderr)

    out.write("\n".join(lines))
    with open("xm-blog-seed.sql", "w", encoding="utf-8") as f:
        f.write(out.getvalue())
    print("已写入 xm-blog-seed.sql", file=sys.stderr)


if __name__ == "__main__":
    main()
