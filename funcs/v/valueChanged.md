# valueChanged

## 语法

`valueChanged(X, [mode="prev"])`

## 参数

**X** 字符串、布尔、时间或数值类型的向量/矩阵/表/元组。

**mode** 字符串，可选值为："prev", "next", "either" 和 "both"，默认值为 "prev"。

* "prev"：前一个元素。
* "next"：后一个元素。
* "either"：前一个元素或后一个元素。
* "both"：前一个元素和后一个元素值。

## 详情

*X* 中每个元素较 *mode* 是否发生变化，若当前元素值发生变化，则返回 true，否则返回 false。若比较对象不存在，则返回
false。例如：valueChanged(X, [mode="prev"]) 的第一个元素返回 false；valueChanged(X,
[mode="next"]) 的最后一个元素返回 false。

若 *X* 为矩阵/表，在每列内进行上述操作，返回一个矩阵/表。

## 例子

```
x= 1 2 2 2 2 3 NULL 3 4 8
valueChanged(x)
// output
[false,true,false,false,false,true,true,true,true,true]

valueChanged(x,"next")
// output
[true,false,false,false,true,true,true,true,true,false]

valueChanged(x,"either")
// output
[true,true,false,false,true,true,true,true,true,true]

valueChanged(x,"both")
// output
[false,false,false,false,false,true,true,true,true,false]

tup=(1 2 3, `A`A`B, 2021.10.12+1 2 2)
valueChanged(tup)
// output
([false,true,true],[false,false,true],[false,true,false])

m=matrix(1 2 3, 1 2 3, 1 3 3)
valueChanged(m)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| false | false | false |
| true | true | true |
| true | true | false |

```
id= 1 2 2 2 2 3 3 4 8
sym=`A + string(1 2 2 2 2 3 3 4 8)
val=83.8 92.8 8.1 61.4 40.7 67.2 15.2 20.6 96.5
t=table(id, sym, val)
valueChanged(t)
```

| id | sym | val |
| --- | --- | --- |
| false | false | false |
| true | true | true |
| false | false | true |
| false | false | true |
| false | false | true |
| true | true | true |
| false | false | true |
| true | true | true |
| true | true | true |

相关函数：[keys](../k/keys.html)

