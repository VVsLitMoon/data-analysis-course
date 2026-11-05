# sql-17 · 累计、滑动窗口与 ROWS / RANGE

## 累计值包含哪些行
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW 表示从第一行累计到当前行。ROWS BETWEEN 2 PRECEDING AND CURRENT ROW 表示当前行与前两行，共最多三行。
## 明确窗口边界
带 ORDER BY 却不写 frame 时，许多聚合窗口默认 RANGE 到当前同行值，会把排序值相同的行一起包括。初学时写清 ROWS 和稳定排序，避免并列日期累计看起来突然跳跃。
## 最近七行不等于最近七天
先按天汇总并补齐没有交易的日期，才能用 ROWS 6 PRECEDING 表示当天加前六天。另一种方法是日期范围连接。滚动均值还要说明不足七天时使用已有天数还是固定七天作分母。

## 可运行例子

```sql
SELECT order_id,
  user_id,
  amount,
  SUM(amount) OVER(PARTITION BY user_id
  ORDER BY order_at,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_gmv
FROM orders
WHERE status='paid'
ORDER BY user_id,
  order_at,
  order_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

7 日滚动和 7 行滚动何时等价？

1. 只有金额相同时
2. 一日一行且日历连续时
3. 任何订单明细上都等价

<details><summary>答案与解释</summary>

答案：2。必须先保证行对应连续日期。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "order_id",
        "user_id",
        "amount",
        "running_gmv"
      ],
      "rows": [
        [
          "101",
          "1",
          "100.00",
          "100.00"
        ],
        [
          "102",
          "1",
          "50.00",
          "150.00"
        ],
        [
          "103",
          "1",
          "50.00",
          "200.00"
        ],
        [
          "104",
          "1",
          "200.00",
          "400.00"
        ],
        [
          "105",
          "1",
          "0.00",
          "400.00"
        ],
        [
          "106",
          "2",
          "80.00",
          "80.00"
        ],
        [
          "107",
          "2",
          "20.00",
          "100.00"
        ],
        [
          "114",
          "2",
          "100.00",
          "200.00"
        ],
        [
          "108",
          "3",
          "100.00",
          "100.00"
        ],
        [
          "109",
          "3",
          "100.00",
          "200.00"
        ],
        [
          "110",
          "4",
          "200.00",
          "200.00"
        ],
        [
          "111",
          "4",
          "50.00",
          "250.00"
        ],
        [
          "112",
          "7",
          "300.00",
          "300.00"
        ],
        [
          "113",
          "7",
          "100.00",
          "400.00"
        ]
      ],
      "total": 14
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
