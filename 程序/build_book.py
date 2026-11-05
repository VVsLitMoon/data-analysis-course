"""Build the authored curriculum into a browser book, Markdown and runnable examples."""
from pathlib import Path
import json,re,textwrap
ROOT=Path(__file__).resolve().parent.parent
lessons=[]
modules=[('start','00 起点：先理解数据'),('sql','01 SQL：从查询到手撕'),('python','02 Python 与 Pandas'),('stats','03 概率与统计'),('ab','04 AB 实验与因果'),('business','05 电商业务分析'),('tools','06 工具、模型与工程'),('path','07 复习与面试衔接')]
def add(m,title,body,code='',engine='sql',q='',options=None,answer=0,explain='',task='',hint='',solution='',advanced=False,lab=''):
 n=1+sum(x['module']==m for x in lessons)
 if options:
  shift=n%len(options)
  options=options[shift:]+options[:shift]
  answer=(answer-shift)%len(options)
 lessons.append(dict(id=f'{m}-{n:02}',module=m,title=title,body=textwrap.dedent(body).strip(),code=textwrap.dedent(code).strip(),engine=engine,quiz={'q':q,'options':options or [],'answer':answer,'explain':explain},task=task,hint=hint,solution=solution,advanced=advanced,lab=lab))

add('start','怎么使用本讲义', '''
## 先完成一个很小的动作
你现在不需要会编程。先点练习区的“运行代码”，你会看到一个名为 result 的结果列，数值是 2。把代码里的 1 + 1 改成 1 + 2，再运行，结果就变成 3。这就是编程最基本的循环：表达想法、运行、看结果、修改。
## 学习顺序
先读“起点”，接着 SQL 前半和 Python 入门。之后交替学习统计与业务；窗口函数和实验设计需要前面的基础。每节只做四件事：读懂例子、运行默认代码、完成小改动、回答自测。连续不懂两节，就回到前置概念。
## 代码在哪里运行
双击本文件夹的“启动讲义.cmd”，浏览器会打开本地页面。SQL 用本机 MySQL 8.0；Python 用本机 Python 环境。每次点击运行都会恢复示例数据，因此大胆修改。代码区的一次运行里可以放多条 SQL。
直接打开 index.html 也能读书、自测和看预期结果，但运行代码需要启动本地程序。学习进度保存在当前浏览器，换浏览器前先导出。
## 对“学会”的定义
看到答案觉得熟悉不等于会做。能解释每一行、能修改条件、第二天能不看答案复现，才适合标记“我理解了”。本讲义覆盖入门所需范围，不宣称穷尽所有可能的面试问题。
''','SELECT 1 + 1 AS result;',q='第一次学习最合适的动作是？',options=['运行一个小例子，再修改一个数字','马上计时做困难题','背下所有函数名字'],explain='先建立代码与结果之间的联系。',task='让 result 等于 7。',hint='试试加法或乘法。',solution='SELECT 3 + 4 AS result;')
add('start','表、行、列和数据粒度','''
## 像看 Excel 一样看数据库
一张表像一张规整的 Excel 工作表。列表示属性，例如用户编号、注册日期；行表示一个对象或一次事件。users 的一行是一个用户，orders 的一行是一笔订单。数据库是管理这些表的软件；SQL 是向它提要求的语言。
## 粒度决定能不能相加
“一行代表什么”叫数据粒度。用户表有 7 行，不代表 7 笔订单；一个用户能下多单。订单金额可以按订单相加，用户年龄却不应该在订单表连接后直接平均，否则多下单的人会被重复计算。
## 读懂右边两句话
SELECT 表示选取，星号表示全部列，FROM 表示从哪张表取。分号结束一条语句。先看 users，再看 orders，找出重复的 user_id 和不重复的 order_id。
## 练习使用的模拟电商数据
为了练习数据分析，我们准备了一组虚构的电商平台数据，记录用户注册、登录、浏览商品和下单等行为。你在代码中看到的表名，都对应这组练习数据。
users 是用户表：每行记录一位用户的信息，包括用户编号、注册日期和城市。orders 是订单表：每行记录一笔订单，包括订单编号、下单用户、时间和金额。同一位用户可以有多笔订单，所以这两张表的行数不一定相同。
现在先认识 users 和 orders 就够了。后面还会用到 logins（登录记录）、events（浏览、加购和支付行为）、assignments（实验分组）和 calendar（日期表），用到时会逐一解释。点击页面上方“查看示例数据”，可以直接看到各表的内容。
示例订单的时间设在 2026 年 1—3 月。订单状态 paid 表示已支付，cancelled 表示已取消，refunded 表示已退款。本讲义计算支付订单数量和金额时，只纳入 paid 状态的订单。
''','SELECT * FROM users;\nSELECT * FROM orders LIMIT 5;',q='orders 表里 user_id 重复意味着？',options=['同一个用户可能下多笔订单','表一定损坏了','这些行必须删掉'],explain='订单粒度允许用户重复，订单编号才是这一表的唯一标识。',task='把 LIMIT 5 改成 LIMIT 2，观察行数。',hint='LIMIT 控制最多返回多少行。')
add('start','编号、主键与表之间的关系','''
## 为什么不拿姓名当编号
两个人可能同名，一个人可能改名。主键是能唯一识别一行的列或列组合，通常不允许重复和空值。users 的主键是 user_id，orders 的主键是 order_id。
## 一个用户，多笔订单
orders.user_id 指向 users.user_id，这是业务上的关联关系。一对多表示一个用户对应多笔订单。外键约束能由数据库检查引用关系，但教学订单表未实际建立外键；有同名列也不自动保证数据一致。
## 联合键和重复
“用户 + 日期”可能代表用户某天是否活跃。登录明细同一天能登录多次，先去重才得到用户日表。不同粒度需要不同键，不能一见重复就删除。
''','SELECT user_id, COUNT(*) AS order_rows FROM orders GROUP BY user_id;',q='用户表与订单表通常是什么关系？',options=['一对多','一定一对一','完全没有关系'],explain='用户有零笔、一笔或多笔订单。',task='观察哪些用户没有出现在结果里。',hint='没有订单的用户不会出现在仅从 orders 查询的结果中。')
add('start','比例、百分比、百分点与增长率','''
## 分子和分母要同口径
100 个访问用户里 10 人购买，购买转化率是 10 / 100 = 10%。分子是购买人数，分母是访问人数，必须来自同一时间、同一人群。订单数除以用户数不是用户转化率。
## 最容易混淆的两句话
转化率从 10% 到 12%，绝对增加 2 个百分点；相对增长是 (12% - 10%) / 10% = 20%。从 0 增到 10 的相对增长率没有通常意义下的有限值，需要单独说明。
## 数学符号先认识这几个
Σ 表示把数加起来；n 是个数；x̄ 是平均值；√ 是平方根；|x| 是距离 0 的大小。乘法用 *，除法用 /，Python 次方用 **。先理解含义，再熟悉写法。
''','SELECT 10.0/100 AS rate, (0.12-0.10)*100 AS percentage_points, (0.12-0.10)/0.10 AS relative_lift;',q='从 20% 到 25% 是？',options=['增加 5 个百分点，相对增长 25%','相对增长 5%','增加 25 个百分点'],explain='0.05 / 0.20 = 0.25。',task='算从 4% 到 5% 的百分点变化和相对增长。',hint='先做新值减旧值，再除旧值。')
add('start','空值、异常值和业务口径','''
## 空白不等于零
NULL 表示未知、未记录或不适用。用户城市为空，并不意味着“没有城市”；金额为 0 可能是免费订单。把空值直接补成零会改变均值和比例，补之前要知道空值为什么产生。
## 先问清楚再计算
“收入是多少”至少要确认：按下单还是支付时间、是否扣退款、是否含运费、货币单位、时区、测试账户是否排除、数据是否已完整到账。这些约定叫指标口径。
## 看起来奇怪不等于错误
999 元取消订单不该算进本例支付 GMV，但金额大本身不能证明异常。数据检查包含主键重复、缺失、负数、时间先后、取值范围和数据到达延迟。
''',"SELECT status, COUNT(*) AS n, SUM(amount) AS amount_sum FROM orders GROUP BY status;\nSELECT * FROM users WHERE city IS NULL;",q='城市缺失最合适的理解是？',options=['城市信息未知，需要明确如何处理','城市就是零','整行一定应删除'],explain='缺失原因和分析目标决定处理方式。')
add('start','报错、结果检查和拆题方法','''
## 先读错误，不要立刻重写
SQL 报 Unknown column，通常是列名拼错或别名作用阶段不对；syntax error 常见原因是漏逗号、括号或用了中文标点。Python NameError 是变量还不存在，IndentationError 是缩进不一致。先找错误位置，再一次改一个问题。
## 没报错也可能做错
结果能运行只是第一关。检查行数、主键是否唯一、金额总和有没有翻倍、比例是否在合理范围、没有订单的人是否被保留。用一个人和两三行手算，最容易发现口径错误。
## 通用四步
第一，写出输出一行代表什么。第二，写清分子分母及过滤条件。第三，拆成中间表逐步运行。第四，加入空值、并列、重复、无订单等边界情况。不要靠不停加 DISTINCT 掩盖连接错误。
''',"SELECT COUNT(*) AS all_rows, COUNT(DISTINCT user_id) AS users_with_orders FROM orders;",q='SQL 不报错能证明答案正确吗？',options=['不能，还要检查口径和边界','能','只要加 DISTINCT 就能'],explain='语法正确与业务正确是两回事。')

