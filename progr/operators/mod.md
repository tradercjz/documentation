# mod(%)

## 语法

`X % Y`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量或矩阵。当*X*和*Y*都是向量或矩阵时，它们的长度必须相同。

## 详情

`mod` 表示取模。它返回的是 *X* 与 *Y* 逐个元素相除的余数。

* 当 *Y* 是正整数时，结果总是非负的，例如，-10%3 的结果是 2；
* 当 *Y* 是负整数时，结果总是非正的，例如，-10%-3 的结果是 -1。

函数 [mod](../../funcs/m/mod.md)
通常用于分组数据。例如，`[5,4,3,3,5,6]%3`是`[2,1,0,0,2,0]`；数据可以分为三组。

## 例子

```
x=1 2 3;
x % 2;
// output
[1,0,1]

2 % x;
// output
[0,0,2]

y=4 5 6;
x mod y;
// output
[1,2,3]
mod(y, x);
// output
[0,1,0]

m=1..6$2:3;
m;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
m mod 3;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 0 | 2 |
| 2 | 1 | 0 |

```
x=-1 2 3;
x%-5;
// output
[-1,-3,-2]

-1%5;
// output
4
```

