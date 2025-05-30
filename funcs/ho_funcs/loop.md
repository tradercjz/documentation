# loop

## 语法

`loop(func, args...)`

或

`func:U(args…)`

或

`func:U X`

或

`X func:U Y`

## 详情

loop 高阶函数与 each 高阶函数很相似，区别在于函数返回值的格式和类型。ploop 是相应的并行版本。

each 高阶函数根据每个子任务计算结果的数据类型和形式，决定返回值的数据形式。若所有子任务的数据类型和形式都相同， 则返回
Vector 或 Matrix，否则返回 Tuple。而 loop 总是返回 Tuple。

## 参数

* **func** 是一个函数。
* **args/X/Y** 是 *func* 的参数。

## 例子

函数入参是矩阵时：

```
m=matrix([1 3 4 2,1 2 2 1])
max:U(m)
```

返回：(4,2)

```
n=matrix([11 5 9 2,8 5 3 2])
m add:U n
```

返回：([12,8,13,4],[9,7,5,3])

函数入参是数组向量时：

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5 4, 6 7 8, 1 9 10]);
sum:U(a)
```

返回：(6,9,21,19)

下例中，通过 loop 函数将数组转换为元组。

```
a=[1,2,3,4,5]
asis:U(a)
```

返回：(1,2,3,4,5)

