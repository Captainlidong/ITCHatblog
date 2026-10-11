# -*- coding: utf-8 -*-
"""种子文章库 第三批：开发工具 10 篇 + 面试 10 篇"""

ARTICLES_P3 = [
# ============ 开发工具 (category_id=8) ============
{"cat": "开发工具", "title": "IDEA 提效技巧合集：这些快捷键我每天都在用", "tags": ["IDEA", "效率工具"],
"content": """<p>IDEA 的上限取决于你对它的了解程度，分享一套我自己用顺手的提效技巧。</p>
<h2>高频快捷键</h2><p>Shift+Shift 全局搜索（找类、找文件、找符号一把梭）；Alt+Enter 万能修复（报错、优化、类型转换都找它）；Ctrl+Alt+L 格式化、Ctrl+Alt+V 提取变量、Ctrl+Alt+M 提取方法——重构三连用熟了代码整洁度会上一个台阶；Shift+F6 全局重命名，连注释一起改。</p>
<h2>神级功能</h2><p>①Live Template：输入 psvm/sout 自动展开，自定义模板把常用代码块配置成缩写；②Postfix Completion：对象后敲 .if / .for / .null 自动包逻辑；③Evaluate Expression：断点暂停时 Alt+F8 任意求值，调试神器；④多光标编辑：Alt+J 逐个选中相同词，批量改比正则快。</p>
<h2>插件推荐</h2><p>KeyPromoter X（用鼠标操作时提醒你对应快捷键，强制养成习惯）、CodeGlance（右侧代码缩略图）、Rainbow Brackets（彩虹括号）、Lombok、MybatisX（mapper 接口和 xml 跳转）。</p>
<p>养成路径：强迫自己两周内遇到重复操作就搜"有没有快捷键"，肌肉记忆养成就回不去了。</p>"""},
{"cat": "开发工具", "title": "Git 进阶：rebase、cherry-pick 与 stash 的正确用法", "tags": ["Git", "版本控制"],
"content": """<p>会 add/commit/push 只是入门，掌握下面几个操作才算真正驾驭 Git。</p>
<h2>rebase：让提交历史变成一条线</h2><p>功能分支拉出后主线有了新提交，在分支上 git rebase main 把自己的提交"搬"到最新主线上，历史比 merge 干净。铁律：**不要对已推送到共享分支的提交做 rebase**，那会让协作者的本地历史错乱。交互式 rebase（git rebase -i）还能合并、拆分、改写历史提交，提 PR 前整理自己的提交序列非常好用。</p>
<h2>cherry-pick：摘一个提交过来</h2><p>hotfix 分支上的某个修复需要同步到多个发布分支，逐个 cherry-pick commit-id，比整分支 merge 精准。</p>
<h2>stash：手头改动先收起来</h2><p>写到一半要切分支修线上问题，git stash 收起、git stash pop 恢复。加 -u 连未跟踪文件一起收。stash 列表支持多次嵌套，记得写备注（git stash save "msg"）。</p>
<h2>救命三招</h2><p>reset --soft 回退提交保留改动；reflog 找回任何"丢失"的提交（reset 硬回退也能救）；revert 生成反向提交安全地撤销已推送的变更。</p>"""},
{"cat": "开发工具", "title": "Postman 进阶：环境变量、脚本与自动化测试", "tags": ["Postman", "接口调试"],
"content": """<p>把 Postman 当"手敲 URL 工具"用太浪费了，它的自动化能力值得每个后端学习。</p>
<h2>环境变量体系</h2><p>建立 dev / test / prod 三套环境，host、token、user-id 都用 {{变量}} 占位。切换环境一键完成，同一套请求打三个环境。token 用脚本自动注入：在登录请求的 Tests（后置脚本）里写 pm.environment.set("token", pm.response.json().data.token)，之后所有请求的 header 引用 {{token}}，永不再手动复制。</p>
<h2>前置与后置脚本</h2><p>Pre-request Script 可以生成时间戳签名、随机测试数据；Tests 里写断言：pm.expect(pm.response.json().code).to.eql("200")，接口返回结构变了立刻报红。</p>
<h2>Collection 与批量执行</h2><p>请求按模块归到 Collection，写好断言的集合用 Runner 一键跑全部接口当回归测试；配合 Newman 命令行能挂到 CI 上。Collection 之间支持 setNextRequest 编排流程（登录→下单→支付→查单）。</p>
<p>建议：新接口调通后顺手把请求和断言存进 Collection，三个月后的回归测试会感谢现在的你。</p>"""},
{"cat": "开发工具", "title": "VSCode 必装插件清单（前端 & 通用）", "tags": ["VSCode", "插件", "效率"],
"content": """<p>VSCode 的一半能力在插件生态，整理我重装系统后必装的一批。</p>
<h2>通用提效</h2><p>Prettier（保存自动格式化，统一风格终结争论）；Code Spell Checker（拼写检查，变量名不再写出 typo）；TODO Highlight / Todo Tree（高亮 TODO 和 FIXME，技术债一目了然）；GitLens（行内显示每行代码的提交人和时间，追溯利器）；Error Lens（错误直接显示在行尾，不用悬停）。</p>
<h2>前端方向</h2><p>Volar（Vue 语言服务，Vue2 项目装 Volar 的 Vue2 专用版或 Vetur）；ESLint + Stylelint；Tailwind CSS IntelliSense（写原子类有自动补全）；Auto Rename Tag（改标签头尾同步）；Path Intellisense（路径补全）。</p>
<h2>通用配置心得</h2><p>settings.json 里开启 formatOnSave 并指定默认 formatter，团队统一用一份配置文件入库；远程开发套件（Remote-SSH + WSL）让笔记本也能连服务器写代码，体验和本地一致。</p>
<p>原则：插件不是越多越好，每个都启动会拖慢性能，装高频用的，剩下的按需加。</p>"""},
{"cat": "开发工具", "title": "Docker 日常高频命令与踩坑备忘", "tags": ["Docker", "运维", "容器"],
"content": """<p>平时用 Docker 高频的就是那十几个命令，加上几个必须记住的坑，整理成备忘。</p>
<h2>高频命令</h2><p>镜像：docker pull / images / rmi；容器：run（-d 后台 -p 端口映射 -v 目录挂载 --name 命名 --restart=always 自启）、ps -a、logs -f（看日志神技）、exec -it xxx bash（进容器排查）、stop/start/rm；系统：system prune 清理无用镜像容器（加 -a 连没在用的镜像一起清，磁盘告急必备）、stats 看容器资源占用。</p>
<h2>必记的坑</h2><p>①容器里 localhost 是容器自己，访问宿主机要 host.docker.internal 或宿主机内网 IP；②容器时区默认 UTC，日志时间差 8 小时，启动加 -v /etc/localtime:/etc/localtime:ro 或环境变量 TZ=Asia/Shanghai；③-v 挂载的数据卷删容器数据还在，但 docker rm -v 会连带删匿名卷，注意；④docker logs 默认无限制增长，生产要配日志驱动或轮转。</p>
<h2>调试技巧</h2><p>容器起不来先 logs 再 inspect 看退出码；进不去容器（没有 bash）就试 sh；想看容器内文件直接 docker cp 拷出来。</p>"""},
{"cat": "开发工具", "title": "Linux 日常开发常用命令备忘清单", "tags": ["Linux", "命令行"],
"content": """<p>做后端免不了跟 Linux 打交道，整理一份我自己最常用的命令清单。</p>
<h2>查问题三板斧</h2><p>①grep：grep -rn "关键字" ./ 递归搜索并显示行号；管道组合 tail -f app.log | grep ERROR 实时过滤；②find：find /path -name "*.log" -mtime +7 找七天前的日志配合 -delete 批量清理；③top / ps -ef | grep java / netstat -tlnp（谁占了端口）、lsof -i:8080。</p>
<h2>文件操作</h2><p>tail -f -n 200 实时看日志；less 大文件浏览（G 跳末尾，/ 搜索）；cp/mv/rm 之外记住 rsync -avz 增量同步比 scp 好用；du -sh * 看目录大小、df -h 看磁盘——磁盘满是最常见的线上事故。</p>
<h2>文本处理</h2><p>awk 取列（awk '{print $1}'）、sed 替换（sed -i 's/old/new/g'）、sort | uniq -c | sort -rn 统计Top N——三件套组合能完成 90% 的日志分析。</p>
<h2>安全习惯</h2><p>rm 前先 ls 确认；生产操作用个人账号 + sudo 而不是 root 裸奔；重要操作前先备份。命令行没有回收站。</p>"""},
{"cat": "开发工具", "title": "用 Markdown 写文档：从排版到画图", "tags": ["Markdown", "写作", "文档"],
"content": """<p>Markdown 是程序员的通用写作语言，掌握进阶技巧后，README、设计文档、技术方案都能写得又快又专业。</p>
<h2>基础之外的排版技巧</h2><p>表格用 | 对齐语法，配合 :---: 控制对齐；任务列表 - [ ] 跟踪进度；折叠块 <details><summary> 放长日志/补充说明，README 不再被刷屏；脚注和引用块让文档更有层次；代码块标注语言才有语法高亮（```java）。</p>
<h2>在 Markdown 里画图</h2><p>Mermaid 是杀手级能力：flowchart 画流程图、sequenceDiagram 画时序图、gantt 画排期，GitHub 和多数文档平台原生渲染。技术方案里的"请求时序图"不用再开画图软件，改文本就能维护。</p>
<h2>工具链</h2><p>Typora（所见即所得，写作最舒服）、VSCode + Markdown Preview Enhanced、图床方案：Typora + PicGo + OSS/GitHub，粘贴截图自动上传转链接，写博客流程丝滑。</p>
<h2>写作建议</h2><p>技术文档四段式：背景 → 方案 → 结论 → 遗留问题；多用列表和代码块，少用大段文字；目录（[TOC]）长文必备。</p>"""},
{"cat": "开发工具", "title": "Maven 依赖冲突排查实录：NoSuchMethodError 剿灭记", "tags": ["Maven", "Java", "踩坑"],
"content": """<p>NoSuchMethodError、ClassNotFoundException 这类运行时报错，十有八九是依赖冲突。记录一次完整的排查过程。</p>
<h2>现象</h2><p>本地跑得好好的，打包到测试环境就抛 NoSuchMethodError，堆栈指向一个 JSON 工具类的方法不存在。</p>
<h2>定位</h2><p>第一步：mvn dependency:tree -Dincludes=要查的groupId > tree.txt 看依赖树，发现同一个工具包被两个依赖分别带入，版本一个是 2.8 一个是 2.12。第二步：mvn help:effective-pom 看最终生效的版本——Maven 的"最短路径优先"原则让 2.8 赢了，而代码用的是 2.12 的新方法。</p>
<h2>解决</h2><p>方案一：dependencyManagement 里显式锁定统一版本（强制所有传递依赖对齐）；方案二：exclude 掉冲突的传递依赖。选择在父 POM 统一 dependencyManagement 锁版本，全工程一次到位。</p>
<h2>预防</h2><p>①引入新依赖前先看它带了什么传递依赖；②CI 里加 mvn dependency:analyze 检查未使用和版本漂移；③版本号统一在父 POM 管理，子模块禁止写版本号。</p>"""},
{"cat": "开发工具", "title": "Windows Terminal + PowerShell 终端美化实录", "tags": ["终端", "Windows", "效率"],
"content": """<p>程序员的终端就是每天盯着最久的地方，花半小时美化，之后每天都是好心情。记录 Windows 下的完整配置。</p>
<h2>基础组合</h2><p>Windows Terminal + PowerShell 7（比自带的 5 快且语法现代化）+ Git Bash（保留，很多工具依赖）。Terminal 里配置多标签页，默认启动项选 PowerShell 7。</p>
<h2>外观</h2><p>Oh My Posh 引擎 + Nerd Font 字体（必须，否则图标全是方块；推荐 CaskaydiaCove NF）。主题我用的是半透明亚克力 + One Half Dark 配色，背景透明度 85% 效果最佳。profile 里配 startingDirectory 记住常用目录。</p>
<h2>效率配置</h2><p>PowerShell 装 PSReadLine（语法高亮 + 历史命令预测，输入时会灰字提示历史命令，Tab 补全），设 predictionStyle 为 HistoryAndPlugin；常用别名写进 $PROFILE（ll、gs、gp 这些）。管理员权限直接在 Terminal 里配好，省去右键。</p>
<h2>配色原则</h2><p>对比度优先，别为了好看牺牲可读性；深浅色主题各配一套，白天浅色晚上深色对眼睛友好。</p>"""},
{"cat": "开发工具", "title": "Navicat 数据库管理与设计实用技巧", "tags": ["Navicat", "数据库", "工具"],
"content": """<p>Navicat 是最常用的数据库 GUI，但大多数人只用它写查询，下面这些功能值得用起来。</p>
<h2>结构与数据</h2><p>①设计表：图形化改字段、加索引，还能导出变更 SQL 给 DBA 审查；②数据传输：库到库整表复制，跨环境搬数据神器（生产脱敏数据拉到测试环境）；③ER 图：自动生成表关系图，接手陌生库先看这个，表关系一目了然。</p>
<h2>查询效率</h2><p>查询编辑器支持多语句执行和结果多标签；选中一段 SQL 单独跑（F8 或执行选中），调优长脚本时分段验证；查询结果网格直接双击改数据（内部走 update），改测试数据方便但要小心；语句模板和自动补全记得开。</p>
<h2>安全与效率</h2><p>①连接密码导出备份要加密，换电脑迁移用 Navicat 自带的导出连接（设主密码）；②颜色分组标记环境：生产标红色、测试绿色，防止误操作；③定时备份任务配起来，本地开发库也有价值；④导出向导支持 Excel/CSV/JSON，给业务方导数据不用写代码。</p>
<p>替代方案提醒：DBeaver 免费、DataGrip 更强，团队用什么跟着用什么，习惯迁移成本低。</p>"""},

# ============ 面试 (category_id=10) ============
{"cat": "面试", "title": "Java 基础高频面试题：这些细节决定第一印象", "tags": ["Java", "面试", "八股"],
"content": """<p>Java 基础是面试的"必考第一题"，答得扎实整个面试的基调就稳了。整理最高频的几个考点。</p>
<h2>== 与 equals 与 hashCode</h2><p>== 比引用（基本类型比值），equals 默认也是比引用，重写 equals 必须重写 hashCode——否则 HashMap 里同对象不同桶，查找直接失效。String 重写了 equals 和 hashCode，且由于字符串常量池，字面量比较 == 也常为 true，这是经典陷阱。</p>
<h2>String 为什么设计成不可变</h2><p>①常量池复用的前提；②线程安全；③hashCode 可缓存（String 的 hash 有缓存字段）；④安全性（路径、类名、网络参数不可被篡改）。</p>
<h2>final / finally / finalize</h2><p>final 修饰类方法变量（不可继承/重写/重新赋值）；finally 保证释放资源（try-with-resources 更优雅）；finalize 已废弃，资源清理用 AutoCloseable。</p>
<h2>面向对象三特性举例</h2><p>别背定义，用例子讲：封装（POJO 收敛字段和校验）、继承（模板方法里子类只实现差异步骤）、多态（策略模式里同一接口不同实现运行时切换）。</p>
<p>基础题的核心答题策略：先一句话给结论，再补一个使用场景或源码细节，比长篇背诵加分。</p>"""},
{"cat": "面试", "title": "HashMap 面试全景：结构、扩容与线程安全", "tags": ["HashMap", "集合", "面试"],
"content": """<p>HashMap 是 Java 集合面试的绝对 C 位，围绕它的问题可以连出一条完整链路。</p>
<h2>底层结构</h2><p>JDK8 里是 数组 + 链表 + 红黑树：哈希冲突挂链表，链表长度超过 8 且数组容量 ≥ 64 时转红黑树，查询从 O(n) 优化到 O(log n)。为什么阈值是 8？泊松分布下哈希均匀时链表到 8 的概率极低，树化是兜底而非常态。</p>
<h2>容量与扩容</h2><p>默认容量 16，负载因子 0.75，超过 容量×0.75 扩容到两倍。JDK8 的高明之处：扩容时元素新位置要么在原下标、要么原下标+旧容量（高位多了一个 bit），不需要重新计算 hash。为什么容量必须是 2 的幂？为了让 (n-1) & hash 等价于取模且分布均匀。</p>
<h2>put 流程</h2><p>计算 hash（高 16 位异或低 16 位，让高位也参与运算）→ 定位桶 → 空则直放 → 是树节点走红黑树插入 → 链表尾插（JDK7 是头插，并发扩容会成环）→ 超阈值树化 → 最后判断扩容。</p>
<h2>线程安全</h2><p>HashMap 并发下数据覆盖、size 不准。替代：Collections.synchronizedMap 粗粒度锁，或 ConcurrentHashMap（JDK8 CAS + synchronized 锁单个桶）。为什么 key 允许 null？因为 hash 对 null 特判放 0 号桶。</p>"""},
{"cat": "面试", "title": "JVM 面试：内存区域、GC 流程与常见收集器", "tags": ["JVM", "GC", "面试"],
"content": """<p>JVM 三连问（内存区域、GC 怎么工作、怎么调优）几乎每场后端面试都会出现。</p>
<h2>运行时数据区</h2><p>线程私有：程序计数器、虚拟机栈（局部变量表，StackOverflowError 的来源）、本地方法栈；线程共享：堆（对象实例，GC 主战场）、方法区（JDK8 后是元空间，存类信息，用的本地内存）。字符串常量池在 JDK7 后移到了堆里。</p>
<h2>分代回收流程</h2><p>新对象进 Eden，Eden 满触发 Minor GC：存活对象进 Survivor（From/To 交替，年龄+1），默认 15 岁晋升老年代；大对象直接进老年代；老年代空间不足触发 Major GC / Full GC（伴随 STW，也是调优的主目标）。</p>
<h2>常见收集器演进</h2><p>Parallel（吞吐优先，批量任务）→ CMS（低停顿但有碎片，已废弃）→ G1（区域化分代，可预测停顿，JDK9+ 默认）→ ZGC/Shenandoah（着色指针、并发整理，停顿亚毫秒级）。回答时说清楚"你的场景用什么、为什么"比背名字加分。</p>
<h2>排查工具</h2><p>jps 定位进程 → jmap dump 堆快照 → MAT/jvisualvm 分析大对象；线上 OOM 记得加 -XX:+HeapDumpOnOutOfMemoryError 参数自动留现场。</p>"""},
{"cat": "面试", "title": "并发面试：synchronized、volatile 与线程安全的边界", "tags": ["并发", "Java", "面试"],
"content": """<p>并发题的区分度高，答好三件套（可见性、原子性、有序性）是入场券。</p>
<h2>volatile：可见性 + 有序性，没有原子性</h2><p>写 volatile 变量会刷新到主存并使其他 CPU 缓存失效（可见性），同时通过内存屏障禁止指令重排（有序性）。但 i++ 这类"读-改-写"三步操作它管不住。典型用法：状态标志位（停止线程的 flag）、双重检查锁单例里防止对象半初始化逸出。</p>
<h2>synchronized：三态锁</h2><p>基于对象监视器实现，JDK6 优化后有锁升级路径：无锁 → 偏向锁（只有一个线程访问）→ 轻量级锁（交替访问，CAS 自旋）→ 重量级锁（竞争激烈，走操作系统互斥量）。JDK15 后偏向锁默认废弃，因为维护成本高于收益。修饰静态方法是锁 Class 对象，修饰实例是锁当前对象，别混用造成"看起来锁了其实没互斥"。</p>
<h2>AQS 一句话</h2><p>ReentrantLock、Semaphore、CountDownLatch 的底座：一个 volatile int state + CLH 双向队列 + 模板方法，公平/非公平的区别是获取锁前要不要先排队。</p>
<h2>答题加分项</h2><p>主动提"无锁化"：CAS（注意 ABA 问题与版本号）、ThreadLocal（内存泄漏要 remove）、不可变对象。能说出"先考虑不共享，再考虑不可变，最后才是锁"的优先级，面试官眼睛会亮。</p>"""},
{"cat": "面试", "title": "MySQL 面试：事务、锁与 MVCC 讲清楚", "tags": ["MySQL", "面试", "事务"],
"content": """<p>MySQL 面试的高频深水区在事务隔离级别和 MVCC，背概念没用，要能推演。</p>
<h2>四个隔离级别对应的问题</h2><p>读未提交（脏读）→ 读已提交（RC，解决脏读，剩不可重复读）→ 可重复读（RR，MySQL 默认，剩幻读）→ 串行化（全解决但并发差）。重点：MySQL 的 RR 在很大程度上通过间隙锁解决了幻读——当前读走临键锁，快照读走 MVCC。</p>
<h2>MVCC 的推演</h2><p>每行记录有隐藏的 trx_id（最后修改事务）和 roll_pointer（指向 undo log 版本链）。读时生成 ReadView，包含活跃事务列表，按可见性规则沿版本链找能看到的那一版。RC 每次查询生成新 ReadView（所以能读到别人已提交的新数据），RR 复用第一次的 ReadView（所以整个事务看到的都是开头那个快照）——这就是两个级别行为差异的全部原因。</p>
<h2>锁的分层</h2><p>全局锁（备份）、表级锁（MDL 元数据锁、意向锁）、行级锁（记录锁、间隙锁 Gap、临键锁 Next-Key）。高频追问："select ... for update" 是当前读加临键锁，"select" 普通读是快照读不加锁。</p>
<h2>加分点</h2><p>主动提 binlog 两阶段提交（redo log prepare → binlog → commit）保证主从一致，面试官大概率会顺势追问。</p>"""},
{"cat": "面试", "title": "Redis 面试：持久化、过期删除与内存淘汰", "tags": ["Redis", "面试", "缓存"],
"content": """<p>Redis 面试除了缓存三问，持久化和内存管理是第二梯队的高频区。</p>
<h2>持久化：RDB vs AOF</h2><p>RDB：定时 fork 子进程把内存快照写成二进制文件，恢复快、文件小，但两次快照间的数据会丢；AOF：追加写每条命令，appendfsync everysec 是性能与安全的平衡点（最多丢 1 秒），文件大恢复慢。4.0 之后混合持久化（AOF 重写时前半段 RDB 格式 + 增量 AOF）兼得两者，生产推荐。fork 时的写时复制（COW）是追问重灾区：大内存实例 fork 会卡顿，所以单实例内存别太大（建议 10G 内）。</p>
<h2>过期删除：惰性 + 定期</h2><p>惰性删除：访问 key 时检查过期才删，省 CPU 但冷数据占内存；定期删除：每 100ms 随机抽一批带过期时间的 key 删，平衡两者。</p>
<h2>内存淘汰：八种策略</h2><p>内存满后按策略驱逐：noeviction（默认，写报错）、lru（近似 LRU，采样淘汰）、lfu（访问频率，4.0+）、random、ttl。缓存场景推荐 allkeys-lru 或 allkeys-lfu，别用默认的 noeviction 让写入直接失败。</p>
<h2>高频追问链</h2><p>主从复制流程（全量 RDB + 增量积压缓冲区）→ 哨兵选主 → 集群分片（16384 槽位，CRC16 按 key 定槽）。把这条链路串起来，Redis 面试基本通关。</p>"""},
{"cat": "面试", "title": "Spring 面试：IOC、AOP 与循环依赖", "tags": ["Spring", "面试", "原理"],
"content": """<p>Spring 三问（IOC 是什么、AOP 怎么实现、循环依赖怎么解决）的答案都指向同一个内核：三级缓存与动态代理。</p>
<h2>IOC：控制反转的本质</h2><p>不是"new 不用自己写"，而是对象的组装权交给容器：依赖注入（构造器/Setter/字段）+ 生命周期管理。加分点：说到"依赖注入优先用构造器注入"——不可变、依赖必填、不会在字段注入时破坏封装，Spring 官方也推荐。</p>
<h2>AOP：动态代理的选择</h2><p>有接口默认 JDK 动态代理（实现 InvocationHandler，基于接口），无接口用 CGLIB（生成子类，final 方法代理不了）。事务、日志、权限这些横切逻辑通过切面织入。高频追问：代理对象内部 this 调用不走切面——这和事务失效是同一个根源。</p>
<h2>循环依赖：三级缓存</h2><p>A 依赖 B、B 又依赖 A。Spring 用三级缓存解决：一级缓存放成品 Bean，二级缓存放提前暴露的半成品，三级缓存放 ObjectFactory（生成早期引用，需要时才创建代理）。流程：A 实例化后先把工厂放三级缓存 → 注入 B 时触发 B 创建 → B 注入 A 时从三级缓存拿到 A 的早期引用 → B 完成 → A 继续。注意：**构造器注入的循环依赖无解**（都还没实例化完成），Spring Boot 2.6+ 默认禁止循环依赖，逼着从设计上消除它。</p>
<p>答题策略：这三问互相咬合，主动把"代理"作为主线串起来讲，层次感立刻出来。</p>"""},
{"cat": "面试", "title": "分布式面试：CAP 与 BASE 理论怎么落地到方案", "tags": ["分布式", "架构", "面试"],
"content": """<p>CAP 被问烂了，但多数人只会背定义。面试官真正想听的是：你能不能用它们解释具体技术选型。</p>
<h2>CAP 的正确理解</h2><p>一致性（所有节点同一时刻看到相同数据）、可用性（每个请求都有响应）、分区容错（网络分区时系统仍工作）。分布式系统分区是必然存在的，所以 P 是前提，真正的选择在 C 和 A 之间——**分区发生时，要么拒绝请求保一致，要么继续服务保可用**。</p>
<h2>用 CAP 解释常见组件</h2><p>ZooKeeper：选主期间不可用，CP；Eureka：每个节点都能独立服务，AP；Redis 主从：异步复制可能丢数据，偏 AP；etcd（Raft 多数派写入）：CP。回答模板："这个组件在网络分区时选择拒绝服务还是返回旧数据"，一句话定位它的取舍。</p>
<h2>BASE：CAP 的工程化妥协</h2><p>基本可用（降级、限流、削峰）、软状态（中间状态允许存在，如支付中）、最终一致（消息队列、重试对账）。现实中几乎所有的"最终一致"方案都是 BASE 思想。</p>
<h2>实战话题衔接</h2><p>分布式事务：强一致用 TCC/2PC（代价高），最终一致用本地消息表 + MQ + 对账补偿（性价比高）；分布式锁：Redis（AP，极端情况锁丢失）vs ZooKeeper（CP，性能低）。选型话术："看业务对不一致的容忍窗口，能容忍就最终一致。"</p>"""},
{"cat": "面试", "title": "算法面 40 分钟：如何稳定发挥做出一道题", "tags": ["面试", "算法", "方法论"],
"content": """<p>算法面考的不只是做题，是模拟协作：你能不能结构化地解决问题。40 分钟的标准节奏分享给大家。</p>
<h2>前 5 分钟：确认理解</h2><p>复述题目，主动问清边界：数组有多长？有没有重复？数据范围（决定能不能用哈希/排序）？输入为空怎么办？很多挂掉的人不是不会做，是理解就偏了。</p>
<h2>5-15 分钟：先讲思路再动笔</h2><p>先给暴力解并报复杂度（这本身是得分点），再往优化方向推："暴力是 O(n²)，瓶颈在重复查找，我可以用哈希把查找降到 O(1)。"面试官点头后再写代码——**没确认思路就闷头写是大忌**。</p>
<h2>15-30 分钟：写代码</h2><p>边写边讲（暴露思路过程，卡住时面试官会提示）；变量命名别用 a b c；写完主动走一遍测试用例：正常 case、边界（空输入、单元素、极值）各过一遍，当场自己抓 bug 比面试官指出来强十倍。</p>
<h2>最后 5 分钟：报复杂度与收尾</h2><p>时间/空间复杂度主动说，能优化就提一嘴 trade-off（"哈希牺牲空间换时间"）。</p>
<p>心态提示：卡住很正常，把卡住的点说出来（"我在考虑去重的时候卡住了，想用双指针试试"），沟通本身就是考察项。</p>"""},
{"cat": "面试", "title": "HR 面与谈薪：别在最后一关翻车", "tags": ["面试", "谈薪", "软技能"],
"content": """<p>技术面全过，HR 面和谈薪才是拿 offer 的最后一公里，翻车的人不在少数。</p>
<h2>HR 面在考察什么</h2><p>稳定性（为什么离职、通勤时长、职业规划）、文化匹配（协作方式、抗压表达）、以及"你说的和技术面反馈是否一致"。回答离职原因的口径：永远向前看（追求更大平台/业务方向），不吐槽前司；职业规划给"专业深度 + 团队贡献"两条线，别聊"三年当架构师"这种空话。</p>
<h2>谈薪的基本功</h2><p>①先摸市场行情（招聘网站同岗位区间 + 朋友内推打听），心里有锚点；②报期望值报区间上沿（报 20-25k，最后大概率落在 22 上下），并说明依据（当前薪资 + 涨幅逻辑或能力匹配度）；③问清薪资结构：月薪 × 月数、年终奖规则、调薪窗口、社保公积金基数、股票期权折现——打包总包比较才公平；④手里有其他 offer 如实说，是筹码不是威胁。</p>
<h2>反问环节问什么</h2><p>问业务（这个岗位负责什么、团队现状）、问成长（code review 文化、技术分享氛围）、问考核（试用期标准）。别问"加不加班"（答案你懂的），换种问法："团队目前的工作节奏大概是什么样？"</p>
<p>最后：所有口头承诺都写进 offer 里才算数，签字前逐条确认。</p>"""},
]