add('sql','第一条查询：SELECT、FROM 与别名','''
## 把中文问题翻译成 SQL
问题是“查看用户编号和所在城市”。SELECT 后面列出想看的列，列之间用英文逗号；FROM 后面写表名。AS 给输出列起一个便于阅读的新名字，不会修改原表。
## 按顺序读代码
第一行选择 user_id 和 city，第二行说明从 users 获取。SQL 关键字不要求大写，但统一大写便于区分。字符串用单引号，例如 '上海'；数字一般不加引号。-- 后面是注释，不执行。
## 常量也能被查询
SELECT 2 * 3 不需要表；有 FROM 时，常量通常在每一行重复出现。不要把列名写成 'user_id'，那会把固定文字当结果。
''',"SELECT user_id AS id, city AS user_city\nFROM users;",q="SELECT 'city' FROM users 得到什么？",options=['每行都是 city 这个文字','每人的城市','必定报错'],explain='单引号包住的是字符串，不是列引用。',task='把输出增加一列 channel。',hint='在列清单里加英文逗号和列名。',solution='SELECT user_id AS id, city AS user_city, channel FROM users;')
add('sql','筛选：WHERE、比较与逻辑','''
## 逐行决定保留谁
WHERE 对每行判断条件，只保留结果为 TRUE 的行。= 等于，<> 不等于，> 大于，>= 大于等于。SQL 比较相等是一个等号，Python 是两个。
## 同时与任选
AND 要求两个条件都成立，OR 只需至少一个，NOT 取否定。AND 通常比 OR 先计算，混用时直接加括号，避免错误理解。
## 例子的业务含义
只选 paid 且金额至少 100 的订单。先筛状态，再筛金额。若题目要“上海或者北京的自然流量用户”，应写 (city='上海' OR city='北京') AND channel='organic'。
''',"SELECT order_id, user_id, amount\nFROM orders\nWHERE status = 'paid' AND amount >= 100;",q='AND 的意思是？',options=['两个条件都成立','任意一个成立即可','删除符合条件的行'],explain='WHERE 只筛选结果，不会删除源表。',task='找 paid 且金额小于 100 的订单。',hint='把 >= 改为 <。')
add('sql','范围、列表和模糊匹配','''
## 三个常用简写
IN ('上海','北京') 表示在列表里；BETWEEN 50 AND 100 包含两端，相当于 >=50 AND <=100；LIKE '%海%' 表示包含“海”。LIKE 的 % 匹配任意长度，_ 匹配一个字符。
## 日期边界特别重要
DATETIME 带时分秒。查询整个 1 月，用 >= '2026-01-01' AND < '2026-02-01'。BETWEEN '2026-01-01' AND '2026-01-31' 可能只包含 31 日零点，漏掉其余时间。
## 类型与大小写
字符是否区分大小写由排序规则决定，不要假设所有数据库一样。IN 中的字符串必须加单引号；LIKE 是模式匹配，不是复杂正则。
''',"SELECT * FROM users WHERE city IN ('上海','北京');\nSELECT order_id, order_at FROM orders WHERE order_at >= '2026-01-01' AND order_at < '2026-02-01';",q='查询整月时间最稳妥的范围是？',options=['本月起点 <= 时间 < 下月起点','只等于本月第一天','到最后一天零点为止'],explain='左闭右开同时覆盖所有时分秒。',task="把城市条件改为 city LIKE '%海%'。",hint='会匹配上海。')
add('sql','NULL：IS NULL、COALESCE 与三值逻辑','''
## 未知参与比较仍可能未知
NULL = NULL 不返回 TRUE，NULL <> 1 也不是 TRUE。WHERE 只保留 TRUE，因此查询缺失值用 IS NULL，非缺失用 IS NOT NULL，不能用 = NULL。
## 给展示结果兜底
COALESCE(city, '未知') 返回从左到右第一个非空参数。它不修改原表，只替换当前结果的展示。NULLIF(a,b) 在二者相等时返回 NULL，常用 NULLIF(分母,0) 防止把除零当正常比例。
## 三个特别坑
COUNT(列) 不数空值，COUNT(*) 数行。NOT IN 的候选集合如果含 NULL，可能意外没有结果；需要时使用 NOT EXISTS。空字符串 '' 与 NULL 是不同概念。
''',"SELECT user_id, COALESCE(city,'未知') AS city_label FROM users;\nSELECT 3.0 / NULLIF(0,0) AS safe_ratio;",q='筛选缺失城市应写？',options=['city IS NULL','city = NULL',"city = 'NULL'"],explain='NULL 是特殊空值标记，字符串 NULL 只是四个字母。')
add('sql','排序、限制与去重','''
## 行没有默认顺序
ORDER BY amount DESC 表示金额从大到小，ASC 是从小到大。金额并列时加 order_id，排序才稳定。LIMIT 3 返回排序后最多三行，并不是自动找前三名。
## DISTINCT 对整组列去重
SELECT DISTINCT user_id 得到不同用户。SELECT DISTINCT user_id, category 得到不同的“用户—品类”组合，同一个用户仍能出现多次。
## LIMIT 与排名的区别
LIMIT 3 只要三行；“前三种金额且保留并列”需要后面的 DENSE_RANK。数据很大时 OFFSET 分页可能慢，面试进阶可了解按索引键继续翻页。
''',"SELECT order_id, amount FROM orders WHERE status='paid' ORDER BY amount DESC, order_id LIMIT 3;\nSELECT DISTINCT user_id, category FROM orders ORDER BY user_id, category;",q='DISTINCT user_id, category 对什么去重？',options=['整对值','只对 user_id','只对 category'],explain='SELECT 中的全部选定列共同决定重复。',task='改成最便宜的三笔 paid 订单。',hint='DESC 改成 ASC。')
add('sql','聚合：COUNT、SUM、AVG、MIN、MAX','''
## 把多行变成摘要
SUM(amount) 把金额相加，AVG 求平均，MIN/MAX 找最小最大。没有 GROUP BY 时，整个筛选结果作为一个组，通常返回一行摘要。
## 计数有三种
COUNT(*) 数所有行；COUNT(city) 数城市非空的行；COUNT(DISTINCT user_id) 数不同且非空的用户。订单数和购买人数因此不同。
## 没有数据怎么办
无符合记录时 COUNT 为 0，SUM 和 AVG 通常为 NULL。业务明确需要零时再 COALESCE(SUM(amount),0)。AVG 会忽略空值；把空值补零以后平均值会改变。
''',"SELECT COUNT(*) AS paid_orders, COUNT(DISTINCT user_id) AS buyers, SUM(amount) AS gmv, AVG(amount) AS aov FROM orders WHERE status='paid';\nSELECT COUNT(*) AS users, COUNT(city) AS known_city_users FROM users;",q='购买人数通常应该怎样统计？',options=['COUNT(DISTINCT user_id)','COUNT(*) 一定可以','SUM(user_id)'],explain='同一个买家可能有多笔订单。',task='筛出 2026 年 2 月 paid 订单再算上述指标。',hint='WHERE 再追加左闭右开的日期范围。')
add('sql','GROUP BY 与 HAVING','''
## 先分组，再分别计算
GROUP BY channel 表示按渠道分组，每组做 COUNT 或 SUM。最终一行代表一个渠道，不再是一位用户。SELECT 中普通列应该是分组键，其余列应聚合；MySQL 的严格分组模式会阻止许多不明确写法。
## 筛行与筛组
WHERE 在聚合前筛明细，HAVING 在聚合后筛组。找“paid 订单总额超过 200 的用户”，paid 写 WHERE，总额超过 200 写 HAVING。
## 逻辑执行顺序
理解为 FROM/JOIN → WHERE → GROUP BY → HAVING → 窗口计算 → SELECT → DISTINCT → ORDER BY → LIMIT。优化器实际执行可调整，但这个顺序能解释为什么 WHERE 不能用窗口结果。
''',"SELECT user_id, COUNT(*) AS paid_orders, SUM(amount) AS gmv\nFROM orders\nWHERE status='paid'\nGROUP BY user_id\nHAVING SUM(amount)>200\nORDER BY gmv DESC;",q='筛选总额超过 200 的用户用？',options=['HAVING SUM(amount)>200','WHERE SUM(amount)>200','LIMIT 200'],explain='聚合之后才有每个用户的总额。',task='只保留至少 3 笔 paid 订单的用户。',hint='HAVING COUNT(*) >= 3。')
add('sql','CASE WHEN：条件分类与条件聚合','''
## 在 SQL 中表达“如果”
CASE WHEN 条件 THEN 结果 ELSE 其他结果 END。按顺序检查，第一个成立的分支生效，漏写 ELSE 时未匹配的行返回 NULL。不同分支尽量保持相同数据类型。
## 条件计数为什么成立
CASE WHEN status='paid' THEN 1 ELSE 0 END 把 paid 订单变成 1，其余变成 0；再 SUM 就是 paid 行数。COUNT(CASE WHEN 条件 THEN 1 END) 也可计数，因为未命中返回 NULL。
## 一个常见错误
COUNT(CASE WHEN 条件 THEN 1 ELSE 0 END) 会把 0 也计入，所以数的是全部非空行。条件金额用 SUM(CASE WHEN 条件 THEN amount ELSE 0 END)。
''',"SELECT user_id, SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END) AS paid_n, SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) AS paid_amount FROM orders GROUP BY user_id;",q='COUNT(CASE WHEN 条件 THEN 1 ELSE 0 END) 会？',options=['把 0 和 1 都计数','只计 1','只计 0'],explain='COUNT 关心是不是 NULL，不关心是不是 0。',task='增加取消订单数量。',hint="新增 SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END)。")
add('sql','INNER JOIN：按键连接两张表','''
## 为什么需要连接
订单里没有渠道，用户表里有渠道。要按渠道统计支付金额，需要把每笔订单对应的用户信息补上。JOIN 是按条件寻找匹配行，不是按行号拼接。
## 逐行理解
users u 中 u 是表的短名字；orders o 同理。ON u.user_id=o.user_id 指定相同用户才匹配。u.channel 表示来自用户表的 channel。INNER JOIN 只保留双方都能匹配的行。
## 连接后的一行是什么
在用户主键唯一的前提下，连接后每一行仍是一笔订单。用户会因为多笔订单重复出现。因此连接后求用户数通常需要 COUNT(DISTINCT u.user_id)。
''',"SELECT u.channel, COUNT(*) AS paid_orders, SUM(o.amount) AS gmv\nFROM users u JOIN orders o ON u.user_id=o.user_id\nWHERE o.status='paid'\nGROUP BY u.channel;",q='JOIN 的 ON 条件的作用是？',options=['规定哪些行互相匹配','规定输出排序','自动删除重复订单'],explain='它表达关联关系。',task='改为按城市统计。',hint='SELECT 和 GROUP BY 都改成 u.city。')
add('sql','LEFT JOIN：保留没有订单的用户','''
## 左表是你要保留的人群
LEFT JOIN 保留左表每一行。没有右表匹配时，右表列填 NULL。用户没有订单也应出现在报表时，用 users 作左表。
## 条件写错位置会丢人
右表的 paid 条件写在 ON 里，表示只匹配 paid 订单；若放 WHERE o.status='paid'，没有订单的人因为 NULL 比较不是 TRUE 而被过滤，失去保留作用。
## 计数也要配合
COUNT(*) 会把无订单用户那一行也数成 1；COUNT(o.order_id) 才是订单数。金额展示为 0 用 COALESCE(SUM(o.amount),0)。
''',"SELECT u.user_id, COUNT(o.order_id) AS paid_orders, COALESCE(SUM(o.amount),0) AS gmv\nFROM users u LEFT JOIN orders o ON u.user_id=o.user_id AND o.status='paid'\nGROUP BY u.user_id ORDER BY u.user_id;",q='保留零订单用户时 paid 条件应放哪里？',options=['JOIN 的 ON 中','一定放 WHERE 中','ORDER BY 中'],explain='WHERE 对右表条件筛选会把未匹配的 NULL 行去掉。',task='只看没有 paid 订单的用户。',hint='在分组之后添加 HAVING COUNT(o.order_id)=0。')
add('sql','连接翻倍、自连接与笛卡尔积','''
## 为什么金额突然变大
一个用户有 3 笔订单、4 条登录。直接按 user_id 把两张明细连接，产生 3×4=12 行，每笔订单被重复 4 次。SUM 就会翻倍。DISTINCT 金额会误删不同订单的相同金额，无法正确修复。
## 先聚合到需要的粒度
先把订单变成一人一行金额、登录变成一人一行次数，再按用户连接。连接前先问每边的键是否唯一。
## 另外两种连接
自连接是同一张表使用两个别名，可比较同一用户前后订单；记得用时间和编号限制配对，避免自己连自己和重复对。CROSS JOIN 得到全部组合，例如日期×渠道补零框架；行数等于两侧行数相乘。
MySQL 8.0 没有原生 FULL OUTER JOIN，可用左连接加右侧未匹配行 UNION ALL 模拟，先掌握左连接即可。
''',"WITH a AS (SELECT user_id,SUM(amount) AS gmv FROM orders WHERE status='paid' GROUP BY user_id), b AS (SELECT user_id,COUNT(*) AS login_n FROM logins GROUP BY user_id)\nSELECT u.user_id,COALESCE(a.gmv,0) AS gmv,COALESCE(b.login_n,0) AS login_n FROM users u LEFT JOIN a ON u.user_id=a.user_id LEFT JOIN b ON u.user_id=b.user_id;",q='3 笔订单和 4 条登录直接按用户连接有几行？',options=['12 行','7 行','3 行'],explain='每笔订单会匹配该用户的全部 4 条登录。',task='用代码结果手算用户 1 的金额是否正确。',hint='只把 paid 订单金额加一次。')
add('sql','子查询、EXISTS 与反连接','''
## 查询也能当材料
子查询是括号里的查询。返回一个数的叫标量子查询，如全体平均金额；FROM 中的子查询像临时表，需要起别名。相关子查询会引用外层当前行的值。
## 有没有比连上多少更合适
EXISTS 只关心子查询是否存在至少一行。找有 paid 订单的用户时，不会因为多笔订单重复用户。NOT EXISTS 查没有匹配的用户，通常比含 NULL 风险的 NOT IN 更清楚。
## 别把“全体均值”和“用户均值”搞混
一笔订单高于全体订单均值，和一个用户总消费高于平均用户总消费，是两道不同问题。先确定比较粒度。
''',"SELECT u.user_id FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id=u.user_id AND o.status='paid');\nSELECT order_id,amount FROM orders WHERE status='paid' AND amount>(SELECT AVG(amount) FROM orders WHERE status='paid');",q='EXISTS 返回的核心含义是？',options=['是否存在匹配行','匹配行的金额之和','匹配行的第一列文字'],explain='SELECT 1 是惯用写法，判断的是行是否存在。')
add('sql','CTE 与 UNION：把复杂查询拆开','''
## 给中间结果起名字
WITH paid AS (...) 定义只在本条语句里可用的公共表表达式，简称 CTE。它不是永久表。多个 CTE 用逗号分隔，后面的可以引用前面的。
## 按问题的层次拆
先得到用户金额，再筛高价值用户，最后汇总渠道。每一层写出粒度，比一口气嵌套很多括号更易检查。CTE 不保证一定物化或更快，优化器会选择。
## 上下拼接与左右连接
UNION ALL 上下拼接并保留重复；UNION 会去重。两边列数相同，对应类型兼容，按列的位置对应，不是按列名。JOIN 是横向补列，不能混淆。
''',"WITH paid AS (SELECT * FROM orders WHERE status='paid'), spend AS (SELECT user_id,SUM(amount) AS gmv FROM paid GROUP BY user_id)\nSELECT * FROM spend WHERE gmv>=200 ORDER BY user_id;\nSELECT 'A' AS label UNION ALL SELECT 'A';",q='UNION ALL 的特点是？',options=['上下拼接并保留重复','横向按键匹配','一定去重'],explain='ALL 表示保留所有输入行。',task='把 UNION ALL 改成 UNION，观察变化。',hint='两行相同文字会变成一行。')
add('sql','窗口函数：保留明细，也看组内信息','''
## 聚合和窗口的差别
GROUP BY 会把多行收成一行；窗口函数给每行增加组内计算结果，保留原来明细。想同时看每笔订单金额和该用户总额时，窗口很合适。
## 三个组成部分
SUM(amount) OVER(PARTITION BY user_id) 中 SUM 是计算，PARTITION BY 按用户分区，OVER 告诉数据库这是窗口计算。窗口内 ORDER BY 指定计算顺序；最终输出顺序仍需查询末尾 ORDER BY。
## 先筛再算
WHERE status='paid' 会先筛掉非支付订单，窗口只看筛后的行。窗口结果不能直接写在同层 WHERE，先放 CTE，再由外层筛选。
''',"SELECT order_id,user_id,amount,SUM(amount) OVER(PARTITION BY user_id) AS user_total\nFROM orders WHERE status='paid' ORDER BY user_id,order_id;",q='窗口 SUM 默认会把每个用户压成一行吗？',options=['不会，保留输入行','会','只能用在一张一行的表'],explain='这正是窗口和 GROUP BY 的关键区别。',task='去掉 PARTITION BY user_id，观察每行总额。',hint='OVER() 表示把全部输入行当同一窗口。')
add('sql','三种排名与每组 Top N','''
## 先用 100、100、80 理解
ROW_NUMBER 给出 1、2、3；RANK 给出 1、1、3；DENSE_RANK 给出 1、1、2。ROW_NUMBER 需要稳定的并列打破规则，例如 order_id；RANK/DENSE_RANK 如果把唯一编号加入排名排序，就破坏金额并列语义。
## “前 3”必须问清楚
恰好最多 3 行选 ROW_NUMBER<=3；前三种不同金额选 DENSE_RANK<=3；竞赛名次前三选 RANK<=3，可能不足三种金额。面试说明你采用哪一种。
## 查询结构
内层计算每个用户内的金额名次，外层筛 rn<=2。外层排序只是方便阅读，不改变名次定义。
''',"WITH ranked AS (SELECT order_id,user_id,amount,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY amount DESC,order_id) AS rn FROM orders WHERE status='paid')\nSELECT * FROM ranked WHERE rn<=2 ORDER BY user_id,rn;",q='100、100、80 的 DENSE_RANK 是？',options=['1、1、2','1、2、3','1、1、3'],explain='密集排名保留并列且不跳号。',task='输出每个用户最大的两种金额，保留并列。',hint='用 DENSE_RANK，窗口排序只保留 amount DESC。')
add('sql','LAG、LEAD 与相邻比较','''
## 向前看和向后看
LAG(value) 取排序后上一行的值，LEAD 取下一行。第一行没有上一行通常返回 NULL。PARTITION BY 决定在哪个人或哪类商品内部移动。
## 上一行不等于昨天
如果某用户只在 1 日和 5 日下单，LAG 得到的是上一笔订单日期 1 日，不是 4 日。月度数据缺了 2 月时，3 月上一行可能是 1 月，做环比要先补全月份。
## 稳定排序
按时间再按订单号排列，才能在同一时刻多笔订单时保持确定。相邻时间差用 TIMESTAMPDIFF(单位,先前,当前)。
''',"WITH t AS (SELECT order_id,user_id,order_at,LAG(order_at) OVER(PARTITION BY user_id ORDER BY order_at,order_id) AS previous_at FROM orders WHERE status='paid')\nSELECT *,TIMESTAMPDIFF(HOUR,previous_at,order_at) AS gap_hours FROM t ORDER BY user_id,order_at,order_id;",q='LAG 取到的必定是昨天吗？',options=['不是，是排序后的上一行','是','只取最小值'],explain='日历连续性必须另行保证。')
add('sql','累计、滑动窗口与 ROWS / RANGE','''
## 累计值包含哪些行
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW 表示从第一行累计到当前行。ROWS BETWEEN 2 PRECEDING AND CURRENT ROW 表示当前行与前两行，共最多三行。
## 明确窗口边界
带 ORDER BY 却不写 frame 时，许多聚合窗口默认 RANGE 到当前同行值，会把排序值相同的行一起包括。初学时写清 ROWS 和稳定排序，避免并列日期累计看起来突然跳跃。
## 最近七行不等于最近七天
先按天汇总并补齐没有交易的日期，才能用 ROWS 6 PRECEDING 表示当天加前六天。另一种方法是日期范围连接。滚动均值还要说明不足七天时使用已有天数还是固定七天作分母。
''',"SELECT order_id,user_id,amount,SUM(amount) OVER(PARTITION BY user_id ORDER BY order_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_gmv FROM orders WHERE status='paid' ORDER BY user_id,order_at,order_id;",q='7 日滚动和 7 行滚动何时等价？',options=['一日一行且日历连续时','任何订单明细上都等价','只有金额相同时'],explain='必须先保证行对应连续日期。')
add('sql','日期、字符串、类型转换和数值精度','''
## 常用日期函数
DATE(datetime) 取日期；DATE_ADD(date,INTERVAL 1 DAY) 加一天；DATEDIFF(后,前) 返回日期天数差；TIMESTAMPDIFF(SECOND,前,后) 看更细时间差。DATE_FORMAT(date,'%Y-%m') 可做月份标签，展示字符串不等于日期类型。
## 字符串与转换
CONCAT 拼接文本，SUBSTRING 从 1 开始取片段，TRIM 去首尾空格，LOWER 转小写。CAST('123' AS UNSIGNED) 转整数，转换失败或截断可能受 SQL 模式影响，别用它掩盖脏数据。
## 钱和小数
DECIMAL 是定点小数，适合金额；FLOAT/DOUBLE 是近似浮点。ROUND 用于最终展示，过早四舍五入会累积误差。整数编号不应该拿来求平均；DATE、DATETIME 与带时区解释也要区分。
''',"SELECT DATE('2026-01-31 13:20:00') AS dt,DATE_ADD('2026-01-31',INTERVAL 1 DAY) AS next_day,DATEDIFF('2026-02-02','2026-01-31') AS day_gap,DATE_FORMAT('2026-01-31','%Y-%m') AS month;\nSELECT CONCAT('user-',CAST(7 AS CHAR)) AS label,ROUND(100.0/3,2) AS amount;",q='DATEDIFF(后日期, 前日期) 的常见含义是？',options=['相差的天数','相差的秒数','两日期字符串拼接'],explain='需要秒级差值时用 TIMESTAMPDIFF。')
add('sql','留存率：先定义 cohort 和观察窗','''
## 同一起点的人放在一组
cohort 是具有同一入组时间或特征的人群。注册次日留存率：某日注册用户中，在注册日后第 1 个自然日登录的人数 / 该日注册人数。它不是“所有今天活跃者里昨天也活跃的比例”。
## 为什么先去重
同一用户次日登录 5 次也只算 1 位留存用户。把登录明细先转为用户—日期唯一记录，再连接注册人群，防止分子分母被重复。
## 尚未观察不能当流失
数据只到 1 月 31 日时，1 月 31 日注册的次日留存还不可观察，应排除或标记未成熟，而不是按 0。D1、D7、7 日内回访和第 7 日回访是不同定义。
''',"WITH d AS (SELECT DISTINCT user_id,DATE(login_at) AS dt FROM logins)\nSELECT u.signup_date,COUNT(*) AS new_users,COUNT(d.user_id) AS retained_users,ROUND(COUNT(d.user_id)/COUNT(*),4) AS d1_retention\nFROM users u LEFT JOIN d ON u.user_id=d.user_id AND d.dt=DATE_ADD(u.signup_date,INTERVAL 1 DAY)\nWHERE u.signup_date < '2026-03-31' GROUP BY u.signup_date ORDER BY u.signup_date;",q='一个新用户次日登录 5 次，应计多少留存用户？',options=['1','5','0'],explain='留存的计量单位是用户。',task='改成注册第 2 天登录的留存。',hint='INTERVAL 1 DAY 改成 2 DAY，并同步调整可观察边界。')
add('sql','连续登录：去重、编号、找日期差','''
## 连续天数不是登录次数
某人在 1 日登录两次、2 日一次、3 日一次，连续是 3 天，不能说 4 天。第一层先取 DISTINCT user_id, DATE(login_at)。
## 连续日期减连续编号得到同一个锚点
1 月 1、2、3 日的序号是 1、2、3，各自减序号天都指向同一天。5、6 日减后续序号得到另一个锚点。按用户与锚点分组，就得到每段连续区间。
## 面试讲法
先说明每日去重，再用 ROW_NUMBER 按日编号，再用 DATE_SUB 生成分组锚点，最后 COUNT 得连续长度。可进一步取每人最大长度或筛至少三天。
''',"WITH d AS (SELECT DISTINCT user_id,DATE(login_at) AS dt FROM logins), r AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY dt) AS rn FROM d), g AS (SELECT *,DATE_SUB(dt,INTERVAL rn DAY) AS anchor FROM r)\nSELECT user_id,MIN(dt) AS start_date,MAX(dt) AS end_date,COUNT(*) AS streak_days FROM g GROUP BY user_id,anchor HAVING COUNT(*)>=3 ORDER BY user_id,start_date;",q='连续登录题的第一步是什么？',options=['按用户和自然日去重','直接数登录行数','只保留每人第一天'],explain='一天的多次登录不能增加连续天数。',task='找至少连续 2 天的区间。',hint='修改 HAVING 阈值即可。')
add('sql','复购、首单和最后一单','''
## 先说明复购单位
同一天两单算不算复购？有的题定义两笔 paid 订单，有的要求不同购买日，有的关注首购后 30 天内再次购买。先定义，不能套一个公式到所有场景。
## 找首单与末单
ROW_NUMBER 按 order_at、order_id 升序取第一行为首单；降序取第一行为末单。MIN(order_at) 只给时间，不能自动拿到那笔订单的其他所有字段。
## 复购率的分母
一个观察窗内，复购买家 / 至少购买一次的买家，是一种常见定义。新客 30 日复购的分母必须只含有足够 30 天观察期的新客，否则低估。
''',"WITH buyer AS (SELECT user_id,COUNT(*) AS paid_orders,COUNT(DISTINCT DATE(order_at)) AS paid_days FROM orders WHERE status='paid' GROUP BY user_id)\nSELECT COUNT(*) AS buyers,SUM(paid_orders>=2) AS repeat_by_orders,SUM(paid_days>=2) AS repeat_by_days FROM buyer;",q='同一天两单是否复购由什么决定？',options=['题目的业务定义','SQL 自动决定','永远不算'],explain='先约定按订单数还是不同购买日。')
add('sql','漏斗：有人看、有人加购、有人购买','''
## 漏斗是按路径看流失
浏览 → 加购 → 支付。宽松口径可以只要求同一用户各事件出现过；严格漏斗还要求时间先后、同一会话或规定窗口。三种事件人数直接相除，不一定是路径转化。
## 先做最容易解释的一种
本例统计 1 月 1 日“当天有各事件”的用户数，不要求顺序，所以明确叫事件覆盖，不称严格有序漏斗。条件 COUNT(DISTINCT ...) 让一个用户多次浏览只算一次。
## 严格漏斗怎么延伸
先确定每用户第一个浏览，再找浏览之后第一个加购，再找加购之后的支付，规定窗口和相同业务对象。不能只取所有事件的独立最早时间：最早加购在浏览前时，之后的有效加购可能被漏掉。
''',"SELECT COUNT(DISTINCT CASE WHEN event_type='view' THEN user_id END) AS viewers,COUNT(DISTINCT CASE WHEN event_type='cart' THEN user_id END) AS cart_users,COUNT(DISTINCT CASE WHEN event_type='pay' THEN user_id END) AS pay_users FROM events WHERE event_at>='2026-01-01' AND event_at<'2026-01-02';",q='每个事件都出现过是否保证有序漏斗？',options=['不保证，还需事件时间顺序','保证','只要人数一样就保证'],explain='有的用户可能先支付后浏览。')
add('sql','环比、同比与日期补零','''
## 比较的基准是什么
环比是与上一个可比周期相比，同比增长是与去年同周期相比。增长率 = (本期 - 基期) / 基期。基期为 0 时标记不可直接计算，不要伪装成 0% 增长。
## 缺失月份不应跳过
先造月份表，左连接月度金额，将确实无订单的月份补零，再 LAG。数据未到齐的月份应标记不完整，不能随意补零。
## 可比性比公式重要
本月只有前 10 天，不能直接和上个月完整月比较；春节错位、天数不同、退款延迟也会影响结果。下面教学日历完整，因此可以示范补零。
''',"WITH months AS (SELECT DISTINCT DATE_FORMAT(dt,'%Y-%m') AS mon FROM calendar), m AS (SELECT DATE_FORMAT(order_at,'%Y-%m') AS mon,SUM(amount) AS gmv FROM orders WHERE status='paid' GROUP BY mon), filled AS (SELECT months.mon,COALESCE(m.gmv,0) AS gmv FROM months LEFT JOIN m USING(mon)), lagged AS (SELECT *,LAG(gmv) OVER(ORDER BY mon) AS previous_gmv FROM filled)\nSELECT *,ROUND((gmv-previous_gmv)/NULLIF(previous_gmv,0),4) AS mom FROM lagged ORDER BY mon;",q='基期为 0 时，通常应该？',options=['标记相对增长不可直接计算','增长率一定 0%','增长率一定 100%'],explain='公式分母为零，需要单独说明。')
add('sql','七日滚动：先补日期再开窗口','''
## 把文字口径变成边界
“截至当天的近 7 个自然日”包含当天和前 6 天；“过去 7 天且不含当天”则是前 7 天至前 1 天。半开区间能避免午夜边界重复。
## 两层查询各做一件事
先以 calendar 为左表补全每日 paid 金额，再在这张一日一行表上做 ROWS 6 PRECEDING。因为 calendar 从 1 月 1 日开始，头 6 天窗口少于 7 个观察日。
## 筛日期的位置会改变窗口
若只想展示 1 月 7 日以后的结果，应先计算含前六天的窗口，再在外层筛日期。提前删掉历史日期会导致首行窗口不完整。
''',"WITH daily AS (SELECT c.dt,COALESCE(SUM(o.amount),0) AS gmv FROM calendar c LEFT JOIN orders o ON DATE(o.order_at)=c.dt AND o.status='paid' GROUP BY c.dt), rolling AS (SELECT *,SUM(gmv) OVER(ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS gmv_7d FROM daily)\nSELECT * FROM rolling WHERE dt BETWEEN '2026-01-07' AND '2026-01-12' ORDER BY dt;",q='展示日期筛选通常放在何时？',options=['计算完整窗口之后','必须在窗口之前','不能筛选'],explain='否则历史行被提前移走，窗口起点会错误。')
add('sql','中位数、分位数与分布','''
## 中位数怎么手算
先排序，奇数个取中间一个，偶数个取中间两个的平均。中位数受极端大值影响较小，但不能代替总额；分位数描述低于某个值的比例，不同软件的插值定义可能不同。
## MySQL 8.0 的实现思路
MySQL 8.0 没有通用内置 MEDIAN 聚合。用 ROW_NUMBER 排序，同时 COUNT(*) OVER() 得总数，挑出 FLOOR((n+1)/2) 和 FLOOR((n+2)/2) 两个位置，最后 AVG。
## 进阶认识
NTILE(4) 尽量按行数分四桶，相同金额可能拆桶；PERCENT_RANK 与 CUME_DIST 的并列规则不同。做金额分层先约定边界，不能把所有“分位”函数当成同义词。
''',"WITH r AS (SELECT amount,ROW_NUMBER() OVER(ORDER BY amount,order_id) AS rn,COUNT(*) OVER() AS n FROM orders WHERE status='paid')\nSELECT AVG(amount) AS median_amount FROM r WHERE rn IN (FLOOR((n+1)/2),FLOOR((n+2)/2));",q='偶数个数的中位数通常取？',options=['中间两数平均','最大的数','最小的数'],explain='先排序，再取中间两个。',advanced=True)
add('sql','建表、修改数据和事务','''
## 查询之外还有什么
CREATE TABLE 定义列与类型，INSERT 添加行，UPDATE 修改行，DELETE 删除行，DROP TABLE 删除整表。读题阶段通常只需要 SELECT，真实工作中修改数据应先确认范围和备份。
## 约束防止坏数据
PRIMARY KEY 唯一且非空；UNIQUE 通常限制重复；NOT NULL 不许缺失；CHECK 表达取值规则；FOREIGN KEY 约束关联。数据库约束和业务校验互相补充。
## 事务把操作当作一组
START TRANSACTION 开始，COMMIT 确认，ROLLBACK 撤销未提交修改。下面只改讲义的 scratch 表，回滚后恢复。InnoDB 支持事务，DDL 常有隐式提交，不能假设 DROP 可回滚。
ACID 分别是原子性、一致性、隔离性、持久性。脏读、不可重复读、幻读是并发观察问题；隔离级别与 MVCC、锁的细节放在面试进阶。
''',"SELECT * FROM scratch;\nSTART TRANSACTION;\nUPDATE scratch SET amount=99 WHERE id=1;\nSELECT * FROM scratch;\nROLLBACK;\nSELECT * FROM scratch;",q='ROLLBACK 在这里的作用是？',options=['撤销未提交修改','永久删除数据库','按金额排序'],explain='本例只涉及支持事务的表内 DML。',advanced=True)
add('sql','索引、EXPLAIN 与常见 SQL 八股','''
## 索引像书的目录
索引帮助快速定位部分行，代价是空间和写入维护。并非每个条件都走索引；低选择性、小表、函数包裹列、隐式类型转换等会影响优化器选择。联合索引的列顺序要结合过滤和排序。
## 先看计划再下结论
EXPLAIN 显示访问方式、候选与实际索引、估计行数等。type=ALL 表示扫描，不等于必然有问题；小表扫描可能合理。EXPLAIN ANALYZE 会实际执行查询，面对昂贵语句要知道代价。
## 八股的理解版
DELETE 通常按行删除并可有 WHERE；TRUNCATE 清空表且常隐式提交；DROP 删除表定义。WHERE 筛行，HAVING 筛组。视图是保存的查询定义，不默认存一份独立结果。规范化减少冗余，分析宽表便于查询但要管理口径和更新一致性。
## 性能排查顺序
先保证结果对，再缩小扫描范围、只选需要的列、在合适粒度预聚合、检查连接键及数据倾斜；最后看索引与执行计划。不能为“更快”改变业务结果。
''',"EXPLAIN SELECT * FROM orders WHERE order_id=101;\nEXPLAIN SELECT * FROM orders WHERE amount>100;",q='索引越多一定越好吗？',options=['不是，会增加写入和存储成本','是','索引只能用于排序'],explain='需要根据工作负载权衡。',advanced=True)

