# stats-15 · Bootstrap、置换与稳健性

## 用重抽样近似不确定性
Bootstrap 从已有样本中有放回抽取同样大小的样本，反复计算统计量，观察其分布。简单百分位区间取 2.5% 与 97.5% 分位；不是所有小样本或极端分布下都准确，复杂场景需更合适方法。
## 抽样单位要对
用户随机分流时，同一用户多条订单应一起抽取或先聚合到用户。直接按订单抽样会破坏相关结构，低估不确定性。Bootstrap 不能修复有偏样本或缺失关键人群。
## 置换检验在做什么
在可交换性等零假设条件下打乱组标签，比较真实统计量与随机标签统计量。它与有放回重抽样不同。随机种子、重复次数和预处理规则应记录，结果才能复现。

## 可运行例子

```python
import numpy as np
rng = np.random.default_rng(42)
x = np.array([10,12,9,13,11,14,8,12])
boot = rng.choice(x, size=(2000,len(x)), replace=True).mean(axis=1)
print("Bootstrap 均值区间：", np.quantile(boot,[0.025,0.975]))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

用户随机分流且一人多单，应优先按什么重抽样？

1. 用户
2. 任意订单行
3. 金额大小排序位置

<details><summary>答案与解释</summary>

答案：1。保留随机化单位内部的相关结构。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "Bootstrap 均值区间： [ 9.875 12.375]\n"
}
```
