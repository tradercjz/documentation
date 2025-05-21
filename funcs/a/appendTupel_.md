# appendTuple!

## 语法

`appendTuple!(X, Y, [wholistic=false])`

## 参数

**X** 是一个元组。

**Y** 是一个元组。

**wholistic** 是一个 bool 标量，默认值为 false。

## 详情

将 *Y* 中的数据追加到 *X* 中。

* 当 *wholistic* 为 true 时，将 *Y* 整体作为一个元素追加到 *X* 中
* 当 *wholistic* 为 false 时，将 *Y* 中的每一个元素依次追加到 *X* 中
* 当 *X* 是列式元组时，*Y* 中元素必须与 *X* 中元素类型一致，且 *wholistic* 只能为
  false

## 例子

```
x = (1,"X")
y = ([2,3],"Y")
x.appendTuple!(y,true)
print(x)
// output
(1,"X",([2,3],"Y"))

x.appendTuple!(y,false)
print(x)
// output
(1,"X",([2,3],"Y"),[2,3],"Y")

x = [[1,2,3],4]
x.setColumnarTuple!()
x.appendTuple!((5,6),false)
print(x)
([1,2,3],4,5,6)
```

