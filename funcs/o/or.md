# or

## 语法

`or(X, Y)` 或 `X||Y`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量或矩阵。

## 详情

按元素逐个返回 *X* 逻辑或 `(OR)Y` 的结果。

注意：若 `or` 或 `||` 的操作数包含 NULL 时，||
返回的对应结果为 NULL，而 `or` 针对不同 server 版本，返回的结果不同。

* 对于小于 2.00.9.4 的版本，`or` 返回的对应结果为 NULL。
* 对于 2.00.9.4 及以上版本，`or` 返回的结果由配置项
  *logicOrIgnoreNull* 控制，见下表：

| 操作数 | 操作数 | 返回值（*logicOrIgnoreNull*= true 时） | 返回值（*logicOrIgnoreNull*= false 时） |
| --- | --- | --- | --- |
| 非零 | NULL | true | NULL |
| 零 | NULL | true | NULL |
| NULL | NULL | true | NULL |

## 例子

```
1 || 0;
```

输出返回：true

```
x=1 0 1;
x || 0;
```

输出返回：[true,false,true]

```
y=0 1 0;
x or y;
```

输出返回：[true,true,true]

```
t=table(1..3 as id, 4..6 as value);
t;
```

输出返回：

| id | value |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
select id, value from t where id=2 or id=3;
```

输出返回：

| id | value |
| --- | --- |
| 2 | 5 |
| 3 | 6 |

相关函数：[and](../a/and.md), [not](../n/not.md)

