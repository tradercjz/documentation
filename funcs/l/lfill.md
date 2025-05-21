# lfill

## 语法

`lfill(obj)`

## 参数

**obj** 是数值型向量或只包含数值类型的表。

## 详情

* 如果 *obj* 是向量，线性填充两个非空元素之间的 NULL值。
* 如果 *obj* 是表，对于表中的每一列，线性填充两个非空元素之间的 NULL 值。

`lfill` 不会改变向量的值，[lfill!](lfill_.md) 会改变向量的值。

## 例子

```
a= NULL 1.5 NULL NULL 4.5
a.lfill();
// output
[NULL,1.5,2.5,3.5,4.5]

b=1 NULL NULL 6
b.lfill();
// output
[1,3,4,6]

t=table(1 NULL NULL 4 5 6 as id,2.1 2.2 NULL NULL 2.4 2.6 as val);
select * from lfill(t);
```

| id | val |
| --- | --- |
| 1 | 2.1 |
| 2 | 2.2 |
| 3 | 2.266667 |
| 4 | 2.333333 |
| 5 | 2.4 |
| 6 | 2.6 |

相关函数：[bfill](../b/bfill.md), [bfill!](../b/bfill_.md), [lfill!](lfill_.md)