add('python','Python 第一步：变量、类型与 print','''
## 像给计算结果贴标签
price = 20 把整数 20 绑定到变量 price。等号在这里是赋值；比较相等写 ==。print(price) 把内容显示出来，否则运行脚本可能没有可见输出。
## 四种先认识的类型
int 是整数，float 是小数，str 是文本，bool 是 True/False。'20' 是文本，20 是数字，不能随意相加。None 表示缺少一个值，与 0、空字符串不同。
## 读代码的方法
程序通常从上到下执行，后面的变量可用前面的结果。# 后面是注释。变量名用能解释业务的英文或拼音，避免单字母堆叠。先改数值观察输出，再尝试增加计算。
''','price = 20\nquantity = 3\nrevenue = price * quantity\nprint("收入：", revenue)\nprint("变量类型：", type(revenue).__name__)'.replace('type(revenue).__name__','type(revenue)'),engine='python',q='Python 中 price = 20 表示？',options=['给变量赋值','判断是否相等','打印 20'],explain='判断相等写 price == 20。',task='把数量改成 5，计算收入。',hint='只修改 quantity 的值。')
add('python','列表、字典、索引和切片','''
## 一串值和一组对应关系
列表 [10,20,30] 按顺序保存多个值，字典 {'organic':100,'paid':80} 按键查值。列表从 0 开始编号，a[0] 是第一个；a[-1] 是最后一个。切片 a[0:2] 取第 0、1 位，不包含第 2 位。
## 不要把容器混淆
元组 tuple 常表示固定组合，集合 set 存不同元素且不能靠它保留排序。len 求长度，sum 对数值求和。字典的键必须存在才能直接索引，也可用 .get(键,默认值)。
## 可变对象要留心
b=a 不会复制整个列表，两个名字指向同一对象；简单列表复制用 a.copy()。复杂嵌套复制另有细节，先能识别“修改共享对象”的问题。
''','amounts = [100, 50, 80]\nchannels = {"organic": 100, "paid": 80}\nprint(amounts[0], amounts[-1], amounts[:2])\nprint(sum(amounts), len(amounts))\nprint(channels.get("new_channel", 0))',engine='python',q='列表第一项的索引是？',options=['0','1','-2'],explain='Python 索引从 0 开始。',task='加入第四个金额并求平均。',hint='平均值 = sum(amounts) / len(amounts)。')
add('python','条件、循环与缩进','''
## 如果满足条件，就执行
if 后面写条件和英文冒号，下面缩进四个空格。elif 是另一种情况，else 兜底。缩进决定哪些代码属于分支，不只是排版。
## 对每个元素重复同一动作
for amount in amounts 依次把列表元素交给 amount。range(3) 得到 0、1、2。while 在条件成立时持续运行，初学尽量先用有明确终点的 for，避免无限循环。
## 计数器怎么工作
先设 total=0，再每次 total += amount，相当于 total=total+amount。break 结束循环，continue 跳过本次剩余操作。能用向量化处理表时，Pandas 通常不必逐行循环。
''','amounts = [100, 50, 0, 80]\ntotal = 0\nfor amount in amounts:\n    if amount > 0:\n        total += amount\n        print("计入：", amount)\nprint("合计：", total)',engine='python',q='Python 用什么确定代码块范围？',options=['缩进','句号','中文括号'],explain='保持一致缩进是语法要求。',task='只累计至少 80 的金额。',hint='把 if 条件改为 amount >= 80。')
add('python','函数、模块、异常与调试','''
## 把重复逻辑装进函数
def rate(buyers,visitors): 定义函数，括号里是参数。return 把结果交给调用者，print 只是显示。函数内部的局部变量通常不应该靠外部代码直接读取。
## 不要藏住错误
除零、错误类型、不存在的列都会报异常。先看报错最后一行，再找代码行号；可以 print 中间变量或用 VS Code 断点。try/except 用于能合理处理的已知问题，不要一股脑忽略所有错误。
## 导入模块，使用现成的函数
import math 导入模块，math.sqrt(4) 求平方根。库版本不同可能影响行为。本讲义运行时预装了 pandas、NumPy、SciPy、scikit-learn；文件和网络读写留在你自己的 VS Code 环境操作。
''','def conversion_rate(buyers, visitors):\n    if visitors == 0:\n        return None\n    return buyers / visitors\n\nprint(conversion_rate(12, 100))\nprint(conversion_rate(0, 0))\nimport math\nprint(math.sqrt(16))',engine='python',q='return 与 print 的区别是？',options=['return 交回结果，print 显示内容','完全一样','return 只用于循环'],explain='函数返回值可继续参与计算。',task='把第一个调用改成 25 位购买、200 位访问。',hint='修改函数调用参数，不需要修改定义。')
add('python','DataFrame：在 Python 中看一张表','''
## 两个对象先分清
Pandas 的 DataFrame 是二维表，Series 是一列带索引的数据。每次运行，讲义已准备 users、orders、logins、events、assignments、calendar 六张 DataFrame，与 SQL 用的是同一组数据。
## 先检查再分析
head() 看前几行，shape 看行列数量，columns 看列名，dtypes 看数据类型。info() 会直接打印摘要；describe() 描述数值分布，但不能替代业务理解。
## 与 SQL 对照
orders['amount'] 是一列；orders[['order_id','amount']] 是两列表。方括号里是列名列表；少一层括号时含义不同。示例日期最初是字符串，后面再转成日期。
''','print(orders.head(3))\nprint("行列数：", orders.shape)\nprint(orders.dtypes)\nprint(orders[["order_id", "amount"]].head())',engine='python',q="orders[['order_id','amount']] 返回？",options=['包含两列的表','一个数字','两行'],explain='双层括号的内层是列名列表。')
add('python','筛选、排序与新列','''
## 布尔条件像一列开关
orders['status']=='paid' 得到每行 True/False，把它放进 orders[...] 就只保留 True 的行。多个条件用 &、|、~，每个比较都加括号，不用 Python 的 and/or 连接整列。
## loc 与 iloc
.loc[行条件,列名] 按标签选取；.iloc[0:3,0:2] 按位置选取，右端不包含。sort_values 指定排序列和升降序。
## 安全添加新列
筛选后准备修改，先 .copy()。新列可以用整列运算生成，不必逐行循环。避免 chained assignment：不要连续两次方括号后直接赋值，使用 .loc 或明确副本。
''','paid = orders.loc[(orders["status"] == "paid") & (orders["amount"] >= 100)].copy()\npaid["amount_after_10pct_discount"] = paid["amount"] * 0.9\nprint(paid.sort_values(["amount", "order_id"], ascending=[False, True]))',engine='python',q='Pandas 两个整列条件通常用？',options=['&，每个比较加括号','and 且不用括号','英文逗号'],explain='整列逐元素逻辑与使用 &。',task='改成金额在 50 到 100 之间。',hint='两个金额比较都加括号后用 & 连接。')
add('python','groupby、聚合与 transform','''
## 从明细到用户摘要
groupby('user_id') 按用户分组，agg 可以同时求订单数、金额总和、均值。size 计行数，count 计非空值，nunique 计不同值；与 SQL 计数的细节对照理解。
## 想保留每行怎么办
transform('sum') 把每组汇总值广播回每行，相当于 SQL 的 SUM OVER(PARTITION BY)。agg 会缩成组级结果，transform 保留原来长度。
## 最新行与组内排名
先按用户、时间、订单号排序，再按 user_id 去重保留最后一条，可以取最新订单；并列时间由订单号打破。groupby()['amount'].rank(method='dense',ascending=False) 对应金额稠密排名；method='min' 类似 RANK，method='first' 按现有行顺序打破并列，因此使用前需排序。
## 两个默认值
groupby 常默认把空分组键排除，需要时用 dropna=False。as_index=False 让分组列保留为普通列，初学更容易继续连接。
''','paid = orders.loc[orders["status"] == "paid"].copy()\nsummary = paid.groupby("user_id", as_index=False).agg(paid_orders=("order_id", "size"), gmv=("amount", "sum"))\npaid["user_gmv"] = paid.groupby("user_id")["amount"].transform("sum")\npaid["amount_rank"] = paid.groupby("user_id")["amount"].rank(method="dense", ascending=False)\nlatest = paid.sort_values(["user_id", "order_at", "order_id"]).drop_duplicates("user_id", keep="last")\nprint(summary)\nprint(paid[["order_id", "user_id", "amount", "user_gmv", "amount_rank"]].head())\nprint("每位用户最新订单：")\nprint(latest[["user_id", "order_id", "order_at"]])',engine='python',q='transform 与 agg 的主要区别是？',options=['transform 通常保留原行数','transform 只能计数','agg 一定保留每行'],explain='它把组内结果对应回明细行。')
add('python','merge、concat 与连接检查','''
## 和 SQL JOIN 一样先检查键
merge(...,on='user_id',how='left') 左连接。validate='one_to_many' 表示期望左侧键唯一、右侧可重复；不满足时主动报错，有助于防止金额翻倍。
## 指标校验
连接前后比较订单数、总额和未匹配比例。indicator=True 增加匹配来源列。Pandas 缺失键之间的匹配行为与普通 SQL NULL 连接不同，遇到空键时要明确处理。
## 拼接与透视
concat 默认沿行方向拼接，列名不同会产生缺失。pivot 把唯一组合转为宽表，pivot_table 可先聚合；melt 把宽表拉成长表。行列结构是展示方式，不应偷偷改变指标定义。
## 实验按用户分析
先把 paid 订单汇成一人一行金额，再以 assignments 的入组用户为左表连接，没消费的金额填 0；is_buyer 在有 paid 订单时为 1（金额为零的支付订单也算买家）。最后按 arm 算用户数、购买率和人均金额，避免把订单当独立用户。
''','paid = orders.loc[orders["status"] == "paid"]\njoined = users.merge(paid, on="user_id", how="left", validate="one_to_many", indicator=True)\nprint(joined[["user_id", "order_id", "_merge"]])\nprint("合并后金额：", joined["amount"].sum())\nprint(paid.pivot_table(index="user_id", columns="category", values="amount", aggfunc="sum", fill_value=0))\nspend = paid.groupby("user_id", as_index=False).agg(gmv=("amount", "sum"), paid_orders=("order_id", "size"))\nexperiment = assignments.merge(spend, on="user_id", how="left", validate="one_to_one")\nexperiment[["gmv", "paid_orders"]] = experiment[["gmv", "paid_orders"]].fillna(0)\nexperiment["is_buyer"] = (experiment["paid_orders"] > 0).astype(int)\nprint(experiment.groupby("arm").agg(users=("user_id", "size"), conversion=("is_buyer", "mean"), gmv_per_user=("gmv", "mean")))',engine='python',q='validate 参数为什么有用？',options=['核对键的唯一性，及时发现意外关系','自动保证所有业务正确','只是让代码更快'],explain='它能防止本应一对多的连接悄悄变成多对多。')
add('python','缺失、重复、日期与滚动','''
## 清洗要保留解释
isna() 找缺失，fillna() 补值，dropna() 删缺失。drop_duplicates(subset=[...]) 依据指定键去重，但先确认哪一行该保留，例如按更新时间排序保留最后一条。不能把真实重复购买删掉。
## 日期转成可计算的类型
pd.to_datetime 把字符串变日期时间；errors='coerce' 会把无效字符串变 NaT，随后必须检查数量。.dt.date 取日，.dt.to_period('M') 取月。统一时区后再比较。
## 排序后才移动
groupby().shift() 对应 LAG。rolling(7) 是七行；按时间索引的 rolling('7D') 是时间窗，端点由 closed 等参数控制。先补日历更容易解释每天的滚动金额。
''','paid = orders.loc[orders["status"] == "paid"].copy()\npaid["dt"] = pd.to_datetime(paid["order_at"]).dt.normalize()\ndaily = paid.groupby("dt")["amount"].sum()\ndays = pd.date_range("2026-01-01", "2026-01-10")\ndaily = daily.reindex(days, fill_value=0)\nprint(pd.DataFrame({"gmv": daily, "rolling7": daily.rolling(7, min_periods=1).sum()}))\nprint("城市缺失数：", users["city"].isna().sum())',engine='python',q="rolling(7) 默认是指？",options=['7 行','无条件代表 7 天','7 个用户'],explain='只有连续一日一行时才恰好对应七天。')
add('python','NumPy、向量化和可复现抽样','''
## 数组会整批运算
NumPy 的数组与 Python 列表不同，np.array([1,2])*2 得 [2,4]，列表 [1,2]*2 会重复列表。向量化用底层数组操作，通常比逐个 Python 循环更适合大表。
## 随机不是不可验证
np.random.default_rng(42) 创建固定种子的随机数生成器，同一算法环境下复现同一抽样流程。换种子可检验结论是否依赖某次抽样；种子不能消除抽样误差。
## 文件与图表在本讲义的安排
网页运行区只展示文本与表格，交互图由后面的专用控件提供。导出的 Notebook 可在 VS Code 中运行和画图；导出脚本会包含示例数据初始化，离开网页也能用。
## 条件分层和除零
np.where(条件,成立取值,否则取值) 可以整列打标签，多分支可用 np.select。计算 Pandas 比率前，用分母.where(分母.ne(0)) 把零变成缺失，再用分子.div(分母)，避免出现无穷大。不要把“不可计算”和“结果为零”混成一件事。
''','import numpy as np\nx = np.array([1, 2, 3])\nprint("数组乘法：", x * 2)\nrng = np.random.default_rng(42)\nprint("抽 5 个 0 到 9 的整数：", rng.integers(0, 10, size=5))\nprint("均值：", x.mean())\nprint("分层：", np.where(x >= 2, "高", "低"))\nnumerator = pd.Series([10, 0])\ndenominator = pd.Series([100, 0])\nprint("安全比率：", numerator.div(denominator.where(denominator.ne(0))))',engine='python',q='固定随机种子主要用于？',options=['复现抽样过程','保证没有误差','让结果一定显著'],explain='可复现和无偏、显著是不同概念。')

