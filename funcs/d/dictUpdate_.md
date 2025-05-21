# dictUpdate!

## 语法

`dictUpdate!(dictionary, function, keys, parameters,
[initFunc=copy])`

## 参数

**dictionary** 是一个字典。

**function** 是一个函数。

**keys** 可以是标量或向量，表示对哪些键应用函数。

**parameters** 和 **keys** 具有相同长度。应用函数的参数是 *parameters* 和字典的初始值。

**initFunc** 是一个一元函数。当更新的键不存在时，执行该函数。只有当字典的值是 ANY 类型时，才能指定该参数。

## 详情

更新字典中的特定的键的值。

## 例子

```
x=dict(1 2 3, 1 1 1);
x;
// output
3->1
1->1
2->1

dictUpdate!(x, add, 2 3, 1 2);
// output
3->3
1->1
2->2

x.dictUpdate!(mul, 3 4, 2 4);
// output
4->4
3->6
1->1
2->2

d = dict(`IBM`MSFT, [1 2, 3 4])
msg = table(`IBM`MSFT`GOOG as symbol, 2 3 2 as ap)
d.dictUpdate!(append!, msg.symbol, msg.ap, x->array(x.type(), 0, 512).append!(x))
d;
// output
MSFT->[3,4,3]
GOOG->[2]
IBM->[1,2,2]
```

