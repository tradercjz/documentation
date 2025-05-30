# each

## 语法

`each(func, args...)`

(把一个函数应用到指定参数中的每个元素。)

或

`F :E X`

(把一个函数应用到X中的每个元素。)

或

`X <operator> :E Y`

(把一个函数应用到X和Y中的每个元素，X和Y长度相同。)

或

`func:E(args...)`

## 参数

* **func** 是一个函数。
* **args** 是func的参数。
* **operator** 是一个二元运算符。
* **X** 和 **Y** 可以是数据对、向量、矩阵、表、数组向量或字典。

## 详情

将指定函数（func）或运算符（operator）按以下规则应用到输入对象(args, X, Y)上：

* 对于矩阵，把函数应用到每一列；
* 对于表，把函数应用到每一行；
* 对于数组向量，把函数应用到每一行；
* 对于字典，把函数应用到字典的每一个 value。

each 根据每个子任务计算结果的数据类型和形式，决定返回值的数据形式。若所有子任务的数据类型和形式都相同，则返回 Vector 或 Matrix，否则返回
Tuple。

func(X) 和 func :E X 的区别是前者将X视作一个输入变量，而后者取遍X中的每一个参数。如果 func 是一个向量函数，应该避免使用 "each (:E)
" ，因为在元素比较多的时候，元素的比对就会很慢。

*peach* 是并行计算版本的 *each* 高阶函数。对于执行时间较长的任务，*peach* 比
*each* 能节省大量的时间。但对于小任务，*peach* 可能执行时间要比each更长，因为并行函数调用的开销很大。

## 例子

假设需要计算3个员工的日薪，员工的工时存放在向量x=[9,6,8]中，员工的时薪在8小时以下是$10，在8小时以上是$20。考虑下面的 *wage*
函数：

```
x=[9,6,8]
def wage(x){if(x<=8) return 10*x; else return 20*x-80}
wage x;

The vector can't be converted to bool scalar.
```

*wage(x)* 不返回结果，因为x<=8，即 [9,6,8]<=8 返回了一个向量的条件值[0,1,1]，而不是if 需要的标量。

可使用以下方案来解决这个问题：

```
each(wage, x);

[100,60,80]

wage :E x;

[100,60,80]

def wage2(x){return iif(x<=8, 10*x, 20*x-80)};
// iif 函数是一个逐元素的条件操作

wage2(x);

[100,60,80]
```

类似的，*each* 也可以用于有多个参数的函数：

```
def addeven(x,y){if (x%2==0) return x+y; else return 0}
x1=1 2 3
x2=4 5 6;
each(addeven, x1, x2);

[0,7,0]
```

*each* 所用数据可以是数据对：

```
t = table(1 2 3 as id, 4 5 6 as value, `IBM`MSFT`GOOG as name);
t;
```

| id | value | name |
| --- | --- | --- |
| 1 | 4 | IBM |
| 2 | 5 | MSFT |
| 3 | 6 | GOOG |

```
each(max, t[`id`value]);

[3,6]
```

*each* 所用数据可以是矩阵：

```
m=1..12$4:3;
m;
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 1 | 5 | 9 |
| 2 | 6 | 10 |
| 3 | 7 | 11 |
| 4 | 8 | 12 |

```
each(add{1 2 3 4}, m);
// add{1 2 3 4}是一个部分应用，each将向量[1, 2, 3, 4]与矩阵m的每列相加。
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 2 | 6 | 10 |
| 4 | 8 | 12 |
| 6 | 10 | 14 |
| 8 | 12 | 16 |

```
x=1..6$2:3;
y=6..1$2:3;
x;
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
y;
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 6 | 4 | 2 |
| 5 | 3 | 1 |

```
each(**, x, y);

[16,24,16]
// 比如，24=3*4+4*3
```

当输入对象有多个时，每次取出每个对象相同位置的元素，作为指定函数的参数。例如：

