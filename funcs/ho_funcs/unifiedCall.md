# unifiedCall

## 语法

`unifiedCall(func, args)`

## 参数

**func** 是一个函数。

**args** 是一个tuple, tuple的每一个元素作为函数的参数。

## 详情

用指定的参数调用一个函数。同 [call](call.md) 类似，可以用在 [each/peach](each.md) 或 [loop](loop.md)/[ploop](ploop.md) 函数中，来调用一批函数。区别在于，*call*
函数的args参数个数不确定，由func传入的函数决定。 而 *unifiedCall*
的args只有一个，通过tuple来给func函数传入多个参数。

## 例子

```
unifiedCall(sum, [1..10])
```

返回：55

```
unifiedCall(add, ([1,2,3,4,5,6,7,8,9,10],2))
```

返回：[3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

```
each(unifiedCall, [std, max], [[matrix(1 3 5 7 9, 1 4 7 10 13)], [0..100]]);
```

得到：

| col1 | col2 |
| --- | --- |
| 3.1623 | 100 |
| 4.7434 | 100 |

下面这个例子，自定义一个函数，再通过unifiedCall传入参数，进行调用。

```
def f(a,b){return (a+2)*b}
unifiedCall(f, (5,10))
```

返回：70