add('stats','总体、样本、参数与统计量','''
## 为什么要学习统计
你想知道全部用户的购买率，却只能观察部分用户或某段时间。总体是你真正想了解的对象，样本是实际观察到的一部分。总体购买率是参数；样本购买率是统计量，会随抽样变化。
## 描述与推断
“这 100 人中有 12 人购买”是描述统计；“总体购买率大约 12%，不确定性是多少”是统计推断。多看一批样本可能得到 9% 或 14%，不一定是代码错了。
## 样本大也可能偏
只调查忠实老客，会高估全体满意度；只看完成订单会忽略流失的人，这是选择偏差或幸存者偏差。随机抽样有助代表总体，随机分流有助因果识别，两者目的不同。
## 数据类型决定方法
城市是名义分类，满意度等级是有序类别，订单数是离散数值，等待时间近似连续。不能把城市编码 1、2、3 当数值平均。独立观测也不是理所当然：一个人的多次点击往往相关。
''','import numpy as np\nrng = np.random.default_rng(42)\nfor n in [100, 1000, 10000]:\n    sample = rng.binomial(1, 0.12, size=n)\n    print(n, "人的样本购买率：", sample.mean())',engine='python',q='随机分流和随机抽样的主要目的相同吗？',options=['不同，前者支持因果，后者支持代表性','完全相同','两者都能修复所有偏差'],explain='随机分流不自动保证样本代表所有目标人群。')
add('stats','均值、中位数、方差和标准差','''
## 中心与分散要一起看
均值 = 总和 / 个数，中位数是排序中间位置，众数是最常见值。收入或消费长尾时，少数大值会拉高均值；同时看中位数和高分位更完整。
## 方差为什么平方
每个值减均值后的偏差直接相加会抵消，平方后不会抵消。总体方差取平方偏差平均；样本方差常除以 n-1，用于无偏估计总体方差。标准差是方差开平方，回到原单位。
## 不要混用分母
NumPy var 默认 ddof=0，Pandas Series.var 通常默认 ddof=1。它们可能算出不同数字而都符合各自定义。四分位距 IQR=Q3-Q1 描述中间一半的范围，对极端值较稳健。
''','import numpy as np\nx = np.array([10, 10, 20, 20, 200])\nprint("均值/中位数：", x.mean(), np.median(x))\nprint("总体方差：", x.var(ddof=0))\nprint("样本标准差：", x.std(ddof=1))\nprint("25/75 分位数：", np.quantile(x, [0.25, 0.75]))',engine='python',q='加入一个极端大值，通常哪个更敏感？',options=['均值','中位数','二者永远完全相同'],explain='均值使用每个值的具体大小。',task='把 200 改为 2000，比较均值和中位数。',hint='只修改最后一个数。')
add('stats','加权平均、标准化与辛普森悖论','''
## 整体比例不能随便平均
A 渠道 10 人里 5 人购买，B 渠道 100 人里 10 人购买。整体是 15/110，不是 (50%+10%)/2。应按分母加权：Σ(分组比例×分组人数)/总人数。
## 每组变好，整体也可能变差
当流量从高转化群体转向低转化群体，即便各群体转化率上升，整体也可能下降。这是辛普森悖论的一种情形。先看分层表现，再看结构占比变化。
## 标准化怎样帮助比较
固定同一套人群权重，比较两期的分层转化率，可以区分结构变化与组内变化。z-score=(x-均值)/标准差 用来衡量离均值几个标准差，但不会自动把任意分布变成正态。
''','buyers = [5, 10]\nvisitors = [10, 100]\nrates = [buyers[i] / visitors[i] for i in range(2)]\nprint("错误的等权平均：", sum(rates) / 2)\nprint("整体转化率：", sum(buyers) / sum(visitors))',engine='python',q='合并两组转化率时应该？',options=['合并分子分母，或按分母加权','永远直接平均比例','选较大比例'],explain='不同分组人数不一样时，等权平均会误导。')
add('stats','概率、组合计数与独立性','''
## 概率先从等可能结果理解
公平骰子有 6 个等可能面，掷出偶数的概率是 3/6。一般 P(A) 在 0 到 1 之间，补事件 P(非A)=1-P(A)。A 或 B 的概率等于 P(A)+P(B)-P(A且B)。
## 独立与互斥不同
独立表示知道 A 不改变 B 的概率，P(A且B)=P(A)P(B)。互斥表示不能同时发生，交集为零；两个概率都非零的互斥事件并不独立。
## 排列与组合
从 n 个里选 k 个不看顺序，组合数 C(n,k)=n!/[k!(n-k)!]。看顺序用排列 n!/(n-k)!。! 是阶乘，比如 3!=3×2×1。抽样放回通常保持抽取概率，不放回会改变后续概率。
''','import math\nprint("5 人选 2 人：", math.comb(5, 2))\nprint("公平硬币连续两次正面：", 0.5 * 0.5)\nprint("至少一次正面：", 1 - 0.5 ** 2)',engine='python',q='互斥与独立是同一个概念吗？',options=['不是','是','只有投硬币时一样'],explain='互斥知道一件发生，就排除另一件；这通常改变概率。')
add('stats','条件概率、全概率与贝叶斯','''
## 条件概率是在新范围内计算
P(A|B)=P(A且B)/P(B)，前提 P(B)>0。已知用户来自某渠道，再算购买概率，就是在该渠道的人群里换一个分母。P(A|B) 通常不等于 P(B|A)。
## 从不同来源合并
全概率把互斥且完整的来源分组加权：P(购买)=Σ P(购买|渠道)P(渠道)。贝叶斯反过来找“已购买的人来自某渠道的概率”。
## 低基准率为什么重要
假设异常订单占 1%，检测能发现 90% 异常，同时误报 5% 正常。10000 单中真报 90、误报 495，报异常后真的异常概率是 90/(90+495)，约 15.4%，不是 90%。
## 面试两箱题
先明确选箱概率，再写每箱抽到某颜色的概率，最后乘先验并归一化。是否放回、是否观察顺序都会改变计算，先复述条件再动笔。
''','base = 0.01\nsensitivity = 0.90\nfalse_positive = 0.05\ntrue_alert = base * sensitivity\nfalse_alert = (1 - base) * false_positive\nprint("告警为真概率：", true_alert / (true_alert + false_alert))',engine='python',q='P(异常|告警) 一定等于 P(告警|异常) 吗？',options=['不一定，还受到基准率影响','一定','都等于 50%'],explain='条件反向需要贝叶斯和先验概率。',task='把异常基准率从 1% 改为 10%，观察后验。',hint='保持检测能力不变，只改 base。',lab='bayes')
add('stats','随机变量、期望、方差与协方差','''
## 随机变量给结果一个数字
掷骰点数、用户是否购买、订单金额都是随机变量。离散变量可列概率质量函数；连续变量用密度描述，单个精确点的概率通常为零，区间面积才是概率。CDF 表示不超过 x 的累计概率。
## 期望不是最常出现的值
E(X)=ΣxP(X=x)，是长期平均的理论值。一个游戏 90% 得 0 元、10% 得 100 元，期望是 10 元，但一次游戏不会得到 10 元。
## 三个常用性质
E(aX+b)=aE(X)+b；Var(aX+b)=a²Var(X)；Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)。期望相加不要求独立；方差直接相加需要协方差为零，独立是充分条件。
## 协方差到相关系数
协方差看是否一起高低，除以两侧标准差得到 Pearson 相关系数，落在 [-1,1]。相关为零只代表无线性相关，不能推出一般意义的独立。
''','import numpy as np\nx = np.array([0, 100])\np = np.array([0.9, 0.1])\nmean = (x * p).sum()\nvariance = ((x - mean) ** 2 * p).sum()\nprint("期望：", mean, "方差：", variance)',engine='python',q='期望相加是否一定要求独立？',options=['不要求','要求','只适用于正态'],explain='期望线性性质普遍成立，方差相加则需要注意协方差。')
add('stats','伯努利、二项与超几何分布','''
## 一次成败与多次成败
一次是否购买可用伯努利分布：成功概率 p，期望 p，方差 p(1-p)。n 次独立且成功概率相同的试验，成功次数用二项分布，期望 np，方差 np(1-p)。
## 二项公式怎么理解
恰好 k 次成功：C(n,k)×p^k×(1-p)^(n-k)。组合数数成功位置，其余两项给一种顺序的概率。用户彼此有干扰或成功概率差异大时，简单二项模型可能不合适。
## 不放回抽取
有限总体中有固定成功数，不放回抽样的成功次数用超几何分布。抽后总体组成改变，不能机械把每次概率相乘成同一个 p。
''','from scipy.stats import binom, hypergeom\nprint("10 次、p=0.2，恰好 2 次：", binom.pmf(2, 10, 0.2))\nprint("至少 2 次：", binom.sf(1, 10, 0.2))\nprint("10 个中 3 个红球，抽 2 个都红：", hypergeom.pmf(2, 10, 3, 2))',engine='python',q='二项分布通常要求？',options=['固定次数、独立、相同成功概率','必须不放回','结果可以有任意连续金额'],explain='成功次数是离散值。')
add('stats','泊松、指数、均匀与正态分布','''
## 事件次数和等待时间
泊松分布常描述固定区间内事件次数，参数 λ 是平均次数，均值和方差都为 λ。独立增量、稳定速率等假设很重要；节假日波动明显时不能机械套用。齐次泊松过程的相邻等待时间服从指数分布，均值 1/λ，具有无记忆性。
## 均匀和正态
连续均匀分布在区间上密度相同。正态分布是对称钟形，由均值 μ 和标准差 σ 决定。标准化 Z=(X-μ)/σ；正态下约 68%、95%、99.7% 落在均值±1、2、3个标准差内。
## 选择模型看生成过程
订单金额常右偏，并不因为数据多就自动变正态。均匀用于等可能区间抽样，二项用于成败次数，泊松用于稀疏计数，指数用于特定过程的间隔；模型是近似，应用前检查假设。
''','from scipy.stats import poisson, expon, norm\nprint("每分钟平均 3 次，零次概率：", poisson.pmf(0, 3))\nprint("等待超过 1 分钟：", expon.sf(1, scale=1/3))\nprint("标准正态落在 ±1.96：", norm.cdf(1.96)-norm.cdf(-1.96))',engine='python',q='订单金额数据很多就一定正态吗？',options=['不一定','一定','只要金额非负就正态'],explain='原始分布与样本均值的抽样分布要区分。')
add('stats','大数定律、中心极限定理与标准误','''
## 大数定律告诉你平均趋向哪里
满足条件时，独立同分布样本的平均随着样本量增加接近期望，但单次样本不保证单调更接近，也不承诺下一次就补偿前面的偏差。
## 中心极限定理告诉你均值怎么波动
在合适条件下，标准化后的样本均值分布趋近正态；这不表示原始金额分布变成正态。重尾、相关、极小样本可能需要额外处理。
## 标准差与标准误
标准差描述个体差异；均值的标准误 SE≈s/√n 描述估计的不确定性。样本量扩大 4 倍，标准误约减半。相关数据的有效样本量比行数小，不能把每次点击都当独立用户。
''','import numpy as np\nrng = np.random.default_rng(42)\nfor n in [10, 100, 1000]:\n    means = rng.exponential(scale=10, size=(1000, n)).mean(axis=1)\n    print(n, "均值的标准差：", round(means.std(ddof=1), 3), "理论近似：", round(10/np.sqrt(n), 3))',engine='python',q='样本量扩大 4 倍，标准误大约？',options=['减半','减为四分之一','扩大四倍'],explain='标准误与样本量平方根成反比。')
add('stats','置信区间：报告估计的不确定性','''
## 不只给一个点
样本均值是点估计，置信区间给一个不确定性范围。常见结构是估计值 ± 临界值×标准误。已知总体标准差或适当大样本近似可用正态；未知方差的均值问题常使用 t 分布。
## 95% 的正确解释
若重复抽样并按同样方法构造区间，长期约 95% 的区间覆盖固定总体参数。对于已算出的这一个区间，频率学派不把它解释成固定参数有 95% 概率落在里面。
## 哪些因素使区间更宽
置信水平更高、波动更大、样本更少都会让区间变宽。二项比例接近 0 或 1、小样本时，简单正态 Wald 区间表现差，应考虑 Wilson 或精确方法，而不是硬套 1.96。
''','import numpy as np\nfrom scipy.stats import t\nx = np.array([10, 12, 9, 13, 11, 14, 8, 12])\nn = len(x)\nse = x.std(ddof=1) / np.sqrt(n)\nmargin = t.ppf(0.975, df=n-1) * se\nprint("均值：", x.mean(), "95% 区间：", (x.mean()-margin, x.mean()+margin))',engine='python',q='提高置信水平，其他条件不变，区间通常？',options=['更宽','更窄','不变'],explain='想让更多重复构造的区间覆盖参数，需要更大范围。')
add('stats','假设检验、p 值与两类错误','''
## 把一个主张放在可检验的位置
H0 是零假设，例如两组转化率相同；H1 是备择，例如不同。先定显著性水平 α、检验方向和方法，再看数据。统计量衡量观察结果偏离 H0 的程度。
## p 值是什么
在 H0 及模型假设成立时，得到当前这样或更极端统计量的概率。它不是“H0 为真的概率”，也不是“结果由随机性造成的概率”。p<0.05 不是效应大或值得上线的保证。
## 错误和功效
一类错误是 H0 真却拒绝，概率上限由 α 控制；二类错误是有指定真实效应却未拒绝，概率 β；功效 power=1-β。未显著不代表证明没有效果，可能区间太宽。
## 单侧还是双侧
只关心预先指定方向且允许不检验另一侧时可考虑单侧；如果上涨下跌都重要应双侧。不能看完方向才把双侧改成单侧追显著。
''','from scipy.stats import binomtest\nresult = binomtest(k=65, n=100, p=0.5, alternative="two-sided")\nprint("100 次正面 65 次，H0:p=0.5，p 值：", result.pvalue)',engine='python',q='p=0.03 的正确解读是？',options=['H0 及假设成立时，当前或更极端结果的概率约 3%','H0 为真概率 3%','业务收益一定是 3%'],explain='p 值是条件于零假设的尾部概率。')
add('stats','均值比较：z、t、配对与 Welch','''
## 先辨认样本关系
同一批用户改版前后是配对数据，可对每人的差值做单样本 t 检验；两批互不重叠用户是独立样本，不能误用配对检验。前后对比仍可能受时间趋势影响，统计检验本身不赋予因果性。
## t 和 z 不按 30 一刀切
总体方差已知的均值问题可用 z；未知时常用 t。样本量增大 t 逐渐接近正态。独立样本均值比较通常可考虑 Welch t，不强行假设两组方差相等。
## 检查假设
独立性、异常值、样本量和分布形态都影响可靠性。重尾数据可以结合合适的聚合单位、预先规定的处理、bootstrap 或稳健方法。不要为了显著随意删大额用户。
''','from scipy.stats import ttest_ind, ttest_rel\na = [10, 12, 9, 13, 11, 14]\nb = [12, 15, 10, 16, 13, 18]\nprint("独立样本 Welch：", ttest_ind(a, b, equal_var=False))\nprint("若确实是同一人前后配对：", ttest_rel(a, b))',engine='python',q='不知道两组方差相等，独立样本均值比较常可考虑？',options=['Welch t 检验','强行把观测配对','只比较总和'],explain='Welch 不要求两组总体方差相同。')
add('stats','比例、卡方、Fisher 与方差分析','''
## 两组转化率
每组独立用户是否转化是二元结果。样本充分时可用两比例 z 检验；在 H0 两比例相同时，标准误常使用合并比例。对效应差构造区间时常用不同的非合并方差，不能混用步骤。
## 分类变量关联
卡方独立性检验比较列联表的观察频数与独立假设下期望频数，输入应是人数，不是百分比。稀疏小样本的 2×2 表可考虑 Fisher 精确检验。它们检验关联，不自动证明因果。
## 三组以上
ANOVA 比较多个组均值，显著说明至少某组不同，并不告诉你哪一对。进一步成对比较需处理多重检验；方差不齐等条件下选择合适变体。非参数 Mann–Whitney 检验也有假设，并非通用“中位数检验”。
''','import numpy as np\nfrom scipy.stats import norm, chi2_contingency, fisher_exact\nn_a = n_b = 1000\nx_a, x_b = 100, 125\npool = (x_a+x_b)/(n_a+n_b)\nse = np.sqrt(pool*(1-pool)*(1/n_a+1/n_b))\nz = (x_b/n_b-x_a/n_a)/se\nprint("两比例双侧 p：", 2*norm.sf(abs(z)))\nprint("卡方：", chi2_contingency([[100,900],[125,875]], correction=False).pvalue)\nprint("小样本 Fisher：", fisher_exact([[1,9],[6,4]]).pvalue)',engine='python',q='列联表检验应输入？',options=['各格人数或频数','只输入百分比','均值和最大值'],explain='频数体现样本量，对不确定性至关重要。')
add('stats','相关、回归、混杂与预测','''
## 相关不等于因果
促销支出与销售额正相关，可能是促销起作用，也可能是旺季同时提高两者。影响处理和结果的第三个变量叫混杂因素。时间先后、相关强弱都不足以单独证明因果。
## 最简单的回归
y≈a+bx，a 是截距，b 是 x 增 1 时预测 y 的变化。最小二乘通过最小化残差平方和拟合。R² 描述模型在样本中解释的变异比例，不等于预测准确率，更不证明因果。
## 相关的几种形式
Pearson 衡量线性关系；Spearman 对排名看单调关系。离群点、范围受限、非线性都影响解读。回归推断要关注误差结构、异方差、相关观测和模型设定；预测还要在未参与训练的数据上评估。
''','import numpy as np\nfrom scipy.stats import linregress, spearmanr\nx = np.array([1,2,3,4,5])\ny = np.array([3,5,6,9,11])\nr = linregress(x,y)\nprint("斜率/截距：", r.slope, r.intercept)\nprint("R²：", r.rvalue**2)\nprint("Spearman：", spearmanr(x,y).statistic)',engine='python',q='回归系数显著可以单独证明因果吗？',options=['不可以','可以','只要 R² 高就可以'],explain='遗漏混杂或反向因果仍可能存在。')
add('stats','Bootstrap、置换与稳健性','''
## 用重抽样近似不确定性
Bootstrap 从已有样本中有放回抽取同样大小的样本，反复计算统计量，观察其分布。简单百分位区间取 2.5% 与 97.5% 分位；不是所有小样本或极端分布下都准确，复杂场景需更合适方法。
## 抽样单位要对
用户随机分流时，同一用户多条订单应一起抽取或先聚合到用户。直接按订单抽样会破坏相关结构，低估不确定性。Bootstrap 不能修复有偏样本或缺失关键人群。
## 置换检验在做什么
在可交换性等零假设条件下打乱组标签，比较真实统计量与随机标签统计量。它与有放回重抽样不同。随机种子、重复次数和预处理规则应记录，结果才能复现。
''','import numpy as np\nrng = np.random.default_rng(42)\nx = np.array([10,12,9,13,11,14,8,12])\nboot = rng.choice(x, size=(2000,len(x)), replace=True).mean(axis=1)\nprint("Bootstrap 均值区间：", np.quantile(boot,[0.025,0.975]))',engine='python',q='用户随机分流且一人多单，应优先按什么重抽样？',options=['用户','任意订单行','金额大小排序位置'],explain='保留随机化单位内部的相关结构。',advanced=True)

