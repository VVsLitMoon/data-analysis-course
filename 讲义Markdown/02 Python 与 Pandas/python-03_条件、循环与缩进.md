# python-03 · 条件、循环与缩进

## 如果满足条件，就执行
if 后面写条件和英文冒号，下面缩进四个空格。elif 是另一种情况，else 兜底。缩进决定哪些代码属于分支，不只是排版。
## 对每个元素重复同一动作
for amount in amounts 依次把列表元素交给 amount。range(3) 得到 0、1、2。while 在条件成立时持续运行，初学尽量先用有明确终点的 for，避免无限循环。
## 计数器怎么工作
先设 total=0，再每次 total += amount，相当于 total=total+amount。break 结束循环，continue 跳过本次剩余操作。能用向量化处理表时，Pandas 通常不必逐行循环。

## 可运行例子

```python
amounts = [100, 50, 0, 80]
total = 0
for amount in amounts:
    if amount > 0:
        total += amount
        print("计入：", amount)
print("合计：", total)
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

只累计至少 80 的金额。

提示：把 if 条件改为 amount >= 80。

## 自测

Python 用什么确定代码块范围？

1. 缩进
2. 句号
3. 中文括号

<details><summary>答案与解释</summary>

答案：1。保持一致缩进是语法要求。

</details>
