# ffill!

## 语法

`ffill!(obj,[limit])`

## 参数

**obj** 可以是向量、矩阵或表。

**limit** 是正整数，表示需要填充的 NULL 值的数量。

## 详情

* + 如果 *obj* 是一个向量，使用 NULL 值前的非空元素来填充 NULL
    值。
  + 如果 *obj* 是一个矩阵或表，对于表中的每一列，使用 NULL
    值前的非空元素来填充 NULL 值。

注意：

该函数会改变输入的对象；而函数 `ffill` 会生成新的对象，不会改变输入的对象。

## 例子

例1.

```
x=1 2 3 NULL NULL NULL 4 5 6
x.ffill!();
x;
// x 中的空值被填充了
[1,2,3,3,3,3,4,5,6]
```

例2. 通过 *limit* 参数，指定需要填充 1 个NULL值：

```
x=1 2 3 NULL NULL NULL 4 5 6
x.ffill!(1);
// output
[1,2,3,3,,,4,5,6]
```

例3. *obj* 指定为一个表

```
date=[2012.06.12,,2012.06.13,2012.06.14,2012.06.15]
sym=["IBM","MSFT","IBM","MSFT","MSFT"]
price=[40.56,26.56,,,50.76]
qty=[2200,4500,1200,5600,]
timestamp=[09:34:07,,09:36:42,09:36:51,09:36:59]
t=table(date,timestamp,sym,price,qty);

ffill!(t);
t;
```

输出返回：

| date | timestamp | sym | price | qty |
| --- | --- | --- | --- | --- |
| 2012.06.12 | 09:34:07 | IBM | 40.56 | 2200 |
| 2012.06.12 | 09:34:07 | MSFT | 26.56 | 4500 |
| 2012.06.13 | 09:36:42 | IBM | 26.56 | 1200 |
| 2012.06.14 | 09:36:51 | MSFT | 26.56 | 5600 |
| 2012.06.15 | 09:36:59 | MSFT | 50.76 | 5600 |