add('ab','AB 实验从一个业务问题开始','''
## 想知道改变带来的增量
“新版转化更高”可能是用户不同；AB 把合格用户随机分为对照和实验组，在相同时间比较。随机化让两组在期望上可比，减少混杂；具体样本仍会有随机差异。
## 一张实验卡
写明目标人群、要改什么、预期机制、主指标、护栏、随机化单位、分流比例、最小值得检测效应、样本量、结束规则和分析方法。先写卡，再收数。
## 一个例子
目标：减少新客结算页流失；处理：展示更清楚的运费；主指标：入组用户 7 日支付转化；护栏：投诉、退款、页面延迟。不能只在“点击过新版按钮”的用户中比较，因为点击本身受到处理影响。
''',q='为什么在看数据前确定实验卡？',options=['防止看结果后改变口径和判定标准','让所有实验必然显著','可以省略随机分流'],explain='事先约定减少选择性报告和追逐显著。')
add('ab','随机化单位、分流与干扰','''
## 用户、设备、店铺还是城市
处理施加给谁，就认真选择随机化单位。按用户分流时，同一用户应稳定分组；跨设备识别不一致可能污染实验。商家策略可能影响所有买家，不能总用买家级随机化。
## 不互相影响是假设，不是事实
实验组分享优惠给对照组、供给竞争、社交传播会产生干扰。可能需要商家/地区集群随机化或时间切换实验，并按对应单位做推断；集群相关会增加所需样本。
## 记录三种人群
被随机分配的人、实际触达的人、触发功能的人是不同集合。ITT 按原分配分析通常保留随机化优势。只分析实际触达者可能引入选择偏差，触发分析需预先定义且解释限制。
''',q='按用户分流时，统计标准误主要应尊重什么？',options=['用户级随机化和相关结构','订单总行数就是独立样本数','只看设备数'],explain='一个用户的多次行为不是多个独立分流单位。')
add('ab','指标：主指标、护栏与比率口径','''
## 把机制和收益串起来
主指标回答是否达到目标；机制指标解释过程，例如按钮点击；护栏监控副作用，例如退款率、延迟、投诉。先确定一个或少量主指标，不能事后从几十项中挑好看的。
## 人均与比率不同
人均收入 = 总收入 / 入组人数，应包含零消费用户。客单价 = 总金额 / 订单数。整体比率通常不是每用户比率的等权平均。处理可能同时改变分子与分母，需要联合看。
## 观察窗口成熟
入组后 7 日转化，最后一天入组的用户也要等满 7 天。只看实验结束时已经成熟的人群时，要预先规定截断方式，不应按结果选择等待天数。
## OEC 和局部指标
总体评价指标试图联系长期价值；一次点击提升不保证长期留存或利润提高。没有完美单指标，必要时给出收益—风险权衡。
''',q='人均收入的分母通常应包含零消费入组用户吗？',options=['应包含，除非事先另有明确目标口径','永远不包含','只包含点击按钮的人'],explain='删掉零消费用户会改变目标人群和指标含义。')
add('ab','MDE、样本量、功效与实验时长','''
## MDE 是规划参数
最小可检测效应 MDE 是希望有足够功效检测到的差异，不是保证能检测到的阈值，也不等于业务上最小值得做的收益。区分绝对差，如 10%→11% 的 1 个百分点，和相对提升 10%。
## 一个入门近似
独立二元结果、两组等量、双侧 α=0.05、功效 80%，当两比例接近 p 时，每组样本数近似 2×p(1-p)×(z(1-α/2)+z(power))²/δ²，δ 是绝对差。真实设计应用更合适的精确或软件计算，并考虑集群、分流和缺失。
均值差的同类近似为每组 n≈2σ²×(z(1-α/2)+z(power))²/δ²，其中 σ² 是单用户结果方差，δ 与指标同单位。二元结果把 σ² 换成 p(1-p) 就得到上面的公式。方差可以来自可比历史样本或试点，但错误方差估计会让规划偏离实际。
## 一定要 50:50 吗
不一定。两组方差和成本相近时，固定总样本的等量分配通常效率较高；风险、流量、处理成本或方差不同可采用不等比例。改变分配比例需相应调整样本量和标准误，不能沿用等量公式再把人数随意拆分。
## 样本量不等于天数
总样本除以每天合格且未重复计入的用户，才是粗略时长；还要覆盖业务周期、等观察窗成熟，考虑分流比例。不能每天累加重复 DAU 当独立新增样本。
## 直觉
想检测一半大小的差异，样本约需要四倍。预算不足时应诚实报告精度限制，而不是降低标准追显著。
''','import math\nfrom scipy.stats import norm\np = 0.10\ndelta = 0.01\nalpha = 0.05\npower = 0.80\nn = math.ceil(2*p*(1-p)*(norm.ppf(1-alpha/2)+norm.ppf(power))**2/delta**2)\nprint("近似每组样本：", n, "总样本：", 2*n)',engine='python',q='MDE 变为原来一半，近似样本需求？',options=['四倍','两倍','一半'],explain='样本量与绝对差的平方成反比。',task='改为希望检测 0.5 个百分点差异。',hint='delta=0.005。',lab='sample')
add('ab','AA、SRM 与实验可信性检查','''
## AA 检查实验系统
两组同样体验的 AA 实验用于发现分流、埋点、统计流程问题。一次显著不一定系统坏了，显著性水平本来容许少量一类错误；重复异常才值得排查。
## SRM 是样本比例异常
原计划 50/50，实际人数偏离远超随机波动时，可能存在分流、触发、日志、过滤问题。SRM 检验只检查分配比例，不等于所有协变量平衡，也不能证明实验有效。
## 排查顺序
看分配日志与分析表是否一致、是否丢数、是否某端版本缺失、机器人过滤是否组间不同、是否按受处理影响的条件筛人。先修可信性，再解读业务 p 值。
''','from scipy.stats import chisquare\nprint("5500/4500 对计划 5000/5000 的 SRM p：", chisquare([5500,4500], f_exp=[5000,5000]).pvalue)',engine='python',q='发现严重 SRM 后应该先？',options=['查分流和数据链路','直接宣布业务胜出','删掉多的一组人数凑齐'],explain='人为凑齐不能修复导致偏差的机制。')
add('ab','结果解读：效应、区间与业务收益','''
## 四个数字一起说
对照基准、实验结果、绝对差/相对提升、置信区间及 p 值。统计显著与业务显著分别回答“证据是否足够”和“收益是否值得”。大样本能把极小收益检测显著。
## 一个完整表述
对照 10%、实验 12%，差 2 个百分点、相对提升 20%；同时报告区间、样本和观察窗。不能只说“涨了 20%”让人误解为加 20 个百分点。
## 上线需要护栏
结合成本、退款、长期留存、处理覆盖率与可推广范围。非显著且区间很宽意味着仍不确定；非显著但区间窄且排除了有价值效应，可以支持“不值得继续”的判断。证明等效或不劣需专门设计。
''','import numpy as np\nfrom scipy.stats import norm\na,na = 1000,10000\nb,nb = 1200,10000\npa,pb = a/na,b/nb\ndiff = pb-pa\nse = np.sqrt(pa*(1-pa)/na + pb*(1-pb)/nb)\nprint("差：", diff, "相对提升：", diff/pa)\nprint("大样本近似 95% 区间：", (diff-1.96*se, diff+1.96*se))',engine='python',q='统计显著是否必然值得上线？',options=['不一定，还看收益成本与护栏','一定','只需看样本量'],explain='统计证据和商业决策不同。',lab='effect')
add('ab','反复偷看、多重检验与提前停止','''
## 每天看到显著就停会怎样
固定样本检验的 α 不是“每天随便看一次、显著就停”的整体错误率。重复观察和选择性停止通常增加误报。可以监控安全风险，但正式效果判定按预设结束规则。
## 很多指标总有一个碰巧显著
同时比较多个版本、多个指标和很多分组时，家族错误率或假发现率需要控制。Bonferroni 简单保守，Holm 控制家族错误率，BH 常用于控制假发现率，选择取决于目标与假设。
## 正确的提前停止
若确需连续决策，预先采用合适的序贯设计、alpha spending 或始终有效的推断方法。不是简单把阈值改成更小就解决所有问题。
''','import numpy as np\nfrom scipy.stats import false_discovery_control\npvalues = np.array([0.001,0.01,0.03,0.2,0.6])\nprint("Bonferroni 调整：", np.minimum(pvalues*len(pvalues),1))\nprint("BH 调整：", false_discovery_control(pvalues,method="bh"))',engine='python',q='每天看，第一次 p<0.05 就停止，与预定一次检验相同吗？',options=['不同，误报控制会改变','相同','只要没换代码就相同'],explain='决策规则也是统计设计的一部分。')
add('ab','长尾、比率、异常值与 CUPED','''
## 收入长尾怎么处理
先确认大额是真实用户还是数据错误。真实大客是业务的一部分，不能只因为影响 p 值而删除。预先规定截尾或 winsorize 会改变估计目标，要同时报告原始口径或解释影响。
## 比率指标的方差
客单价是总收入/总订单，分子分母相关，不能当两个独立均值随意除。可用符合随机化单位的 delta method、bootstrap 等估计不确定性。先按用户组织数据，保留零订单者的口径。
## CUPED 的直觉
用实验前与结果相关的协变量去解释一部分噪声，从而降低方差；调整形如 Y-θ(X-E[X])，θ 常与 Cov(X,Y)/Var(X) 有关。X 应不受本次处理影响，数据可用性、估计方式和新用户缺失要处理。
它不能挽救分流错误、干扰或事后筛人，也不会凭空制造真实效果。
''',q='用本次实验后的点击量直接当 CUPED 协变量有何风险？',options=['点击可能受处理影响，破坏解释','没有风险','可以保证所有结果显著'],explain='常用安全起点是处理前的预测性信息。',advanced=True)
add('ab','异质性、新奇效应与长期观察','''
## 平均有效不等于人人有效
新老客、渠道、地区可能效果不同。分组应有业务机制和预设优先级，检查交互效应；“A 组显著、B 组不显著”不直接证明 A 与 B 的效果差异显著。
## 时间也会改变行为
新版最初因新鲜感提高点击，后来衰减；用户学习成本也可能造成前低后高。覆盖合理周期、查看分期趋势和长期留存，但不要事后只挑最好的一周。
## 决策和推广
目标样本、上线人群和实验季节不同，外推要说明限制。长期 holdout 能观察长期影响，成本和伦理、业务约束需要权衡。一次实验是积累证据的一步。
''',q='A 显著、B 不显著，能直接说两组效果不同吗？',options=['不能，应检验效果差异或交互','能','只看谁 p 值小'],explain='显著性差异不等于差异的显著性。',advanced=True)
add('ab','不能随机时：DID、匹配与因果边界','''
## 前后对比为什么不够
活动后销售上升可能源于节假日、竞争变化或用户组成。反事实是“同一对象如果没接受处理会怎样”，现实看不到，需要设计或假设帮助识别。
## DID 的核心计算
双重差分 = (实验群后-前) - (对照群后-前)。关键假设包括无处理时趋势平行、没有差异化同期冲击等；实验前趋势相近是有用证据，但不能证明未来平行。
## 其他方法知道在解决什么
匹配/倾向得分尽量平衡已观测混杂，无法保证消除未观测混杂；RDD 利用阈值附近的可比性，需要不能精确操纵等条件；工具变量需要相关性和排除限制等强假设。别把方法名称当因果证明。
''','treat_before,treat_after = 100,130\ncontrol_before,control_after = 80,95\ndid = (treat_after-treat_before)-(control_after-control_before)\nprint("DID 估计：",did)',engine='python',q='DID 最核心的识别假设之一是？',options=['无处理时两组趋势平行','两组水平必须完全相等','样本大就无需假设'],explain='差分消除固定水平差异，但不能自动消除不同趋势。',advanced=True)

