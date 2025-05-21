# subtuple

## 语法

`subtuple(X, range)`

## 参数

**X** 是一个元组，它的每个元素必须是长度相同的向量。

**range** 是一个整型数据对，表示范围，只包含下限不包含上限。

## 详情

创建 *X* 的只读子元组。*subtuple*
几乎能在瞬间创建一个只读向量，相比之下，创建一个新的元组需要耗费更多时间。

## 例子

例1：

```
x=(1..10, 11..20, 21..30, 31..40)
subtuple(x, 2:4);
// output
([3,4],[13,14],[23,24],[33,34])
```

例2：

```
m=1000.0
n=20000000
a=(rand(m,n), rand(m,n))
k=10000000;
timer each(avg, a.subtuple(0:k));
// output
Time elapsed: 30.87 ms

timer each(avg, (a[0][0:k], a[1][0:k]));
// output
Time elapsed: 46.508 ms
```

例3：

```
x=(1..10, 11..20)
subtuple(x, 2:4)=([4, 5], [14, 15]);
// output
Syntax Error: [line #2] Please use '==' rather than '=' as equal operator in non-sql expression.
```

`subtuple` 函数创建的元组只能读取，不能写入。

