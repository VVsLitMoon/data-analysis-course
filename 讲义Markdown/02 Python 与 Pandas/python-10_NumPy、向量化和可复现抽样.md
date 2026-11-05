# python-10 · NumPy、向量化和可复现抽样

## 数组会整批运算
NumPy 的数组与 Python 列表不同，np.array([1,2])*2 得 [2,4]，列表 [1,2]*2 会重复列表。向量化用底层数组操作，通常比逐个 Python 循环更适合大表。
## 随机不是不可验证
np.random.default_rng(42) 创建固定种子的随机数生成器，同一算法环境下复现同一抽样流程。换种子可检验结论是否依赖某次抽样；种子不能消除抽样误差。
## 文件与图表在本讲义的安排
网页运行区只展示文本与表格，交互图由后面的专用控件提供。导出的 Notebook 可在 VS Code 中运行和画图；导出脚本会包含示例数据初始化，离开网页也能用。
## 条件分层和除零
np.where(条件,成立取值,否则取值) 可以整列打标签，多分支可用 np.select。计算 Pandas 比率前，用分母.where(分母.ne(0)) 把零变成缺失，再用分子.div(分母)，避免出现无穷大。不要把“不可计算”和“结果为零”混成一件事。

## 可运行例子

```python
import numpy as np
x = np.array([1, 2, 3])
print("数组乘法：", x * 2)
rng = np.random.default_rng(42)
print("抽 5 个 0 到 9 的整数：", rng.integers(0, 10, size=5))
print("均值：", x.mean())
print("分层：", np.where(x >= 2, "高", "低"))
numerator = pd.Series([10, 0])
denominator = pd.Series([100, 0])
print("安全比率：", numerator.div(denominator.where(denominator.ne(0))))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

固定随机种子主要用于？

1. 保证没有误差
2. 让结果一定显著
3. 复现抽样过程

<details><summary>答案与解释</summary>

答案：3。可复现和无偏、显著是不同概念。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "数组乘法： [2 4 6]\n抽 5 个 0 到 9 的整数： [0 7 6 4 4]\n均值： 2.0\n分层： ['低' '高' '高']\n安全比率： 0    0.1\n1    NaN\ndtype: float64\n"
}
```