add('business','电商指标地图：GMV 不是利润','''
## 一条购买链路
曝光 → 点击/访问 → 商品浏览 → 加购 → 下单 → 支付 → 履约 → 退款/复购。每个节点都要定义人数、次数和时间窗口；UV 是去重用户，PV 是浏览次数，DAU 是日活用户而不是登录次数。
## 常用指标公式
支付 GMV = 支付订单金额和（退款等口径另约）；AOV=GMV/订单数；ARPU=收入/全部目标用户；ARPPU=收入/付费用户。收入不一定等于 GMV，平台可能按佣金或服务收入确认。
## 从规模走到收益
利润需要扣除相关成本，毛利、贡献利润、净利润口径不同。补贴换来 GMV 上升不自动意味着赚钱。客单价高也可能来自小额用户流失，要联看用户数、频次和结构。
## 建指标字典
每个指标写名称、业务目的、公式、粒度、时间字段、过滤、去重键、刷新时间和负责人。面试先讲这些口径，比只背缩写有用。
''',q='GMV 上升能直接推出利润上升吗？',options=['不能，还需收入、退款和成本','能','只要订单数增长就能'],explain='交易规模与实际收益不同。',lab='gmv')
add('business','指标拆解：把“大盘下降”拆成问题','''
## 先找恒等式
GMV = 购买用户数 × 人均订单数 × 客单价；也可写为访问用户数 × 用户购买转化率 × 人均订单数 × 客单价。因子定义必须保证乘积真能还原总量。
## 两因素贡献怎么计算
对于 G=A×B，一种顺序拆解是 ΔG=(A1-A0)×B0 + A1×(B1-B0)。先改 A 后改 B，会与反向顺序分配不同，因为存在交互项。可以用对称分摊，但必须说明方法。
## 从代数到业务
先找到变化最多的因子，再按新老客、渠道、地区、品类、终端、价格带分层；比较绝对贡献和相对变化。小盘翻倍可能贡献小，大盘下降 1% 可能影响大。
''','a0,b0 = 1000,100\na1,b1 = 900,110\ndelta_a = (a1-a0)*b0\ndelta_b = a1*(b1-b0)\nprint("A 贡献：",delta_a,"B 贡献：",delta_b)\nprint("合计：",delta_a+delta_b,"实际变化：",a1*b1-a0*b0)',engine='python',q='贡献拆解需要说明方法的原因是？',options=['交互项分配可能依赖顺序','任何公式都不可能相加一致','只要报百分比就够了'],explain='代数恒等不自动给出唯一因果归因。',lab='gmv')
add('business','异常波动：先查数，再找业务原因','''
## 第一步确认异常真的存在
核对埋点、数据延迟、口径变更、去重和时区；对比同星期、同期时段和节假日。不要拿今天半天对昨天全天。阈值、同比、环比、基于历史波动的区间各有适用场景。
## 第二步定位范围
全站还是某渠道？所有端还是某版本？新客还是老客？量下降还是率下降？按可解释维度拆解，优先看对总量贡献最大的部分，不是只看相对跌幅。
## 第三步列证据链
假设支付故障：应见支付成功率下降、错误码上升、特定版本集中；假设投放减少：流量减少而后链路转化可能稳定。每个假设写出可证伪的预期数据。
## 第四步行动与验证
给临时止损、进一步实验或产品改进，并设恢复指标、负责人和观察窗口。面试用“结论—证据—限制—行动”，不要只列十种可能原因。
''',q='GMV 突然下降，第一步通常是？',options=['确认数据完整性和比较口径','立刻说竞争对手降价','先上线更大补贴'],explain='数据链路问题可能伪装成业务异常。')
add('business','漏斗、留存、复购与 cohort','''
## 三种问题分别回答什么
漏斗看流程哪里流失；留存看一批用户后来是否回来；复购看买过的人是否再次购买。人群、行为、时间窗不同就不能横比。
## cohort 表怎么看
行是同一周入组用户，列是入组后第几周，单元格是留存率。较新的 cohort 后面还没发生的时间应留空，不能填零；对比相同用户年龄，才不把自然成熟误认为质量差。
## 提升路径
拉新质量、首购体验、供给匹配、履约、客服、优惠到期和习惯形成都可能影响留存。先分层定位，再提出能验证的机制，避免万能“发券”。
## 流失预警
定义多久未回访才叫流失，结合业务购买周期；买冰箱与买生鲜不能用同一周期。提升回访率同时观察利润与退订投诉。
''',q='新 cohort 尚未经历的第 8 周应填什么？',options=['未成熟/不可观察','0%','上周留存复制过去'],explain='未观察到不等于发生流失。')
add('business','RFM、用户分层与生命周期','''
## R、F、M 是什么
Recency：距最近购买多久；Frequency：观察窗内购买频次；Monetary：观察窗内消费金额。R 越小通常越近期，F/M 越大通常越活跃或价值高；分层方向要写清。
## 如何分层才有用
确定观察日与窗口，计算一人一行特征，再用业务阈值或分位数分组。小样本、并列和长期零购买用户需要处理。RFM 是行为描述，不自动等于终身价值，也不是因果模型。
## 分层要连行动
高价值近期活跃者重体验；高价值久未回访者查流失原因；新客看首购障碍；低价值群体注意服务成本。策略效果用随机实验检验，不凭标签决定人群天生好坏。
''',"SELECT user_id,DATEDIFF('2026-04-01',MAX(DATE(order_at))) AS recency_days,COUNT(*) AS frequency,SUM(amount) AS monetary FROM orders WHERE status='paid' AND order_at<'2026-04-01' GROUP BY user_id ORDER BY user_id;",q='RFM 的 R 越大通常意味着？',options=['距离最近购买越久','最近购买越近','消费金额越高'],explain='这里 R 定义为距最近购买天数。')
add('business','ROI、ROAS、CAC、LTV 与补贴','''
## 指标同名也可能异义
ROAS 常是归因收入/广告支出；ROI 常表达净收益/投入，但业务中有人混用，因此先问定义。CAC 是获客成本，明确新增客户是谁、自然新增如何分摊。LTV 是生命周期价值估计，不应直接拿累计 GMV 充当利润 LTV。
## 归因收益不等于增量
看到广告后购买的人可能本来就会买。平台归因 ROAS 高不保证增量收益高。随机留出对照或合适因果方法能帮助估计增量，并说明不确定性。
## 补贴算账
增量贡献 = 增量收入对应毛利 - 新增补贴 - 额外履约/服务成本等。还要考虑原本会买的人获得补贴、活动间蚕食、提前囤货导致后续回落。
## LTV 预测
需要留存、购买频次、利润率和时间价值假设，分 cohort 回测。短观察窗外推很长未来时不确定性高，报告范围和敏感性，而不是一个精确神奇数字。
''',q='广告归因订单是否全部是广告带来的增量？',options=['不是，有些本来就会购买','是','只有首单才必定增量'],explain='归因规则和反事实增量是不同概念。')
add('business','渠道归因、增长与选择偏差','''
## 把路径和效果区分开
首触、末触、线性多触点都是分配归因功劳的规则。规则能用于报表，但不能独立证明某渠道的因果贡献。跨设备、隐私限制和窗口定义会造成观察缺口。
## 增长是完整链路
拉新 → 激活 → 留存 → 收益 → 传播，每一环都有分母。低价流量如果不留存、退款高，未必是好增长。比渠道时要控制新老客结构、地区、时间和活动差异。
## 常见偏差
把点击人群与未点击人群直接比较会混入原始意愿；只分析成功下单者忽略漏斗前流失；只选高增长门店可能均值回归。能随机留出就优先设计实验，否则明确观察性限制。
''',q='末次点击归因主要回答？',options=['按规则把订单归给谁','谁一定造成了增量','所有未点击者不会买'],explain='归因规则不是因果识别。')
add('business','供给、价格、履约与电商案例','''
## 数分要理解两端
买家需要商品、价格、体验；商家关心流量、成交、利润、履约。销量下降可能是需求不足，也可能缺货、配送限制或商家退出。只盯点击和转化会漏掉供给问题。
## 价格与弹性
价格弹性常表达需求量相对变化 / 价格相对变化，局部近似有条件。历史价格通常不是随机设置，促销和季节会混杂；关联弹性不能直接当因果弹性。
## 三个练习场景
券额加大但利润下降：拆新增购买与原有购买补贴、客单价、毛利、退款。支付转化提升但留存下降：查用户结构、质量和体验。低价商品流量高但缺货：联看可售率、履约与缺货损失。
## 回答方法
先澄清目标与约束，再给指标树、可验证假设、所需数据、实验方案和最终决策标准。不要假装知道公司内部未公开指标阈值。
''',q='销量下降是否只能归因需求？',options=['还可能是供给、库存、履约等','只能是需求','只看广告即可'],explain='电商结果由需求与供给共同决定。')
add('business','数据报告、可视化与结论表达','''
## 图表服务一个问题
趋势用折线，类别比较用条形，分布用直方图/箱线，关系用散点，cohort 用热力图。柱图截断纵轴可能夸大差异，双轴图尤其需要谨慎。不要为好看堆饼图。
## 结论必须有证据量级
“本周支付金额下降 8%，主要来自渠道 A 访问人数减少；支付率基本稳定”比“表现不佳”具体。写明比较期、口径、样本、数据完整性及误差，不把相关写成导致。
## 一页报告结构
决策问题 → 关键结论 → 两三条证据 → 不确定性 → 行动与验证。图题最好直接表达发现，但不能超出证据。附表留复现口径与代码版本。
''',q='讲结论时最有用的结构是？',options=['发现、证据、限制、行动','只放大量截图','只说 p 值'],explain='分析的目的包括帮助采取可验证的行动。')
add('business','项目深挖与手撕 SQL 的口头表达','''
## 项目讲真实贡献
介绍项目时，说明背景和目标、你的角色、使用的数据、分析方法、结果和后续行动，也要能解释方法的局限。如果暂时没有实际项目经历，可以使用本讲义的模拟电商数据完成一个练习项目，例如分析各渠道的订单数量和支付金额；介绍时如实说明这是练习项目。
## 面试常追问
为什么选该指标？分母是谁？数据质量怎么验？为什么不用另一种方法？有没有对照？你的贡献是什么？如果结果不显著怎么办？优先准备能落到代码和证据的回答。
## 手撕 SQL 的节奏
先复述粒度、时间窗、去重与并列规则；写 CTE 草稿，每层一句用途；用两三行手算验证；最后说边界与性能。忘记函数名可先表达逻辑，再补语法，不要安静乱试。
''',q='练习项目可以包装成真实公司业务成果吗？',options=['不应，说明是练习并展示扎实方法','可以随意编数字','只要能背下来就可以'],explain='真实可解释的分析比虚构经历更可持续。')

