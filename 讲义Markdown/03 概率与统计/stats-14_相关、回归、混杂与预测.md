# stats-14 · 相关、回归、混杂与预测

## 相关不等于因果
促销支出与销售额正相关，可能是促销起作用，也可能是旺季同时提高两者。影响处理和结果的第三个变量叫混杂因素。时间先后、相关强弱都不足以单独证明因果。
## 最简单的回归
y≈a+bx，a 是截距，b 是 x 增 1 时预测 y 的变化。最小二乘通过最小化残差平方和拟合。R² 描述模型在样本中解释的变异比例，不等于预测准确率，更不证明因果。
## 相关的几种形式
Pearson 衡量线性关系；Spearman 对排名看单调关系。离群点、范围受限、非线性都影响解读。回归推断要关注误差结构、异方差、相关观测和模型设定；预测还要在未参与训练的数据上评估。

## 可运行例子

```python
import numpy as np
from scipy.stats import linregress, spearmanr
x = np.array([1,2,3,4,5])
y = np.array([3,5,6,9,11])
r = linregress(x,y)
print("斜率/截距：", r.slope, r.intercept)
print("R²：", r.rvalue**2)
print("Spearman：", spearmanr(x,y).statistic)
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

回归系数显著可以单独证明因果吗？

1. 只要 R² 高就可以
2. 不可以
3. 可以

<details><summary>答案与解释</summary>

答案：2。遗漏混杂或反向因果仍可能存在。

</details>
