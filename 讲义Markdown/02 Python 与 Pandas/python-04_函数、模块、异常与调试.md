# python-04 · 函数、模块、异常与调试

## 把重复逻辑装进函数
def rate(buyers,visitors): 定义函数，括号里是参数。return 把结果交给调用者，print 只是显示。函数内部的局部变量通常不应该靠外部代码直接读取。
## 不要藏住错误
除零、错误类型、不存在的列都会报异常。先看报错最后一行，再找代码行号；可以 print 中间变量或用 VS Code 断点。try/except 用于能合理处理的已知问题，不要一股脑忽略所有错误。
## 导入模块，使用现成的函数
import math 导入模块，math.sqrt(4) 求平方根。库版本不同可能影响行为。本讲义运行时预装了 pandas、NumPy、SciPy、scikit-learn；文件和网络读写留在你自己的 VS Code 环境操作。

## 可运行例子

```python
def conversion_rate(buyers, visitors):
    if visitors == 0:
        return None
    return buyers / visitors

print(conversion_rate(12, 100))
print(conversion_rate(0, 0))
import math
print(math.sqrt(16))
```

网页点击“运行代码”。SQL 每次恢复示例表；Python 预置六张 DataFrame。

## 动手改一处

把第一个调用改成 25 位购买、200 位访问。

提示：修改函数调用参数，不需要修改定义。

## 自测

return 与 print 的区别是？

1. 完全一样
2. return 只用于循环
3. return 交回结果，print 显示内容

<details><summary>答案与解释</summary>

答案：3。函数返回值可继续参与计算。

</details>
