# cumfirstNot

## 语法

`cumfirstNot(X, [k])`

参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.md)

## 参数

**k** 一个标量。

## 详情

* 若 *X* 是向量：

  + 如果没有指定 *k*，对 *X* 内的每个元素，返回其之前所有元素中第一个不为 NULL 的元素。
  + 如果指定 *k*，对 *X* 内的每个元素，返回其之前所有元素中第一个不为 *k* 的元素。
* 若 *X* 是矩阵，在每列内进行上述计算，返回一个与 *X* 维度相同的矩阵。

## 例子

```
x=[NULL,1,2,6,NULL,3,4,NULL]
cumfirstNot(x);
// output
[,1,1,1,1,1,1,1]

cumfirstNot(x, 1)
// output
[,,2,2,2,2,2,2]

m=matrix(1 2 3 NULL 4, NULL NULL 8 8 9);
m;
```

| #0 | #1 |
| --- | --- |
| 1 |  |
| 2 |  |
| 3 | 8 |
|  | 8 |
| 4 | 9 |

```
cumfirstNot(m);
```

| #0 | #1 |
| --- | --- |
| 1 |  |
| 1 |  |
| 1 | 8 |
| 1 | 8 |
| 1 | 8 |

相关函数： [firstNot](../f/firstNot.md)

