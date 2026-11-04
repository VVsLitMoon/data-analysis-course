# stats-13 · 比例、卡方、Fisher 与方差分析

## 两组转化率
每组独立用户是否转化是二元结果。样本充分时可用两比例 z 检验；在 H0 两比例相同时，标准误常使用合并比例。对效应差构造区间时常用不同的非合并方差，不能混用步骤。
## 分类变量关联
卡方独立性检验比较列联表的观察频数与独立假设下期望频数，输入应是人数，不是百分比。稀疏小样本的 2×2 表可考虑 Fisher 精确检验。它们检验关联，不自动证明因果。
## 三组以上
ANOVA 比较多个组均值，显著说明至少某组不同，并不告诉你哪一对。进一步成对比较需处理多重检验；方差不齐等条件下选择合适变体。非参数 Mann–Whitney 检验也有假设，并非通用“中位数检验”。

## 可运行例子

```python
import numpy as np
from scipy.stats import norm, chi2_contingency, fisher_exact
n_a = n_b = 1000
x_a, x_b = 100, 125
pool = (x_a+x_b)/(n_a+n_b)
se = np.sqrt(pool*(1-pool)*(1/n_a+1/n_b))
z = (x_b/n_b-x_a/n_a)/se
print("两比例双侧 p：", 2*norm.sf(abs(z)))
print("卡方：", chi2_contingency([[100,900],[125,875]], correction=False).pvalue)
print("小样本 Fisher：", fisher_exact([[1,9],[6,4]]).pvalue)
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

列联表检验应输入？

1. 只输入百分比
2. 均值和最大值
3. 各格人数或频数

<details><summary>答案与解释</summary>

答案：3。频数体现样本量，对不确定性至关重要。

</details>