add('tools','Excel、BI、CSV 与数据交付','''
## Excel 仍然是常用协作工具
先掌握筛选、排序、透视表、SUMIFS/COUNTIFS、XLOOKUP 或查找组合、日期与文本清洗。透视表的求和/计数设置和空值处理要检查；手工改表容易丢复现记录。
## BI 的三层
数据连接与刷新、数据模型及关系、指标和可视化。星型模型把交易事实与用户/商品/日期维度分开；一对多关系方向和重复键会影响结果。看板要有更新时间、口径和异常提醒。
## CSV 与编码
CSV 是文本表，不保存可靠的列类型、公式和样式；身份证、编号前导零可能在打开时丢失。日期、货币和 UTF-8 编码要确认。读取不可信文件先检查列和类型，导出共享数据注意最小必要范围。
## 本讲义的文件方式
浏览器用于运行与自测；Markdown 用于 VS Code 阅读；Notebook 用于逐格执行；SQL/Python 源文件便于后续自己改。不会生成 Word 或 PDF。
''',q='导出 CSV 是否自动保留所有 Excel 类型和样式？',options=['不会，它主要是文本数据','会','只要文件名中文就会'],explain='类型和格式需要单独管理。')
add('tools','机器学习全景：监督、无监督与泄漏','''
## 先问是解释、预测还是因果
回归预测数值，例如收入；分类预测类别/概率，例如流失；聚类寻找相似群体；降维提取低维表示。预测准确不代表发现了因果机制，聚类也不自动产生有业务意义的客群。
## 训练、验证、测试
训练集拟合参数，验证集调参，最终测试集保留作评估。时间任务按时间切分，用户多行数据应避免同用户跨集合泄漏；交叉验证应尊重数据生成结构。
## 最危险的是未来信息
预测下周是否流失时使用下周订单数，是标签泄漏。标准化、缺失填充、特征选择也应仅在训练数据上拟合，再用于验证测试。Pipeline 有助保持步骤正确。
## 先做基线
与简单规则、历史平均或多数类别比较；记录版本、指标、置信度、训练数据窗口和线上漂移。不要一上来就复杂模型。
''',q='预测未来流失时可以用未来订单数当特征吗？',options=['不能，这是信息泄漏','可以提升准确率就行','只要隐藏列名就行'],explain='模型上线时无法得到未来信息。',advanced=True)
add('tools','回归、分类指标与过拟合','''
## 模型需要理解的层次
线性回归预测连续值；逻辑回归通过 sigmoid 把线性组合映射到概率，并不是预测连续目标的普通回归。树能表达非线性和交互；随机森林、梯度提升集成多棵树，仍需控制复杂度和验证。
## 分类指标
Precision=TP/(TP+FP)，Recall=TP/(TP+FN)，F1 是二者调和平均。正例少时 accuracy 可能很高却毫无用处；ROC-AUC 衡量排序的一种表现，PR 曲线常更直接关注稀少正例。阈值决定业务漏报与误报成本，概率还需校准。
## 回归与过拟合
MAE 是绝对误差均值，RMSE 更惩罚大误差。训练好测试差是过拟合信号；正则化、降低复杂度、更多合适数据可改善。偏差—方差权衡不是越复杂越好，不能反复在测试集上挑模型。
''','from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix\ny_true = [0,0,0,1,1,1]\ny_pred = [0,0,1,0,1,1]\nprint(confusion_matrix(y_true,y_pred))\nprint("精确率/召回/F1：",precision_score(y_true,y_pred),recall_score(y_true,y_pred),f1_score(y_true,y_pred))',engine='python',q='正例极少时只看 accuracy 有什么问题？',options=['全预测负例也可能很高','一定等于召回率','无法计算'],explain='指标要与业务代价和类别结构相符。',advanced=True)
add('tools','聚类、特征缩放、时间序列与推荐','''
## 聚类不是自动用户运营方案
K-means 按距离分簇，需选 K，对尺度和离群点敏感，偏好某类簇形状。先理解特征与标准化，再看稳定性、轮廓系数和可解释性；不能只追数学评分。
## 时间序列
趋势、季节性、节假日、噪声和自相关影响预测。按时间留出未来数据，滚动验证；用上周同日/移动平均做基线。随机打乱时间切分可能泄漏未来信息，预测区间比只报点预测更诚实。
## 推荐与搜索了解层
召回找候选、排序预测相关性或价值、多样性和约束影响最终展示。离线指标改善不保证线上收益，位置偏差与曝光选择会影响训练。冷启动、反馈循环是常见问题。
以上属于岗位要求中“数据挖掘”补充，不应抢占零基础的 SQL、统计与业务学习时间。
''',q='时间预测评估为什么通常不用随机切分？',options=['要模拟用过去预测未来，避免泄漏','随机切分一定更慢','时间没有相关性'],explain='评估应与上线使用方式一致。',advanced=True)
add('tools','Hadoop、Spark、数仓与工程常识','''
## 为什么一台电脑不够
海量数据需要分布式存储和计算。HDFS 将文件分块存储并管理副本；YARN 管理集群资源；MapReduce 是分阶段批处理模型。Spark 提供分布式计算，DataFrame/Spark SQL 常用于分析，执行会形成任务图。
## Spark 常见词的含义
惰性计算表示转换通常先记录计划，action 才触发执行；shuffle 是按键重分布数据，可能很贵；数据倾斜是少数键占太多记录，导致某些任务拖慢；cache 用空间换重复计算，但不总是有利。
## 数仓不是随便堆表
事实表记录交易/事件，维度表描述用户/商品等。分区减少扫描范围，列式 Parquet/ORC 适合分析读取；ETL/ELT 组织抽取、转换与加载。增量任务要考虑迟到数据、幂等和回补。
## 数据质量和协作
记录表的粒度、血缘、刷新依赖、主键唯一性、空值率和金额对账。版本管理保存代码与口径变更；只使用获授权的数据，分享时减少个人信息。JD 中 Hadoop/Spark 是加分项，先做到能解释用途，再安排真实集群实践。
''',q='Spark 中 shuffle 通常是？',options=['按键在节点间重新分布数据','随机打乱网页颜色','把所有代码变成单线程'],explain='连接、分组等操作可能引发网络与磁盘开销。',advanced=True)
add('path','零基础学习路线与每日复盘','''
## 先走通，不平均分配时间
第一轮：起点全部 → SQL 1—14 → Python 1—6 → 统计 1—12 → AB 1—7 → 业务 1—4。第二轮：窗口函数、留存、连续、滚动 → 其余统计与业务 → 工具进阶。这里的编号与左侧目录一致。
## 一份十一天紧凑安排示例
第 1—3 天：表、筛选、聚合、连接，数学比例与描述统计。第 4—6 天：窗口、日期、留存、连续、概率与检验。第 7—9 天：SQL 综合、AB 和业务拆解。第 10 天：有反馈的模拟。第 11 天：错题重做、边界复盘、轻量回顾与设备准备。
这不是保证十一天熟练的承诺。每天可用时间未知；若每天不足约两三小时，优先保证 SQL 核心与统计概念，进阶章延后。不要为赶目录跳过基础。
## 一次学习 30—50 分钟
读一节 → 自己解释 → 运行 → 修改 → 自测 → 写一句错误原因。第二天先不看答案重做。网页“我理解了”只是你的自评，不代表系统已经认证掌握。
''',q='零基础遇到连续两节不懂应？',options=['回到前置概念并做小例子','继续硬刷困难题','只背答案'],explain='复习前置知识通常比继续堆新知识更有效。')
add('path','从讲义过渡到题库和模拟面试','''
## 练习是第二步
完成筛选聚合连接后，先做配套的基础练习；窗口日期章后进入留存、连续、滚动练习。先不限时并允许提示，再减少提示，最后限时。练习目录只记录题名和出处链接，不代表所有题面都已离线保存。
## 一次带练怎么进行
你可以告诉我“按讲义 sql-10 带我学”。我先读你的笔记，问一个诊断小问题，只给必要提示；你交 SQL 或解释后，我用边界数据指出具体问题，再出一题变式。不要一开始直接给完整答案。
## 面试阶段怎么继续
结合目标岗位的描述与近期面试反馈调整复习重心。助手不会永久记住历史对话；需要持续上下文时，把笔记与记录文件放在同一目录，新会话开始时先读它们。
## 正式考核的边界
不同岗位的考核形式差别很大，时长、题型、是否允许查资料都以当次通知为准，本讲义不承诺任何具体形式。学习过程中可以查资料求助；正式独立考核时遵守当场规则。
''',q='练习目录是否等于所有题面都已离线保存？',options=['不是，目录只记录题名和出处链接','是','目录可以替代全部练习'],explain='原创练习和外部题单索引是两件不同的事。')
add('path','知识边界、来源与下一阶段','''
## 本讲义覆盖的范围
从数据与数学起点，覆盖 MySQL 8.0 查询和手撕专题、Python/Pandas、概率统计、AB/因果、数据质量、电商指标、业务案例、项目表达，以及数据挖掘和 Hadoop/Spark 概念。每章自测与可运行例子让抽象概念能被检查。
## 仍需要实践的内容
真实生产数据库权限/运维、大规模 Spark 集群调优、完整机器学习项目、复杂实验统计理论不可能靠一份入门讲义穷尽。本讲义提供入口和常见面试概念；学会基础后再按岗位反馈加深。
## 来源怎样使用
讲解和练习为本次原创教学内容，技术口径参考官方文档；面试题只用来安排学习优先级，不当作必考承诺。公式注明近似假设，默认代码会保存本机执行验证记录。预期输出与实时结果分别显示。
## 下一步
从第一课点运行即可。遇到错误保留代码、错误文字和你期待的结果，发给我时标明课号。以后我们依据你真实答题表现更新学习记录，不能仅因资料已经齐备就把进度标成完成。
''',q='这份讲义的“覆盖”意味着？',options=['覆盖约定的学习范围，仍需练习与按反馈深化','保证所有题都会考到','读完无需练习'],explain='完整路线与真正掌握是不同的事。')

