# python-01 · Python 第一步：变量、类型与 print

## 像给计算结果贴标签
price = 20 把整数 20 绑定到变量 price。等号在这里是赋值；比较相等写 ==。print(price) 把内容显示出来，否则运行脚本可能没有可见输出。
## 四种先认识的类型
int 是整数，float 是小数，str 是文本，bool 是 True/False。'20' 是文本，20 是数字，不能随意相加。None 表示缺少一个值，与 0、空字符串不同。
## 读代码的方法
程序通常从上到下执行，后面的变量可用前面的结果。# 后面是注释。变量名用能解释业务的英文或拼音，避免单字母堆叠。先改数值观察输出，再尝试增加计算。

## 可运行例子

```python
price = 20
quantity = 3
revenue = price * quantity
print("收入：", revenue)
print("变量类型：", type(revenue))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

把数量改成 5，计算收入。

提示：只修改 quantity 的值。

## 自测

Python 中 price = 20 表示？

1. 判断是否相等
2. 打印 20
3. 给变量赋值

<details><summary>答案与解释</summary>

答案：3。判断相等写 price == 20。

</details>

## 本机验证时的预期输出

```json
{
  "kind": "python",
  "text": "收入： 60\n变量类型： <class 'int'>\n"
}
```
