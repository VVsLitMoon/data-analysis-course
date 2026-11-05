# business-05 · RFM、用户分层与生命周期

## R、F、M 是什么
Recency：距最近购买多久；Frequency：观察窗内购买频次；Monetary：观察窗内消费金额。R 越小通常越近期，F/M 越大通常越活跃或价值高；分层方向要写清。
## 如何分层才有用
确定观察日与窗口，计算一人一行特征，再用业务阈值或分位数分组。小样本、并列和长期零购买用户需要处理。RFM 是行为描述，不自动等于终身价值，也不是因果模型。
## 分层要连行动
高价值近期活跃者重体验；高价值久未回访者查流失原因；新客看首购障碍；低价值群体注意服务成本。策略效果用随机实验检验，不凭标签决定人群天生好坏。

## 可运行例子

```sql
SELECT user_id,
  DATEDIFF('2026-04-01',MAX(DATE(order_at))) AS recency_days,
  COUNT(*) AS frequency,
  SUM(amount) AS monetary
FROM orders
WHERE status='paid' AND order_at<'2026-04-01'
GROUP BY user_id
ORDER BY user_id;
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

RFM 的 R 越大通常意味着？

1. 消费金额越高
2. 距离最近购买越久
3. 最近购买越近

<details><summary>答案与解释</summary>

答案：2。这里 R 定义为距最近购买天数。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "sql",
  "results": [
    {
      "columns": [
        "user_id",
        "recency_days",
        "frequency",
        "monetary"
      ],
      "rows": [
        [
          "1",
          "59",
          "5",
          "400.00"
        ],
        [
          "2",
          "31",
          "3",
          "200.00"
        ],
        [
          "3",
          "88",
          "2",
          "200.00"
        ],
        [
          "4",
          "88",
          "2",
          "250.00"
        ],
        [
          "7",
          "58",
          "2",
          "400.00"
        ]
      ],
      "total": 5
    }
  ],
  "text": "执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。"
}
```
