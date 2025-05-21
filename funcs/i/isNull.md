# isNull

## 语法

`isNull(X)`

## 参数

**X** 可以是标量、数据对、向量、字典、矩阵或内存表。

## 详情

用于检查是否是 NULL 值。如果元素是 NULL，返回 true。

注： 自 2.00.5 版本开始，当 *X* 是字典、元组、数据向量或表时，该函数将检查每一行中的元素是否是
NULL 值，返回一个具有相同维度的字典、元组或表。

## 例子

```
isNull(00i);
// output
true

isNull(1 NULL NULL 6 NULL 7);

[0,1,1,0,1,0]

isNull(1/0);
// output
true

x=1 NULL 5 NULL 4 6$2:3;
x;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 5 | 4 |
|  |  | 6 |

```
isNull(x);
```

| #0 | #1 | #2 |
| --- | --- | --- |
| false | false | false |
| true | true | false |

```
t=table(1 2 3 as id, `a`b`c as name, 10 NULL 7 as vol)
isNull(t)
```

| id | name | vol |
| --- | --- | --- |
| false | false | false |
| false | false | true |
| false | false | false |

相关函数：[hasNull](../h/hasNull.md), [nullFill](../n/nullFill.md)