def pretty_sql(code):
 # Insert only whitespace outside quoted strings; SQL meaning is unchanged.
 pattern=r"'(?:''|[^'])*'|--[^\n]*|\b(?:SELECT|FROM|WHERE|GROUP BY|HAVING|ORDER BY|LEFT JOIN|JOIN|UNION ALL|UNION|LIMIT)\b|[(),;]"
 depth=0;parts=[];pos=0
 for match in re.finditer(pattern,code):
  token=match.group();parts.append(code[pos:match.start()]);pos=match.end()
  if token.startswith("'") or token.startswith('--'):parts.append(token)
  elif token=='(':parts.append(token);depth+=1
  elif token==')':depth=max(0,depth-1);parts.append(token)
  elif token==',':parts.append(',\n  ' if depth==0 else ',')
  elif token==';':parts.append(';\n')
  else:parts.append('\n'+'  '*min(depth,3)+token)
 parts.append(code[pos:]);result=''.join(parts)
 return '\n'.join(x.rstrip() for x in result.splitlines() if x.strip()).strip()

def build():
 expected_file=ROOT/'data/default_outputs.json'
 outputs=json.loads(expected_file.read_text(encoding='utf-8')) if expected_file.exists() else {}
 for item in lessons:
  if item['engine']=='sql' and item['code']:item['code']=pretty_sql(item['code'])
  if item['id'] in outputs:item['expected']=outputs[item['id']]
 data={'title':'数分起点','version':'2026-09-30','modules':[{'id':i,'title':t} for i,t in modules],'lessons':lessons,'tables':json.loads((ROOT/'data/fixtures.json').read_text(encoding='utf-8'))}
 (ROOT/'lessons.js').write_text('window.BOOK = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
 (ROOT/'程序/curriculum.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 index=['# 零基础互动讲义 · Markdown 导航','优先双击 `启动讲义.cmd` 使用运行、自测和交互图；下面文件可直接用 VS Code 阅读。','']
 coverage=['# 知识点覆盖矩阵','范围：数据分析入门与面试常见考点。并不声称穷尽所有可能面试问题。','', '| 课号 | 主题 | 阶段 | 可执行示例 |','|---|---|---|---|']
 fixtures=json.loads((ROOT/'data/fixtures.json').read_text(encoding='utf-8'))
 cols={'users':['user_id','signup_date','channel','city'],'orders':['order_id','user_id','order_at','amount','status','category'],'logins':['login_id','user_id','login_at'],'events':['event_id','user_id','event_at','event_type'],'assignments':['user_id','arm'],'calendar':['dt']}
 prelude='import pandas as pd\n'+ '\n'.join(f'{k.removeprefix("da_")} = pd.DataFrame({repr(v["rows"])}, columns={repr(cols[k.removeprefix("da_")])})' for k,v in fixtures.items())+'\n'
 (ROOT/'代码示例/_lecture_data.py').write_text(prelude,encoding='utf-8')
 init=(ROOT/'代码示例/00_初始化_MySQL8.sql').read_text(encoding='utf-8')
 init=re.sub(r'^--[^\n]*','-- 本讲义专用模拟数据；会重建 da_beginner_lab 中的六张教学表。',init,count=1)
 # The scratch table is appended below; drop any earlier copy so repeated builds stay identical.
 init=re.sub(r'(?:\s*DROP TABLE IF EXISTS scratch;.*)\Z','',init,flags=re.S)
 # Standalone SQL data: replace only explicit table identifiers, preserve user data.
 for name in fixtures:init=re.sub(r'\b'+name+r'\b',name.removeprefix('da_'),init)
 init=re.sub(r'CREATE DATABASE[^;]*;','CREATE DATABASE IF NOT EXISTS da_beginner_lab CHARACTER SET utf8mb4;',init,flags=re.I)
 init=re.sub(r'USE\s+\w+\s*;','USE da_beginner_lab;',init,flags=re.I)
 (ROOT/'代码示例/00_初始化_MySQL8.sql').write_text(init+'\nDROP TABLE IF EXISTS scratch;\nCREATE TABLE scratch(id INT PRIMARY KEY,amount DECIMAL(12,2));\nINSERT INTO scratch VALUES(1,10),(2,20);\n',encoding='utf-8')
 notebooks={}
 for mid,title in modules:
  folder=ROOT/'讲义Markdown'/title
  folder.mkdir(parents=True,exist_ok=True)
  index+=['## '+title,'']
  for x in [y for y in lessons if y['module']==mid]:
   filename=x['id']+'_'+re.sub(r'[\\/:*?"<>|]','_',x['title'])+'.md'
   relative=f'{title}/{filename}'
   index.append(f'- [{x["id"]} {x["title"]}]({relative.replace(" ","%20")})')
   coverage.append(f'| {x["id"]} | {x["title"]} | {"面试进阶" if x["advanced"] else "基础/核心"} | {x["engine"] if x["code"] else "概念自测"} |')
   body=f'# {x["id"]} · {x["title"]}\n\n'+x['body']+'\n'
   if x['code']:
    body+=f'\n## 可运行例子\n\n```{x["engine"]}\n{x["code"]}\n```\n\n网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。\n'
    ext='sql' if x['engine']=='sql' else 'py'
    export=x['code'] if ext=='sql' else 'from _lecture_data import *\n\n'+x['code']
    (ROOT/'代码示例'/f'{x["id"]}.{ext}').write_text(export+'\n',encoding='utf-8')
    if ext=='py':
     notebooks.setdefault(mid,[]).extend([{'cell_type':'markdown','metadata':{},'source':(f'# {x["id"]} {x["title"]}\n\n'+x['body']).splitlines(True)},{'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':x['code'].splitlines(True)}])
   if x['task']:body+=f'\n## 动手改一处\n\n{x["task"]}\n\n提示：{x["hint"]}\n'
   if x['solution']:body+=f'\n<details><summary>参考改法</summary>\n\n```{x["engine"]}\n{x["solution"]}\n```\n\n</details>\n'
   q=x['quiz']
   body+='\n## 自测\n\n'+q['q']+'\n\n'+'\n'.join(f'{i+1}. {v}' for i,v in enumerate(q['options']))+f'\n\n<details><summary>答案与解释</summary>\n\n答案：{q["answer"]+1}。{q["explain"]}\n\n</details>\n'
   if x.get('expected'):body+='\n## 本机验证时的预期输出\n\n```json\n'+json.dumps(x['expected'],ensure_ascii=False,indent=2)+'\n```\n'
   (folder/filename).write_text(body,encoding='utf-8')
 for mid,cells in notebooks.items():
  book={'cells':[{'cell_type':'markdown','metadata':{},'source':['# 运行说明\n先执行下面初始化单元，再逐个执行课程单元。选择已安装 pandas/NumPy/SciPy/scikit-learn 的 Python 内核。']},{'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':prelude.splitlines(True)}]+cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'nbformat':4,'nbformat_minor':5}
  # Stable cell IDs are required by modern notebook format.
  for i,c in enumerate(book['cells']):c['id']=f'{mid}-{i:03}'
  (ROOT/'代码示例'/f'{mid}_逐格运行.ipynb').write_text(json.dumps(book,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'讲义Markdown/README.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
 (ROOT/'知识点覆盖矩阵.md').write_text('\n'.join(coverage)+'\n',encoding='utf-8')
 print(json.dumps({'lessons':len(lessons),'sql_examples':sum(x['engine']=='sql' and bool(x['code']) for x in lessons),'python_examples':sum(x['engine']=='python' and bool(x['code']) for x in lessons)},ensure_ascii=False))
if __name__=='__main__':build()
