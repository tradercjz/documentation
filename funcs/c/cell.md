# cell

## 语法

`cell(obj, row, col)`

## 参数

**obj** 矩阵或表。

**row** 非负整数，表示行坐标。

**col** 非负整数，表示列坐标。

## 详情

返回一个位于对应行列的标量，等价于 `obj[row, col]`。*cell* 函数通常比
`obj[row, col]` 运行地更快。

## 例子

```
x=(1..6).reshape(3:2);
x;
```

| 0 | 1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
x.cell(0,0);
// output
1
x.cell(0,1);
// output
4
cell(x,1,1);
// output
5

cell(x,2,0);
// output
3
```

