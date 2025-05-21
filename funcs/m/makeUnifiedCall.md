# makeUnifiedCall

## 语法

`makeUnifiedCall(func, args)`

## 参数

**func** 是一个函数。

**args** 是一个 tuple, 由所调用函数的参数所构成。从版本 2.00.11.3 起，args
可以是一个元代码的标量，其代码是一个元组表达式。

## 详情

它使用指定参数调用一个函数并生成脚本。 高阶函数 [unifiedCall](../ho_funcs/unifiedCall.md) 与 `makeUnifiedCall`
的区别是，`makeUnifiedCall` 不执行脚本。

## 例子

```
mc = makeUnifiedCall(matrix, (1 2 3, 4 5 6));
mc;
// output
< matrix([1,2,3], [4,5,6]) >
mc.eval();
```

| col1 | col2 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

从版本2.00.11.3 起， args 支持传入一个元代码标量，其代码是一个元组表达式。

通过下例的对比可以看到：

* 当 args 是一个元组时，会将元组中变量的值传入，此时 a 的值为 < add(3, 5) >
* 当 args 是一个元组表达式的元代码时，会将变量作为函数的参数，生成元代码，此时 b 的值为 < add(x, y) >

```
x=3
y=5
a = makeUnifiedCall(add, (x,y)) // < add(3, 5) >
b = makeUnifiedCall(add, <(x,y)>) // < add(x, y) >
```

因此，当 x 或 y 的值改变，b
的执行结果会将 x 和 y 的值动态传入，而 a 的执行结果不会随 x 和 y 的值变化

```
x = 6
a.eval() //计算 3+5
```

结果为 8 。

```
b.eval() // 计算 6+5
```

结果为 11 。

下例中，函数 `makeUnifiedCall` 以
`sqlTuple` 生成的元组表达式的元代码为参数，调用自定义函数 f，其结果作为函数 sql 的参数 select
，从而生成元代码 c 。

```
// 自定义函数
f = def (x,y)->(x-y)/(x+y)

// 定义待查询的表
t = table(1.0 2.0 3.0 as qty1, 1.0 3.0 7.0 as qty2)

// 生成查询的元代码
c = sql(select=makeUnifiedCall(f, sqlTuple(`qty1`qty2)), from=t)

// 执行对应元代码
c.eval()
```

| \_qty1 |
| --- |
| 0 |
| -0.2 |
| -0.4 |

**相关信息**

* [sqlTuple](../s/sqlTuple.html "sqlTuple")

