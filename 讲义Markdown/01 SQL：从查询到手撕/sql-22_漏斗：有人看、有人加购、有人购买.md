# sql-22 · 漏斗：有人看、有人加购、有人购买

## 漏斗是按路径看流失
浏览 → 加购 → 支付。宽松口径可以只要求同一用户各事件出现过；严格漏斗还要求时间先后、同一会话或规定窗口。三种事件人数直接相除，不一定是路径转化。
## 先做最容易解释的一种
本例统计 1 月 1 日“当天有各事件”的用户数，不要求顺序，所以明确叫事件覆盖，不称严格有序漏斗。条件 COUNT(DISTINCT ...) 让一个用户多次浏览只算一次。
## 严格漏斗怎么延伸
先确定每用户第一个浏览，再找浏览之后第一个加购，再找加购之后的支付，规定窗口和相同业务对象。不能只取所有事件的独立最早时间：最早加购在浏览前时，之后的有效加购可能被漏掉。

## 可运行例子

```sql
SELECT COUNT(DISTINCT CASE WHEN event_type='view' THEN user_id END) AS viewers,
  COUNT(DISTINCT CASE WHEN event_type='cart' THEN user_id END) AS cart_users,
  COUNT(DISTINCT CASE WHEN event_type='pay' THEN user_id END) AS pay_users
FROM events
WHERE event_at>='2026-01-01' AND event_at<'2026-01-02';
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

每个事件都出现过是否保证有序漏斗？

1. 保证
2. 只要人数一样就保证
3. 不保证，还需事件时间顺序

<details><summary>答案与解释</summary>

答案：3。有的用户可能先支付后浏览。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "viewers",
        "cart_users",
        "pay_users"
      ],
      "rows": [
        [
          "5",
          "3",
          "2"
        ]
      ],
      "total": 1
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