```
m1 = matrix(1 3 6, 4 6 8, 5 -1 3)
m2 = matrix(3 -6 0, 2 NULL 3, 6 7 9)
each(corr, m1, m2)
// 等价于 corr(m1[0], m2[0]) join corr(m1[1], m2[1]) join corr(m1[2], m2[2])

[-0.216777, 1, -0.142857]
```

从 2.00.9 版本开始，*each* 所用数据可以是字典：

```
d=dict(`a`b`c, [[1, 2, 3],[4, 5, 6], [7, 8, 9]])
each(sum, d)

b->15
c->24
a->6
```

下例中，我们在一个部分应用中使用了 *call* 函数，该部分应用将向量[1 2 3]作为参数，分别调用函数 *sin* 与
*log*。

```
// 当 "functionName" 为空时，将动态地选择一个函数名字。
each(call{, 1..3},(sin,log));
```

| sin | log |
| --- | --- |
| 0.841471 | 0 |
| 0.909297 | 0.693147 |
| 0.14112 | 1.098612 |

func 为自定义函数，对字典进行操作。当字典的 key 的类型是字符串时，*each* 会对字典进行合并，返回一个表。合并规则如下：

1. 根据第一个字典确定表的 schema，并将字典的 value 写入表中第一行。字段名为该字典的 keys，列数为该字典的 keys
   的个数。无论后续被遍历字典 keys 的个数如何变化，表的 schema 不会被修改。
2. 在遍历后续字典时，每一个字典对应表中一行数据。若某个 key 与表字段名相同，则将其 value 追加到表中，若某个 key
   与表字段不同，则追加空值到表中。

   ```
   days = 2023.01.01..2023.01.10
   def mf(day) {
       out = dict(STRING, ANY)
       if(day==2023.01.05){
           out["v"] = 3
       }
       else{
           out["day"] = day
           out["v"] = 1
       }
       return out
   }
   each(mf, days)

   ```

   | v | day |
   | --- | --- |
   | 1 | 2023.01.01 |
   | 1 | 2023.01.02 |
   | 1 | 2023.01.03 |
   | 1 | 2023.01.04 |
   | 3 |  |
   | 1 | 2023.01.06 |
   | 1 | 2023.01.07 |
   | 1 | 2023.01.08 |
   | 1 | 2023.01.09 |
   | 1 | 2023.01.10 |

从2.00.12和3.00.0版本开始，each 可以接受多元函数且第一个参数为字典。

对于表 t 中 id 列的每个元素，计算其向前累加直到不小于3经过的周期数（可用 `sumbars` 函数实现）；对 id2
的每个元素，计算其向前累加直到不小于5经过的周期数。因为用 `sumbars` 计算每列数据时，*Y*
不同（分别是3和5），必须用一个二元函数跟 each
搭配使用。对一个表转置（`transpose`），返回一个以列名为键值，列为数值的字典。对字典应用转置函数，则还原为表。

```
t = table(1..10 as id, 2..11 as id2)
sumbars:E(t.transpose(), 3 5).transpose()
```

| id | id2 |
| --- | --- |
| 0 | 0 |
| 2 | 2 |
| 1 | 2 |
| 1 | 1 |
| 1 | 1 |
| 1 | 1 |
| 1 | 1 |
| 1 | 1 |
| 1 | 1 |
| 1 | 1 |

提示：

1. 对于执行时间长的任务，使用 *peach* 进行并行计算，可以节约任务执行时间。

   ```
   m=rand(1,20000:5000)
   timer f=peach(mskew{,8},m)

   Time elapsed: 3134.71 ms
   timer f=mskew(m,8)

   Time elapsed: 8810.485 ms
   ```
2. 当元素数量很多时候，不推荐使用 *:E (each)*
   高阶函数，可以使用更高效的向量解决方案。

   ```
   x=rand(16, 1000000);
   timer(10){each(wage, x)};

   Time elapsed: 38164.9 ms

   timer(10){iif(x<8,10*x,20*x-80)};

   Time elapsed: 81.516 ms
   ```

