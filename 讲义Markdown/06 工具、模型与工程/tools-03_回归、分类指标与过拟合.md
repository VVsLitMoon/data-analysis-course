# tools-03 · 回归、分类指标与过拟合

## 模型需要理解的层次
线性回归预测连续值；逻辑回归通过 sigmoid 把线性组合映射到概率，并不是预测连续目标的普通回归。树能表达非线性和交互；随机森林、梯度提升集成多棵树，仍需控制复杂度和验证。
## 分类指标
Precision=TP/(TP+FP)，Recall=TP/(TP+FN)，F1 是二者调和平均。正例少时 accuracy 可能很高却毫无用处；ROC-AUC 衡量排序的一种表现，PR 曲线常更直接关注稀少正例。阈值决定业务漏报与误报成本，概率还需校准。
## 回归与过拟合
MAE 是绝对误差均值，RMSE 更惩罚大误差。训练好测试差是过拟合信号；正则化、降低复杂度、更多合适数据可改善。偏差—方差权衡不是越复杂越好，不能反复在测试集上挑模型。

## 可运行例子

```python
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
y_true = [0,0,0,1,1,1]
y_pred = [0,0,1,0,1,1]
print(confusion_matrix(y_true,y_pred))
print("精确率/召回/F1：",precision_score(y_true,y_pred),recall_score(y_true,y_pred),f1_score(y_true,y_pred))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 自测

正例极少时只看 accuracy 有什么问题？

1. 全预测负例也可能很高
2. 一定等于召回率
3. 无法计算

<details><summary>答案与解释</summary>

答案：1。指标要与业务代价和类别结构相符。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "[[2 1]\n [1 2]]\n精确率/召回/F1： 0.6666666666666666 0.6666666666666666 0.6666666666666666\n"
}
```
