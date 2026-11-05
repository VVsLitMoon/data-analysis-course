# stats-12 · 均值比较：z、t、配对与 Welch

## 先辨认样本关系
同一批用户改版前后是配对数据，可对每人的差值做单样本 t 检验；两批互不重叠用户是独立样本，不能误用配对检验。前后对比仍可能受时间趋势影响，统计检验本身不赋予因果性。
## t 和 z 不按 30 一刀切
总体方差已知的均值问题可用 z；未知时常用 t。样本量增大 t 逐渐接近正态。独立样本均值比较通常可考虑 Welch t，不强行假设两组方差相等。
## 检查假设
独立性、异常值、样本量和分布形态都影响可靠性。重尾数据可以结合合适的聚合单位、预先规定的处理、bootstrap 或稳健方法。不要为了显著随意删大额用户。

## 可运行例子

```python
from scipy.stats import ttest_ind, ttest_rel
a = [10, 12, 9, 13, 11, 14]
b = [12, 15, 10, 16, 13, 18]
print("独立样本 Welch：", ttest_ind(a, b, equal_var=False))
print("若确实是同一人前后配对：", ttest_rel(a, b))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

不知道两组方差相等，独立样本均值比较常可考虑？

1. Welch t 检验
2. 强行把观测配对
3. 只比较总和

<details><summary>答案与解释</summary>

答案：1。Welch 不要求两组总体方差相同。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "独立样本 Welch： TtestResult(statistic=np.float64(-1.7751790062418158), pvalue=np.float64(0.11136649244823799), df=np.float64(8.550295857988166))\n若确实是同一人前后配对： TtestResult(statistic=np.float64(-5.838742081211423), pvalue=np.float64(0.002084792945485739), df=np.int64(5))\n"
}
```
