# rowNames

## 语法

`rowNames(X)`

## 参数

**X** 是一个矩阵

## 详情

返回矩阵 *X* 的行名。参见相关函数： [columnNames](../c/columnNames.md)

## 例子

```
x=1..6$2:3;
x
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
x.rename!(1 2, `a`b`c);
```

|  | a | b | c |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 5 |
| 2 | 2 | 4 | 6 |

```
rowNames x;
// output
[1,2]
```

