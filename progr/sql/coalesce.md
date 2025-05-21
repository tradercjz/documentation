# coalesce

## 语法

`coalesce(X1, X2, args...)`

## 参数

* **X1** 标量或向量。
* **X2** 与 *X1* 类型相同的标量/向量。若 *X1*
  为标量，*X2* 只能为标量；若 *X1* 为向量，*X2* 可以为非空的标量，也可以为与
  *X1* 等长的向量。
* **args** 可选参数，参数说明同 *X2*。

## 详情

根据给定的数据，填充原始数据中的空值，返回一个和原始数据等长的标量/向量。

注： 支持在分布式查询中使用。

逐一检查 X1 中的元素：

* 若非空，则直接返回。
* 若为空，则检查 X2 中相同位置的元素是否为空；若为空，则按照相同的规则检查后续 args
  中相同位置的元素是否为空，直到找到第一个非空值并返回，若找不到则返回空。

## 使用场景

* 将表的多列合并为一列。
* 替代复杂的 `case` 表达式：`select
  coalesce (expr1, expr2, 1) from t` 等效于 `select case
  when vol1 is not null then vol1 when vol2 is not null then vol2 else
  1 end from t`

## 例子

```
coalesce(int(NULL), int(NULL), 1, 3)
1

coalesce(-1 NULL 4 3, NULL 2 NULL 1, 1 4 5 2)
[-1,2,4,3]

vol1 = [3.3, 2.2, 2.1, NULL, 1.2]
vol2 = [NULL, 1.8, 1.9, 2.3, 3.2]
sym = `a`a`b`a`c
t = table(sym, vol1, vol2)

select sym, coalesce(vol1, vol2) as vol from t
```

| sym | vol |
| --- | --- |
| a | 3.3 |
| a | 2.2 |
| b | 2.1 |
| a | 2.3 |
| c | 1.2 |

