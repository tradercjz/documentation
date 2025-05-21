# 函数

## DolphinDB 内置函数

在 Python Session 中，DolphinDB 的绝大部分内置函数可以直接调用，无需导入任何模块。但某些 DolphinDB 的内置函数名（如：dict, set, type 等）与 Python 的函数名相同，此时系统会优先解析为 Python 的函数。

Python Parser 将 DolphinDB 中与 Python 内置函数同名的函数以及 DolphinDB 的常量对象封装在 dolphindb 库中，可在引入 dolphindb 库后调用这些函数或常量对象。

```
import dolphindb as ddb
x = [1,2,3,4].toddb()
type(x)
// output: dolphindb.VECTOR.INT
ddb.type(x)
// output: 4
```

某些 DolphinDB 的内置函数支持运算符作为函数（如 expr, nullCompare 等）的入参。在 Python Parser 中，不能直接传入 Python 支持的运算符和关键字（如：not、and）作为参数，否则会因解析冲突而抛出异常。若运算符存在对应的 DolphinDB 内置函数，可替换成内置函数，见下例：

DolphinDB:
fu

```
expr(6, <, 8)
```

Python Parser:

```
expr(6, lt, 8)
```

**注意**：自定义函数名不能和内置函数同名。

## 命名函数

Python Parser 命名函数的定义和 Python 语法保持一致，以冒号和缩进声明函数体：

```
def <functionName> ([parameters]):
    statements
```

例：定义了一个函数，返回小于 n 的斐波那契数列。

```
def fib(n):
    xs = []
    a, b = 0, 1
    while a < n:
        xs.append(a)
        a, b = b, a + b
	return xs
fib(2000)
// output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
```

Python Parser 自定义函数，支持指定默认参数。目前仅支持常量作为默认参数值：

```
def func1(a, b=1):
    return a+b

func1(4)
// output: 5
```

Python Parser 中调用函数时，支持按顺序提供默认参数，也支持以指定关键字的方式提供参数：

```
def func2(a, b=1, c=2):
    return a+b-c

func2(4, c=4)
// output: 1
```

**注意**：Python Parser 的函数暂不支持：

* 位置参数（/）。
* 星号参数（\* 和 \*\*）
* 函数里面定义类。
* 函数里面使用 import。
* 在函数内可以读取全局变量的值，但无法修改它。

## 聚合函数

`defg` 是 Python Parser 对 DolphinDB 的扩展支持，用于定义聚合函数。

```
defg <functionName> ([parameters]):
    statements
```

## lambda 函数

DolphinDB 原生语法支持如下4种[lambda 表达式](../../lambda.md) 的写法：

```
def <functionName>(parameters): expression

def (parameters): expression

def (parameters) -> expression

parameter -> expression
```

Python 原生语法不支持使用 def 定义匿名函数，也不支持识别 "->" 符号，因此 Python Parser 不支持通过上述4种方法构造 lambda 函数。

Python Parser 的 lambda 表达式书写规则及使用方法与 Python 保持一致：

```
lambda [arg1 [,arg2,.....argn]]: expression
```

## 高阶函数

Python Parser 可直接调用 DolphinDB 内置的高阶函数，但不支持通过符号的方式进行调用。

## 嵌套函数

```
def test_func1(x):
    w = [0.1, 0.3, 0.5, 0.1].toddb()
    def inner():
        s = wsum(x, w)
        return s
    re = inner() / 100
    return re

test_func1([1,2,3,4].toddb())
// output: 0.026

==========================================

def test_func2():
    w = [0.1, 0.3, 0.5, 0.1].toddb()
    def inner(x):
        s = wsum(x, w)
        return s
    x = [1,2,3,4].toddb()
    re = inner(x) / 100
    return re

test_func2()
// output: 0.026
```

## 部分应用（偏函数）

待后续版本支持。

## 函数装饰器

待后续版本支持。

## 函数调用

支持以下2种形式：

* 标准函数调用格式：`<func>(parameters)`
* 调用对象方法格式：`x.<func>(parameters)`，其中 x 是第一个参数。

