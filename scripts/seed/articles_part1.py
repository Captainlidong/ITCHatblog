# -*- coding: utf-8 -*-
"""种子文章库 第一批：后端 12 篇 + 前端 12 篇"""

ARTICLES_P1 = [
# ============ 后端 (category_id=1) ============
{"cat": "后端", "title": "Spring 声明式事务失效的 6 个常见场景", "tags": ["Java", "Spring", "事务"],
"content": """<p>项目里用 @Transactional 看似省心，但踩过坑的人都知道它有一堆"失效姿势"。这篇总结我在真实项目里遇到过的 6 种。</p>
<h2>1. 同类内部方法调用</h2><p>this 调用不走代理对象，AOP 事务自然不生效。解决办法：拆到另一个 Bean，或通过 AopContext.currentProxy() 拿代理再调。</p>
<h2>2. 方法不是 public</h2><p>Spring 事务基于 AOP，默认只对 public 方法生效，protected、private 上加注解是无效的。</p>
<h2>3. 异常被 catch 吃掉了</h2><p>事务回滚依赖异常抛出到代理层。方法内部 try-catch 后没有重新抛出，事务会认为一切正常并提交。</p>
<h2>4. 默认只回滚 RuntimeException</h2><p>抛受检异常（如 IOException）默认不回滚，需要显式声明 @Transactional(rollbackFor = Exception.class)。我个人的习惯是无脑加上这个参数。</p>
<h2>5. 传播行为用错</h2><p>REQUIRES_NEW 挂起外层事务开新事务，NESTED 用保存点。如果想"内层回滚不影响外层"，用错传播行为会两头翻车。</p>
<h2>6. 数据库引擎不支持</h2><p>MySQL 的 MyISAM 引擎不支持事务，InnoDB 才支持。老项目迁移时特别容易踩。</p>
<p>结语：事务失效排查的核心思路是"确认调用链上有没有代理对象"，大部分问题都是它引起的。</p>"""},
{"cat": "后端", "title": "MySQL 索引失效的常见原因与排查思路", "tags": ["MySQL", "SQL优化"],
"content": """<p>明明建了索引却走全表扫描？用 EXPLAIN 看执行计划之前，先检查下面这些常见原因。</p>
<h2>1. 违反最左前缀原则</h2><p>联合索引 (a, b, c) 只有从 a 开始连续命中才能使用。查询条件只有 b 或 c，索引用不上。</p>
<h2>2. 对索引列做函数或运算</h2><p>where date(create_time) = '2026-10-01' 会让索引失效，应改写成范围查询：create_time >= '2026-10-01' and create_time < '2026-10-02'。</p>
<h2>3. 隐式类型转换</h2><p>手机号字段是 varchar，却用 where phone = 13800001234 数字去比，MySQL 会把列转成数值再比，索引失效。字符串条件记得加引号。</p>
<h2>4. 前导模糊查询</h2><p>like '%关键字' 无法使用 B+ 树索引；like '关键字%' 可以。全文检索需求考虑 ES。</p>
<h2>5. or 连接了无索引列</h2><p>or 两侧只要有一边没有可用索引，通常会退化为全表扫描。</p>
<h2>6. 优化器自己放弃了</h2><p>回表代价高于全表扫描时（比如查询命中大部分行），优化器会主动放弃索引，这不是 bug。</p>
<p>排查口诀：先 EXPLAIN，再看 type 和 key 列，最后回头核对 SQL 写法。</p>"""},
{"cat": "后端", "title": "Redis 缓存穿透、击穿、雪崩一次讲清", "tags": ["Redis", "缓存", "高并发"],
"content": """<p>这三个词面试必问，生产事故里也最常见，用一组对比把它们理清楚。</p>
<h2>穿透：查不存在的数据</h2><p>请求打到数据库里根本不存在的数据，缓存永远不命中，恶意请求会打垮 DB。对策：①对空结果也做短过期缓存；②布隆过滤器在缓存前拦截；③接口层做参数合法性校验。</p>
<h2>击穿：热点 key 过期瞬间</h2><p>某个热点 key 过期的瞬间，大量并发直接压到数据库。对策：①互斥锁，只放一个请求去回源重建缓存；②热点数据逻辑过期，物理不过期；③提前异步续期。</p>
<h2>雪崩：大批 key 同时失效</h2><p>同一批缓存设置了相同过期时间，到期集体失效。对策：①过期时间加随机抖动；②多级缓存（本地 caffeine + Redis）；③缓存集群高可用，限流降级兜底。</p>
<h2>一句话记忆</h2><p>穿透查的是"不存在的"，击穿是"一个热点"，雪崩是"一大片"。对策分别对应：拦、锁、散。</p>"""},
{"cat": "后端", "title": "JWT 登录认证的原理与项目实践", "tags": ["JWT", "认证", "Java"],
"content": """<p>前后端分离项目里 JWT 几乎是标配，这里结合我自己项目里的用法讲讲原理和取舍。</p>
<h2>结构：三段式</h2><p>JWT 由 Header（算法声明）、Payload（claims，如 userId、过期时间）、Signature（对前两段用密钥签名）组成，用 . 分隔。签名保证了 token 不可篡改——改了 payload 验签就过不了。</p>
<h2>项目里的实践</h2><p>①登录成功后签发 token，audience 里放 userId-role，过期时间 2 小时；②网关或拦截器统一验签，从 payload 拿身份；③密码参与签名密钥（HMAC256），改密后旧 token 全部失效。</p>
<h2>优缺点</h2><p>优点：无状态、水平扩展友好、跨服务共享方便。缺点：签发后无法主动撤销（除非引入黑名单）、payload 明文可见不能放敏感信息、续期需要 refresh token 机制。</p>
<p>我的建议：单体或小规模微服务直接用 JWT 足够；对强制下线有强需求时，加一层 Redis 黑名单即可。</p>"""},
{"cat": "后端", "title": "接口幂等性设计的 4 种常用方案", "tags": ["分布式", "系统设计"],
"content": """<p>用户重复点击、网络重试、MQ 重复投递，都会让同一个请求到达多次。写操作不做幂等，轻则重复下单，重则资金损失。</p>
<h2>1. 数据库唯一索引</h2><p>用业务唯一键（订单号）建唯一索引，重复插入直接报错兜底。最简单可靠，几乎所有方案的最后防线。</p>
<h2>2. 防重 token 机制</h2><p>进页面先领一个一次性 token 存 Redis，提交时带着 token，服务端用 Redis 的原子删除（DEL 返回 1 才处理）判重。适合表单提交场景。</p>
<h2>3. 分布式锁</h2><p>以业务键为锁粒度，拿到锁的请求先查后做。注意锁要设过期时间，释放要用 Lua 保证原子性。</p>
<h2>4. 状态机</h2><p>订单状态流转用条件更新：update order set status=2 where id=1 and status=1，影响行数为 0 说明已处理过。天然幂等，推荐优先考虑。</p>
<p>实践建议：入口做防重，数据库唯一索引兜底，中间用状态机约束流转，三层配合最稳。</p>"""},
{"cat": "后端", "title": "线程池核心参数到底该怎么设", "tags": ["Java", "并发", "线程池"],
"content": """<p>Executors 的那几个工厂方法在生产环境基本禁用，ThreadPoolExecutor 七个参数才是正经出路。核心参数怎么定，说下我的经验。</p>
<h2>核心线程数</h2><p>CPU 密集型任务取 N+1，IO 密集型取 2N 左右做起点，但别背公式背到底——真实值靠压测调出来。任务耗时里 IO 等待占比越高，线程数越可以往上加。</p>
<h2>队列与拒绝策略</h2><p>有界队列是必须的，无界队列会把内存打爆还会让拒绝策略形同虚设。队列大小结合可接受的延迟倒推：队列长度 ≈ 目标吞吐 × 可容忍等待时间。拒绝策略里 CallerRunsPolicy 能起到天然的限流反压作用，很多场景比直接抛异常友好。</p>
<h2>实践建议</h2><p>①不同业务隔离使用不同线程池，避免相互拖累；②给线程池起名（ThreadFactory），日志排查不抓瞎；③监控活跃线程数和队列深度，接近水位提前扩容。参数是调出来的，不是算出来的。</p>"""},
{"cat": "后端", "title": "分布式 ID 生成方案对比：从 UUID 到雪花算法", "tags": ["架构", "分布式"],
"content": """<p>分库分表之后，数据库自增主键用不了了，全局唯一 ID 怎么生成？主流方案对比一下。</p>
<h2>UUID</h2><p>本地生成、无网络开销，但 36 位字符串太长且无序，做 InnoDB 主键会导致页分裂，一般只用于日志 traceId 这类场景。</p>
<h2>数据库号段模式</h2><p>一张 ID 表存当前最大值和步长，服务一次取一段缓存在内存里用完再取。实现简单、趋势递增，缺点是服务重启会浪费号段、强依赖 DB 可用性（可双 buffer 优化）。</p>
<h2>雪花算法（Snowflake）</h2><p>64 位 = 1 符号位 + 41 时间戳 + 10 机器位 + 12 序列号。本地生成、趋势递增、每毫秒 4096 个，是最常用的方案。唯一要小心的是时钟回拨——要么等时钟追上，要么用逻辑时钟兜底，机器位分配也要规划好（机房+机器编号）。</p>
<p>选型建议：中小项目号段模式足够；追求性能和有序性上雪花；别用 UUID 当主键。</p>"""},
{"cat": "后端", "title": "消息队列如何保证消息不丢失", "tags": ["MQ", "Kafka", "可靠性"],
"content": """<p>消息从生产到消费要闯三关，任何一关丢了就是线上事故。可靠性方案要逐环节配置。</p>
<h2>生产端：确保送出去了</h2><p>同步发送 + 重试，或开启 confirm/ack 机制。Kafka 设置 acks=all 并配合 retries，RocketMQ 用同步发送并检查发送结果。本地消息表是更重的兜底：先落库再发送，定时任务补偿。</p>
<h2>Broker 端：确保存下来了</h2><p>持久化必须开：Kafka 配置 replication.factor >= 3、min.insync.replicas >= 2；RocketMQ 同步刷盘 + 主从同步。吞吐和可靠性是权衡，看业务选档位。</p>
<h2>消费端：确保处理完了</h2><p>关闭自动提交 offset，业务逻辑处理成功后手动 ack。消费失败进重试队列，多次失败进死信队列人工介入。千万别用异步线程处理完之前就 ack。</p>
<p>总结：生产端确认、 broker 持久化、消费端手动 ack，三关都守住了消息才敢说不丢。</p>"""},
{"cat": "后端", "title": "接口性能优化的常用手段与排查顺序", "tags": ["性能优化", "Java"],
"content": """<p>接口慢不能上来就"加缓存"，先定位瓶颈在哪一层，再对症下药。分享我的排查顺序和常用手段。</p>
<h2>先定位：慢在哪一段</h2><p>链路追踪（或最朴素的分段打点日志）把耗时拆成：网关 → 应用逻辑 → DB/下游调用 → 响应传输。八成以上的慢接口瓶颈在数据库。</p>
<h2>数据库层</h2><p>慢查询日志 + EXPLAIN 分析；该建索引建索引，该改写改写；大分页用游标方式（where id > last_id limit 20）代替 limit 100000, 20；大列表用批量查询替代循环单查（消灭 N+1）。</p>
<h2>应用层</h2><p>能缓存的读接口上缓存（注意一致性和击穿问题）；非核心链路异步化（发短信、记日志丢 MQ）；查询字段按需裁剪，别 select *。</p>
<h2>架构层</h2><p>读写分离分散读压力；热点数据本地缓存挡在最前面；实在顶不住再考虑水平扩容，毕竟扩容是最贵的手段。</p>
<p>记住：先测量再优化，凭感觉优化十有八九是白干。</p>"""},
{"cat": "后端", "title": "Spring Bean 的生命周期：从实例化到销毁", "tags": ["Spring", "面试", "原理"],
"content": """<p>Bean 生命周期是 Spring 面试的高频题，也是理解 Spring 扩展机制的基础。按顺序梳理一遍。</p>
<h2>主干流程</h2><p>①根据 BeanDefinition 反射实例化（构造器）；②属性填充（依赖注入发生在这里）；③Aware 回调（BeanNameAware、ApplicationContextAware 等）；④BeanPostProcessor 前置处理；⑤初始化：@PostConstruct → InitializingBean.afterPropertiesSet → init-method；⑥BeanPostProcessor 后置处理（AOP 代理对象通常在这一步生成）；⑦使用；⑧容器关闭时销毁：@PreDestroy → DisposableBean.destroy → destroy-method。</p>
<h2>为什么常用</h2><p>BeanPostProcessor 是 Spring 最强的扩展点，@Autowired、@Async、事务代理全靠它。理解了生命周期，很多"注解为什么不生效"的问题就迎刃而解。</p>
<h2>记忆技巧</h2><p>一句话：构造 → 注入 → Aware → 前处理 → 初始化 → 后处理 → 使用 → 销毁。初始化三兄弟的先后顺序：注解在前、接口在中、配置在后。</p>"""},
{"cat": "后端", "title": "用 Docker 部署 Spring Boot 项目的完整流程", "tags": ["Docker", "部署", "Linux"],
"content": """<p>从"本地能跑"到"服务器上跑"，Docker 是目前最省心的方式。记录一次完整的部署流程。</p>
<h2>编写 Dockerfile</h2><p>多阶段构建：第一阶段用 maven 镜像编译打包，第二阶段只复制 jar 到 JRE 镜像里，最终镜像体积能从 600MB 降到 200MB 以内。注意加 -Djava.security.egd 提升随机数初始化速度，EXPOSE 声明端口。</p>
<h2>编排依赖</h2><p>应用通常还要连 MySQL 和 Redis，用 docker-compose 把 app、mysql、redis 编到一起，depends_on 控制启动顺序，healthcheck 保证数据库就绪后应用才起。数据卷挂载出来，容器重建数据不丢。</p>
<h2>发布流程</h2><p>mvn package 打包 → docker build 打镜像 → docker push 推仓库（或直接 scp）→ 服务器 docker compose pull && up -d 滚动更新。配上 GitHub Actions 就是半自动 CI/CD，加一个 webhook 就是全自动。</p>
<p>踩坑提醒：容器内访问宿主机服务用 host.docker.internal（Mac/Win）或 --network host（Linux），localhost 是容器自己。</p>"""},
{"cat": "后端", "title": "单元测试在业务项目中的落地实践", "tags": ["测试", "JUnit", "工程化"],
"content": """<p>"没时间写单测"是借口，"写了没人看"是现实。分享我在业务项目里让单测真正落地的一些做法。</p>
<h2>技术选型</h2><p>JUnit 5 + Mockito + AssertJ 的组合基本是 Java 圈标配。Spring Boot 自带 spring-boot-starter-test，纯逻辑用不着起 Spring 容器，普通 Mock 单测跑得飞快；只有集成测试才用 @SpringBootTest。</p>
<h2>测什么</h2><p>优先覆盖：核心业务规则（金额计算、状态流转）、容易回归的 bug 修复点、工具类。不追求覆盖率指标，追求"改坏必报"——那些逻辑分支复杂又经常改动的代码才是重点。</p>
<h2>怎么写</h2><p>一个测试方法只测一件事，命名见名知意（should_throw_when_amount_negative 这种）。外部依赖（DB、HTTP）全部 mock 掉，单测不依赖环境才跑得快、才有人愿意跑。</p>
<p>落地心得：把单测纳入 code review 的检查项，新代码没测试不让合入，坚持一个月团队习惯就养成了。</p>"""},

# ============ 前端 (category_id=2) ============
{"cat": "前端", "title": "Vue2 响应式原理：一张图讲清依赖收集", "tags": ["Vue", "原理", "前端"],
"content": """<p>Vue2 的响应式核心是 Object.defineProperty，面试必考，理解它才能解释一堆"为什么不生效"的问题。</p>
<h2>三个角色</h2><p>Observer 递归遍历 data，把每个属性用 defineProperty 改造成 getter/setter；Dep 是依赖收集器，每个属性对应一个 Dep；Watcher 是订阅者，渲染函数、computed、watch 都是 Watcher。</p>
<h2>依赖收集流程</h2><p>组件渲染时触发属性的 getter，把当前 Watcher 收进对应 Dep；属性被修改时触发 setter，通知 Dep 里的所有 Watcher 重新渲染。这就是"数据变了视图跟着变"的全部秘密。</p>
<h2>已知缺陷</h2><p>①defineProperty 监听不到属性的新增和删除，所以才有 Vue.set / Vue.delete；②数组是通过重写七个变异方法实现的响应式，通过下标直接赋值 arr[0] = x 不生效；③初始化时就存在的数据才会被劫持。</p>
<p>Vue3 换成 Proxy 解决了这些问题，但理解 Vue2 的这套机制依然是前端面试的基本功。</p>"""},
{"cat": "前端", "title": "Vue 组件通信的 8 种方式，各自的适用场景", "tags": ["Vue", "组件通信"],
"content": """<p>组件通信是 Vue 项目的日常，方式很多，关键是选对场景。</p>
<h2>父子组件</h2><p>①props / $emit：最基本的方式，父传子用 props，子传父用事件；②$refs：父组件直接拿子组件实例调方法，适合操作子组件内部状态（如表单校验）；③v-model / .sync：本质还是 props + 事件，语法糖而已。</p>
<h2>隔代与兄弟</h2><p>④provide / inject：跨层级注入，适合深层组件拿祖先的配置；⑤EventBus：空 Vue 实例当事件总线，小项目兄弟通信够用，用完记得 off 防止内存泄漏；⑥$attrs / $listeners：透传父级传下来的属性和事件，写高阶包装组件时很好用。</p>
<h2>全局状态</h2><p>⑦Vuex：复杂应用的全局状态管理；⑧localStorage / sessionStorage + storage 事件：跨页面通信，不算 Vue 的机制但实战常用。</p>
<p>原则：先想 props/emit，解决不了再升级手段，别上来就全局状态，组件会失去复用性。</p>"""},
{"cat": "前端", "title": "Vuex 在项目中的正确打开姿势", "tags": ["Vuex", "状态管理"],
"content": """<p>Vuex 用不好会把简单项目搞复杂。分享我总结的几条实践原则。</p>
<h2>什么该放进 Vuex</h2><p>全局共享且多组件依赖的：登录用户信息、权限菜单、字典数据、跨页面需要保持的筛选条件。组件私有的表单数据、临时状态老老实实放 data 里，别什么都往 store 塞。</p>
<h2> Mutation 与 Action 的分工</h2><p>Mutation 是同步修改 state 的唯一途径，devtools 靠它追踪每次变更；Action 负责异步逻辑（调接口），拿到结果再 commit。有人嫌两层麻烦直接在组件里调 action 再 commit mutation，链路清晰比少几行代码重要。</p>
<h2>模块化</h2><p>按业务域拆 module（user、blog、activity），开启命名空间防止命名冲突。state 用函数返回（避免模块复用时引用共享）。</p>
<h2>持久化</h2><p>登录态这种需要刷新不丢的，用 vuex-persistedstate 插件或手动同步到 localStorage，注意敏感字段别落盘。</p>
<p>一句话：Vuex 解决的是"共享"和"可追踪"，不是"所有状态的家"。</p>"""},
{"cat": "前端", "title": "vue-router 导航守卫实战：登录拦截怎么做", "tags": ["Vue Router", "鉴权", "前端"],
"content": """<p>导航守卫是前端鉴权的核心手段，以登录拦截为例讲讲完整实现。</p>
<h2>守卫的分类</h2><p>全局守卫：beforeEach / afterEach，每次路由跳转都会经过；路由独享：route 配置里的 beforeEnter；组件内：beforeRouteEnter / Update / Leave。日常业务主要用全局 beforeEach。</p>
<h2>登录拦截的标准写法</h2><p>①维护一个白名单（/login、/register 等无需登录的页面）；②beforeEach 里判断目标是否在白名单，在就 next() 放行；③不在白名单则检查本地登录态（token 或用户信息），有就 next()；④没有则重定向到 /login 并带上 redirect 参数，登录成功后跳回原页面。</p>
<h2>进阶：权限路由</h2><p>登录只是第一层，菜单级权限做法是：登录后拉取用户权限，动态 addRoutes 注册有权限的路由，或全部注册但在守卫里校验目标路由的 meta 权限，无权限跳 403。</p>
<p>提醒：前端路由守卫只是体验层的拦截，真正的安全必须由后端接口鉴权保证，前端拦得住页面拦不住直接调接口的人。</p>"""},
{"cat": "前端", "title": "axios 二次封装：拦截器与统一错误处理", "tags": ["axios", "工程化"],
"content": """<p>裸用 axios 会让每个页面都写重复的 baseURL、token、错误处理。二次封装一次，全项目受益。</p>
<h2>创建实例</h2><p>axios.create({ baseURL: process.env.VUE_APP_BASEURL, timeout: 30000 })，环境地址放 .env 文件里，开发、测试、生产各一套。</p>
<h2>请求拦截器</h2><p>统一塞 token 到 header；对 GET 参数做序列化；上传接口单独设置 Content-Type 为 multipart。还可以在这里加防重复提交：相同 url+params 的请求进行中就取消。</p>
<h2>响应拦截器</h2><p>统一剥壳：后端如果包了 {code, msg, data}，在这里把 code !== 200 的情况统一提示并 reject，让业务代码只拿干净的 data；401 状态统一跳登录页；网络错误（response 为 undefined 的 error 分支）统一弹"网络异常"。</p>
<h2>使用方式</h2><p>导出封装后的实例，按模块拆 api 文件（user.js、blog.js），页面里只 import api 调函数，不直接碰 axios。换请求库、改提示方式，只动一处。</p>
<p>这套封装在 Vue2 项目里我已经用了三四年，直接抄走就能用。</p>"""},
{"cat": "前端", "title": "前端性能优化清单：从加载到渲染", "tags": ["性能优化", "前端"],
"content": """<p>性能优化是前端进阶绕不开的话题，整理一份我自己项目里反复用的清单。</p>
<h2>资源加载</h2><p>①路由组件懒加载：() => import('./views/xxx')，首屏体积立减一半以上；②图片懒加载 + WebP 格式 + 合适尺寸；③第三方库按需引入（element-ui 用 babel-plugin-component）；④静态资源上 CDN 并开 gzip/br 压缩；⑤合理缓存：带 hash 的文件设强缓存，index.html 设协商缓存。</p>
<h2>渲染优化</h2><p>①大列表虚拟滚动，别一次渲染一万条 DOM；②高频事件防抖节流（搜索输入、resize）；③v-for 必须带稳定的 key，别用 index；④长任务拆分，避免长时间占用主线程；⑤keep-alive 缓存列表页状态，返回不重查。</p>
<h2>度量先行</h2><p>用 Lighthouse 和 Performance 面板看首屏时间、FCP、长任务，优化前后对比数据，别凭感觉。</p>
<p>收益最大的通常是：懒加载、按需引入、图片优化这三板斧。</p>"""},
{"cat": "前端", "title": "ES6+ 实用特性盘点：写出现代感的 JavaScript", "tags": ["JavaScript", "ES6"],
"content": """<p>ES6 之后 JS 的书写体验脱胎换骨，盘点日常开发里使用频率最高的特性。</p>
<h2>解构与展开</h2><p>const { name, age = 18 } = obj、const [...rest] = arr，函数参数对象解构更是必备；展开运算符合并对象数组：{ ...defaults, ...options }，注意是浅拷贝。</p>
<h2>箭头函数与 this</h2><p>箭头函数没有自己的 this，继承外层作用域——这既是优点（回调里不用 that = this）也是坑（不能当对象方法、不能做构造函数）。</p>
<h2>异步三件套</h2><p>Promise 解决回调地狱，async/await 让异步代码看起来像同步。记住 await 只能包一层 try-catch，多个独立请求用 Promise.all 并行而不是顺序 await。</p>
<h2>实用小特性</h2><p>可选链 obj?.a?.b 和空值合并 obj?.count ?? 0，判空代码少一半；Map/Set 处理去重和映射；模板字符串替代拼接。</p>
<p>这些特性组合起来，代码量和可读性都会有质的提升。</p>"""},
{"cat": "前端", "title": "一文搞懂 CSS Flex 布局", "tags": ["CSS", "布局"],
"content": """<p>Flex 出现之前，垂直居中和等高布局要靠各种黑科技。现在一个 display: flex 解决 90% 的布局问题。</p>
<h2>容器属性（加在父元素上）</h2><p>flex-direction 决定主轴方向；justify-content 主轴对齐（space-between 两端对齐最常用）；align-items 交叉轴对齐（center 就是垂直居中）；flex-wrap 换行；gap 控制间距，比 margin 方案干净得多。</p>
<h2>项目属性（加在子元素上）</h2><p>flex: 1 是 flex-grow:1 + flex-shrink:1 + flex-basis:0% 的简写，表示"平分剩余空间"；固定侧边栏给固定宽度，主区域 flex:1，经典后台布局三行 CSS 搞定。</p>
<h2>常用套路</h2><p>①水平垂直居中：容器 justify-content + align-items 双 center；②左右布局右侧自适应；③底部 footer 固定：容器 min-height:100vh + flex 纵向 + 内容区 flex:1；④文本超出省略配合 min-width: 0 解决 flex 子项不收缩的问题。</p>
<p>Grid 更适合二维布局，但日常一维场景 Flex 依然是性价比最高的选择。</p>"""},
{"cat": "前端", "title": "浏览器跨域的来龙去脉与解决方案", "tags": ["跨域", "CORS", "前端"],
"content": """<p>每个前端都遇到过跨域报错，但能把原理讲清楚的不多。这篇从同源策略讲到解决方案。</p>
<h2>什么是同源策略</h2><p>协议、域名、端口三者完全一致才算同源。浏览器出于安全考虑，限制脚本跨源读取响应——注意：请求其实发出去了，服务器也返回了，是浏览器把响应扣下了。</p>
<h2>CORS：正解</h2><p>服务端设置 Access-Control-Allow-Origin 等响应头声明允许的来源。复杂请求（非 GET/POST、带自定义头）会先发 OPTIONS 预检请求，服务端要正确响应预检。Spring 项目里一个 CorsFilter 配置就能解决，生产环境别用 * 而是白名单。</p>
<h2>开发环境代理</h2><p>前后端分离开发时，前端在 vue.config.js 里配 devServer.proxy，让请求先发给同源的开发服务器再转发给后端，绕开浏览器限制。这只解决开发环境，上线要靠后端 CORS 或 Nginx 反向代理。</p>
<h2>其他方案</h2><p>Nginx 反向代理把前后端收敛到同一域名（生产最常用）；JSONP 利用 script 标签不受限的特性，只支持 GET，属于历史方案；postMessage 用于跨窗口通信。</p>
<p>记住一句话：跨域是浏览器行为，绕开它的所有思路本质都是"让请求看起来同源"或"让服务器点头"。</p>"""},
{"cat": "前端", "title": "前端登录态与按钮级权限控制方案", "tags": ["鉴权", "前端", "权限"],
"content": """<p>权限控制分页面级、菜单级、按钮级，一篇讲清我在项目里的完整方案。</p>
<h2>登录态管理</h2><p>token 和用户信息存 localStorage（需要跨标签页就别用 sessionStorage），axios 拦截器统一携带，401 统一清登录态跳登录页。token 过期时间与后端保持一致，敏感操作前后端双重校验。</p>
<h2>页面与菜单级</h2><p>路由 meta 里标记权限标识，全局守卫校验；侧边栏菜单根据用户角色过滤渲染。动态路由方案是登录后 addRoutes，刷新时要在守卫里重新拉取权限再放行，注意死循环问题。</p>
<h2>按钮级</h2><p>注册一个自定义指令 v-permission="['admin']"，指令内部判断当前用户角色，无权限就把元素 remove 掉。相比 v-if 散落在模板里，指令写法更集中、语义更清晰。</p>
<h2>兜底思维</h2><p>前端所有权限控制都是体验层的，直接调接口的场景必须靠后端拦截器兜底。前后端权限标识保持同一套字典，避免两边对不上。</p>"""},
{"cat": "前端", "title": "Webpack 打包体积优化实录：首屏从 4MB 到 1.2MB", "tags": ["Webpack", "工程化", "性能"],
"content": """<p>上次优化一个 Vue2 老项目，首屏 JS 从 4MB 降到 1.2MB，过程记录下来。</p>
<h2>第一步：分析</h2><p>用 webpack-bundle-analyzer 生成可视化报告，一眼看到大头：element-ui 整包引入（700KB）、moment.js 带了全部语言包（500KB echarts 同理）、多个页面把 xlsx 和富文本打进了主包。</p>
<h2>第二步：动手</h2><p>①element-ui 按需引入（babel-plugin-component）；②moment 忽略语言包ContextReplacementPlugin，只留中文；③echarts、wangeditor、xlsx 改为路由级异步加载，用到时才 import()；④生产环境关掉 sourcemap；⑤splitChunks 把稳定依赖拆成 vendor 长缓存。</p>
<h2>第三步：压缩</h2><p>gzip 在 Nginx 层开启（或打包时同时产出 .gz），1.2MB 压完传输只有 350KB 左右；图片压缩、小图转 base64（url-loader 阈值）。</p>
<p>经验总结：先分析再动手，优化的大头永远是"别把用户暂时用不到的代码发给他"。</p>"""},
{"cat": "前端", "title": "移动端适配：rem 与 vw 方案怎么选", "tags": ["移动端", "CSS", "适配"],
"content": """<p>移动端适配的核心问题：同一套代码如何在 320px 到 750px+ 的屏幕上都表现正常。对比两个主流方案。</p>
<h2>rem 方案</h2><p>根字号随屏宽变化，元素全部用 rem 单位。常见做法：设计稿 750px，1rem = 100px，JS 监听 resize 动态设置 html 的 font-size = 屏宽 / 7.5，配合 postcss-pxtorem 自动把 px 转 rem。兼容性好（iOS 6+），需要一点 JS 配合。</p>
<h2>vw 方案</h2><p>100vw = 屏幕宽度，直接用 vw 单位或 postcss-px-to-viewport 转换，纯 CSS 无需 JS，缩放连续无锯齿。兼容性 iOS 8+，现在基本没有障碍。</p>
<h2>怎么选</h2><p>新项目我直接用 vw 方案，配置最简单、精度最高；需要兼容老 WebView 的项目用 rem + flexible。两者都要配合：1px 边框问题（devicePixelRatio 缩放）、字体不建议随屏幕无限缩放（设置最小字号）、图片用 aspect-ratio 固定比例防抖动。</p>
<p>无论哪种方案，记住设计稿还原的前提是和 UI 约定好基准宽度（通常 750）。</p>"""},
]
