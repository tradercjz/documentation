# talib

## 语法

`talib(func, args...)`

## 参数

* **func** 是一个函数名。
* **args** 是函数 func 的参数。

其他相关的 talib 系列函数的参数说明和窗口计算规则请参考: [TA-lib 系列](../themes/TAlib.html)

## 详情

当 args 的前几个元素为 NULL 时，DolphinDB 内置滑动窗口函数与 python TA-lib 的处理方式不同：

* DolphinDB 滑动窗口函数：窗口从第一个元素开始进行滑动窗口计算；
* python TA-lib： 保留开始的所有前置 NULL 值，然后从第一个非空元素开始进行滑动窗口计算。

若需要与 python TA-lib 保持一致的处理方式，可以使用 talib 函数。

## 例子

以下例子通过对比说明了 `talib` 函数和 DolphinDB 函数处理 NULL 值的区别。

```
msum(NULL 1 2 3 4 5 6 7 8 9, 3)
```

输出返回：[,,3,6,9,12,15,18,21,24]

```
talib(msum, NULL 1 2 3 4 5 6 7 8 9, 3)
```

输出返回：[,,,6,9,12,15,18,21,24]

