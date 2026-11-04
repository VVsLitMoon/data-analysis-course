# python-02 · 列表、字典、索引和切片

## 一串值和一组对应关系
列表 [10,20,30] 按顺序保存多个值，字典 {'organic':100,'paid':80} 按键查值。列表从 0 开始编号，a[0] 是第一个；a[-1] 是最后一个。切片 a[0:2] 取第 0、1 位，不包含第 2 位。
## 不要把容器混淆
元组 tuple 常表示固定组合，集合 set 存不同元素且不能靠它保留排序。len 求长度，sum 对数值求和。字典的键必须存在才能直接索引，也可用 .get(键,默认值)。
## 可变对象要留心
b=a 不会复制整个列表，两个名字指向同一对象；简单列表复制用 a.copy()。复杂嵌套复制另有细节，先能识别“修改共享对象”的问题。

## 可运行例子

```python
amounts = [100, 50, 80]
channels = {"organic": 100, "paid": 80}
print(amounts[0], amounts[-1], amounts[:2])
print(sum(amounts), len(amounts))
print(channels.get("new_channel", 0))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

加入第四个金额并求平均。

提示：平均值 = sum(amounts) / len(amounts)。

## 自测

列表第一项的索引是？

1. -2
2. 0
3. 1

<details><summary>答案与解释</summary>

答案：2。Python 索引从 0 开始。

</details>
