# signum

## 语法

`signum(X)`

别名：sign

## 参数

**X** 是布尔值或数值类型的标量、向量或矩阵。

## 详情

返回 *X* 的符号标志。如果 *X* 为正数，返回1； 如果 *X* 为0，返回0；如果
*X* 为负数，返回-1；如果 *X* 中元素为 NULL，则返回 NULL。

## 例子

```
signum(8.2 0 -6 NULL);
// output
[1,0,-1, ]
```

