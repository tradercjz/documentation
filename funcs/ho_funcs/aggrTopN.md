# aggrTopN

## 语法

`aggrTopN(func, funcArgs, sortingCol, top, [ascending=true])`

## 参数

* **func** 必须是一个聚合函数。
* **funcArgs** 是 *func* 的参数，可以是标量或向量。 *func* 有多个参数时，它是一个元组。
* **sortingCol** 是一个数值类型或时间类型的向量，提供 *funcArgs* 的排序指标。
* **top** 可以是整数或者浮点数。

  + 如果是整数，表示选取的前 *top* 行数据；
  + 如果是浮点数，表示百分比，必须小于1.0。根据 *funcArgs* 的总行数 *top*
    来确定需要选取的行数。若结果不是整数，则向下取整，至少取一行。
* **ascending** 是一个布尔值，表示是否按升序排序。 默认值是 true。

其他相关 TopN 系列函数参数说明和窗口计算规则请参考: [TopN](../themes/TopN.html)

## 详情

将 *sortingCol* 根据 *ascending* 指定方式进行排序后，得到 *funcArgs* 中对应的前 *top*
个元素，使用 *func* 指定的聚合函数进行计算。*sortingCol* 包含的 NULL 值当作最小值处理。

## 例子

```
aggrTopN(func=sum, funcArgs=1 2 3 4 5, sortingCol=5 1 2 3 4, top=3, ascending=false)
// output
10

aggrTopN(func=corr,funcArgs=[1..5, 3 9 4 2 5], sortingCol=2 3 4 5 3, top=3)
// output
0.052414
```

*top* =3，aggrTopN严格取前3个元素进行计算，下例中有3个3对应第三位，只取满足 *top* 数量的值进行计算

```
aggrTopN(func=min,funcArgs=1 6 4 -6 4 5, sortingCol=2 3 3 3 4 5, top=3)
// output
1
```

计算每个股票每天最大交易量前25%的交易平均价格。

```
t = table(`A`A`A`B`B`B`B`B`B`B`B as sym, 09:30:06 09:30:28 09:31:46 09:31:59 09:30:19 09:30:43 09:31:23 09:31:56 09:30:44 09:31:25 09:31:57 as time, 10 20 10 30 20 40 30 30 30 20 40 as volume, 10.05 10.06 10.07 10.05 20.12 20.13 20.14 20.15 20.12 20.13 20.16 as price);
t;
```

| sym | time | volume | price |
| --- | --- | --- | --- |
| A | 09:30:06 | 10 | 10.05 |
| A | 09:30:28 | 20 | 10.06 |
| A | 09:31:46 | 10 | 10.07 |
| B | 09:31:59 | 30 | 10.05 |
| B | 09:30:19 | 20 | 20.12 |
| B | 09:30:43 | 40 | 20.13 |
| B | 09:31:23 | 30 | 20.14 |
| B | 09:31:56 | 30 | 20.15 |
| B | 09:30:44 | 30 | 20.12 |
| B | 09:31:25 | 20 | 20.13 |
| B | 09:31:57 | 40 | 20.16 |

```
select aggrTopN(func=avg, funcArgs=price, sortingCol=volume, top=0.25, ascending=false) from t group by sym, time
```

| sym | time | aggrTopN\_avg |
| --- | --- | --- |
| A | 09:30:06 | 10.05 |
| A | 09:30:28 | 10.06 |
| A | 09:31:46 | 10.07 |
| B | 09:30:19 | 20.12 |
| B | 09:30:43 | 20.13 |
| B | 09:30:44 | 20.12 |
| B | 09:31:23 | 20.14 |
| B | 09:31:25 | 20.13 |
| B | 09:31:56 | 20.15 |
| B | 09:31:57 | 20.16 |
| B | 09:31:59 | 10.05 |

