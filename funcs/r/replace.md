# replace

## 语法

`replace(X, oldValue, newValue)`

## 参数

**X** 可以是向量、矩阵。

**oldValue** 标量，与 *X/newValue* 具有相同数据类别，表示将被替换的值。

**newValue** 标量，与 *X/oldValue* 具有相同数据类别，表示新的值。

## 详情

返回将 *oldValue* 替换成 *newValue*
后的向量或矩阵。`replace!` 是 `replace` 的原地改变版本。

## 例子

```
x=1 1 3;
x=x.replace(1,2);
x
// output
[2,2,3];

m=1..4$2:2;
m
```

| #0 | #1 |
| --- | --- |
| 1 | 3 |
| 2 | 4 |

```
m=m.replace(2,1);
m
```

| #0 | #1 |
| --- | --- |
| 1 | 3 |
| 1 | 4 |

```
m.replace!(1,6);
```

| #0 | #1 |
| --- | --- |
| 6 | 3 |
| 6 | 4 |

