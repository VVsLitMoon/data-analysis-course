# sql-01 · 第一条查询：SELECT、FROM 与别名

## 把中文问题翻译成 SQL
问题是“查看用户编号和所在城市”。SELECT 后面列出想看的列，列之间用英文逗号；FROM 后面写表名。AS 给输出列起一个便于阅读的新名字，不会修改原表。
## 按顺序读代码
第一行选择 user_id 和 city，第二行说明从 users 获取。SQL 关键字不要求大写，但统一大写便于区分。字符串用单引号，例如 '上海'；数字一般不加引号。-- 后面是注释，不执行。
## 常量也能被查询
SELECT 2 * 3 不需要表；有 FROM 时，常量通常在每一行重复出现。不要把列名写成 'user_id'，那会把固定文字当结果。

## 可运行例子

```sql
SELECT user_id AS id,
   city AS user_city
FROM users;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

把输出增加一列 channel。

提示：在列清单里加英文逗号和列名。

<details><summary>参考改法</summary>

```sql
SELECT user_id AS id, city AS user_city, channel FROM users;
```

</details>

## 自测

SELECT 'city' FROM users 得到什么？

1. 每人的城市
2. 必定报错
3. 每行都是 city 这个文字

<details><summary>答案与解释</summary>

答案：3。单引号包住的是字符串，不是列引用。

</details>
