# not support: t[0][0]=1
```

## 元组可用的所有属性和方法

```
dir(s)
// output: ['__add__', '__at__', '__dir__', '__eq__', '__iadd__', '__imultiply__', '__init__', '__iter__', '__len__', '__multiply__', '__ne__', '__repr__', '__req__', '__rne__', '__str__', 'toddb']
```

其中 `toddb` 是 Python Parser 中特有的方法，它支持将 Python Parser 的元组对象转换成 DolphinDB 的元组。

```
s = (1, 2, 3)
type(s.toddb())
// output: dolphindb.VECTOR.ANY
```

## 元组支持的操作符

| 操作符 | 含义 | 例子 |
| --- | --- | --- |
| \* | 重复元组 | (1, 2, 3) \* 3 |
| + | 拼接元组 | (1, 2022.01M, 3) + (4, 5, "banana") |

