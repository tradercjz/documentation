# window join

## 语法

### 窗口连接

```
wj(leftTable, rightTable, window, aggs, matchingCols, [rightMatchingCols])
```

### 现行窗口连接

```
pwj(leftTable, rightTable, window, aggs, matchingCols, [rightMatchingCols])
```

## 参数

* **leftTable** 和 **rightTable** 是连接的表。

  注： *rightTable* 不能是分布式表。
* **window** 是表示与左表记录有关的窗口边界的整型数据对或 DURATION 数据对，其中左右边界都包含在内。
* **aggs** 表示聚合函数的元代码，详情请参考 [元编程](../objs/meta_progr.html)，支持输入元组。聚合函数中的参数必须是右表中的数值类型列。支持输出右表字段的不定长 array vector。
* **matchingCols** 是表示连接列的字符串标量或向量。
* **rightMatchingCols** 是表示右表连接列的字符串标量或向量。当 *leftTable* 和
  *rightTable* 至少有一个连接列不同时，必须指定
  *rightMatchingCols*。返回结果中的连接列与左表的连接列名称相同。

## 详情

window join 是 asof join 的扩展。与 asof join 一样：

* 如果只有 1 个连接列，则 window join 假定右表已按照连接列排过序；
* 如果有多个连接列，则 window join
  假定右表根据除最后一个连接列外的其他连接列定义分组，每个分组根据最后一个连接列排序。右表的其他连接列不需要排序；
* 如果这些条件不符合，处理将与期望值不符。左表不需要排序。

与 asof join 一样，使用 `wj` 关联分区表时，用于分组的关联字段必须包含全部分区字段。

如果 *window* = w1:w2，左表的 *matchingCols* 中最后一个连接列对应的每一行记录为
t，在右表中找到与其他连接列对应的记录行以及与最后一个连接列对应并且在 (t+w1) 到 (t+w2) 之间的值，然后把聚合函数应用到右表选中的行。

`wj` 和 `pwj` 的区别是：

* 如果右表没有与 t+w1（窗口左边界）匹配的值， `wj` 的窗口左边界值为空，而 `pwj`
  会选择 (t+w1) 前的最后一个值，将其并入窗口。
* 如果右表有多个与 t+w1（窗口左边界）匹配的值时， `wj` 的窗口会包含所有重复的值，而
  `pwj` 只包含最后一行。

如果 *window* = 0:0 ，右表的计算窗口将由左表两条数据的时间戳决定。假设左表某一条记录时间戳为
t，上一条记录的时间戳为 t0，则右表根据 *matchingCols* 其他列匹配后的计算窗口为 [t0, t)。

以下聚合函数经过优化，使得它们在 window join 中的计算速度更快: [avg](../../funcs/a/avg.html), [beta](../../funcs/b/beta.html), [count](../../funcs/c/count.html), [corr](../../funcs/c/corr.html), [covar](../../funcs/c/covar.html), [first](../../funcs/f/first.html), [last](../../funcs/l/last.html), [max](../../funcs/m/max.html), [med](../../funcs/m/med.html), [min](../../funcs/m/min.html), [percentile](../../funcs/p/percentile.html), [std](../../funcs/s/std.html), [sum](../../funcs/s/sum.html), [sum2](../../funcs/s/sum2.html), [var](../../funcs/v/var.html), [wavg](../../funcs/w/wavg.html), [kurtosis](../../funcs/k/kurtosis.html), [prod](../../funcs/p/prod.html), [skew](../../funcs/s/skew.html), [stdp](../../funcs/s/stdp.html),[varp](../../funcs/v/varp.html), [atImin](../../funcs/a/atImin.html), [atImax](../../funcs/a/atImax.html)

注： 在 window join 中，当 *aggs* 中使用 atImax 和 atImin
进行计算时，如果计算窗口内中有多个相同的最值，默认取最大索引值对应的记录。

## 例子

例1. 基础功能示例

```
t1 = table(`A`A`B as sym, 09:56:06 09:56:07 09:56:06 as time, 10.6 10.7 20.6 as price)
t2 = table(take(`A,10) join take(`B,10) as sym, take(09:56:00+1..10,20) as time, (10+(1..10)\10-0.05) join (20+(1..10)\10-0.05) as bid, (10+(1..10)\10+0.05) join (20+(1..10)\10+0.05) as offer, take(100 300 800 200 600, 20) as volume);
t1;
```

| sym | time | price |
| --- | --- | --- |
| A | 09:56:06 | 10.6 |
| A | 09:56:07 | 10.7 |
| B | 09:56:06 | 20.6 |

```
t2;
```

| sym | time | bid | offer | volume |
| --- | --- | --- | --- | --- |
| A | 09:56:01 | 10.05 | 10.15 | 100 |
| A | 09:56:02 | 10.15 | 10.25 | 300 |
| A | 09:56:03 | 10.25 | 10.35 | 800 |
| A | 09:56:04 | 10.35 | 10.45 | 200 |
| A | 09:56:05 | 10.45 | 10.55 | 600 |
| A | 09:56:06 | 10.55 | 10.65 | 100 |
| A | 09:56:07 | 10.65 | 10.75 | 300 |
| A | 09:56:08 | 10.75 | 10.85 | 800 |
| A | 09:56:09 | 10.85 | 10.95 | 200 |
| A | 09:56:10 | 10.95 | 11.05 | 600 |
| B | 09:56:01 | 20.05 | 20.15 | 100 |
| B | 09:56:02 | 20.15 | 20.25 | 300 |
| B | 09:56:03 | 20.25 | 20.35 | 800 |
| B | 09:56:04 | 20.35 | 20.45 | 200 |
| B | 09:56:05 | 20.45 | 20.55 | 600 |
| B | 09:56:06 | 20.55 | 20.65 | 100 |
| B | 09:56:07 | 20.65 | 20.75 | 300 |
| B | 09:56:08 | 20.75 | 20.85 | 800 |
| B | 09:56:09 | 20.85 | 20.95 | 200 |
| B | 09:56:10 | 20.95 | 21.05 | 600 |

```
wj(t1, t2, -5s:0s, <avg(bid)>, `sym`time);
```

| sym | time | price | avg\_bid |
| --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.3 |
| A | 09:56:07 | 10.7 | 10.4 |
| B | 09:56:06 | 20.6 | 20.3 |

```
wj(t1, t2, -5:-1, <[wavg(bid,volume), wavg(offer,volume)]>, `sym`time);
```

| sym | time | price | wavg\_bid | wavg\_offer |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.295 | 10.395 |
| A | 09:56:07 | 10.7 | 10.32 | 10.42 |
| B | 09:56:06 | 20.6 | 20.295 | 20.395 |

```
t3=t2
t3.rename!(`time, `second)
wj(t1, t3, -2:2, <[wavg(bid,volume), wavg(offer,volume)]>, `sym`time, `sym`second);
```

| sym | time | price | wavg\_bid | wavg\_offer |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.595 | 10.695 |
| A | 09:56:07 | 10.7 | 10.645 | 10.745 |
| B | 09:56:06 | 20.6 | 20.595 | 20.695 |

计算市场上买入价和卖出价之间的平均差占卖出价平均值的比例。

```
wj(t1, t2, -5s:0s, <avg(offer-bid)/avg(offer)>, `sym`time);
```

| sym | time | price | avg\_bid\_div |
| --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 0.0096 |
| A | 09:56:07 | 10.7 | 0.0095 |
| B | 09:56:06 | 20.6 | 0.0049 |

*window join是asof join的扩展：*

```
wj(t1, t2, -100:0, <[last(bid) as bid, last(offer) as offer]>, `sym`time);
```

| sym | time | price | bid | offer |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.55 | 10.65 |
| A | 09:56:07 | 10.7 | 10.65 | 10.75 |
| B | 09:56:06 | 20.6 | 20.55 | 20.65 |

```
select sym, time, price, bid, offer from aj(t1, t2, `sym`time);
```

| sym | time | price | bid | offer |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.55 | 10.65 |
| A | 09:56:07 | 10.7 | 10.65 | 10.75 |
| B | 09:56:06 | 20.6 | 20.55 | 20.65 |

*prevailing window join：*

```
delete from t2 where 09:56:04<=time<=09:56:06;
t2;
```

| sym | time | bid | offer | volume |
| --- | --- | --- | --- | --- |
| A | 09:56:01 | 10.05 | 10.15 | 100 |
| A | 09:56:02 | 10.15 | 10.25 | 300 |
| A | 09:56:03 | 10.25 | 10.35 | 800 |
| A | 09:56:07 | 10.65 | 10.75 | 300 |
| A | 09:56:08 | 10.75 | 10.85 | 800 |
| A | 09:56:09 | 10.85 | 10.95 | 200 |
| A | 09:56:10 | 10.95 | 11.05 | 600 |
| B | 09:56:01 | 20.05 | 20.15 | 100 |
| B | 09:56:02 | 20.15 | 20.25 | 300 |
| B | 09:56:03 | 20.25 | 20.35 | 800 |
| B | 09:56:07 | 20.65 | 20.75 | 300 |
| B | 09:56:08 | 20.75 | 20.85 | 800 |
| B | 09:56:09 | 20.85 | 20.95 | 200 |
| B | 09:56:10 | 20.95 | 21.05 | 600 |

```
wj(t1, t2, -1:1, <[first(bid), avg(offer)]>, `sym`time);
```

| sym | time | price | first\_bid | avg\_offer |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.65 | 10.75 |
| A | 09:56:07 | 10.7 | 10.65 | 10.8 |
| B | 09:56:06 | 20.6 | 20.65 | 20.75 |

例2. 以 tuple 方式动态传参给 aggs。

```
aggs = array(ANY, 3)   //定义一个包含元代码的aggs元组
aggs[0] = <min(bid)>
aggs[1] = <min(offer)>
aggs[2] = <min(volume)>
wj(t1, t2, -5s:0s, aggs, `sym`time);
```

| sym | time | price | min\_bid | min\_offer | min\_volume |
| --- | --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.05 | 10.15 | 100 |
| A | 09:56:07 | 10.7 | 10.15 | 10.25 | 100 |
| B | 09:56:06 | 20.6 | 20.05 | 20.15 | 100 |

例3. pwj 函数示例

```
pwj(t1, t2, -1:1, <[first(bid), avg(offer)]>, `sym`time);
```

| sym | time | price | first\_bid | avg\_offer |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.25 | 10.55 |
| A | 09:56:07 | 10.7 | 10.25 | 10.65 |
| B | 09:56:06 | 20.6 | 20.25 | 20.55 |

在上面的例子中，以左表的第一条记录为例，wj 和 pwj 会在右表中查找 (09:56:06-1) 到 (09:56:06+1) 的数据，wj 使用右表 sym 列中
"A" 在 09:56:07 的数据来计算 first(bid) 和 avg(offer)，然而 `pwj` 使用的是右表 sym 列中
"A" 在 09:56:03 和 09:56:07 的数据。

特殊用法：

```
wj(t1, t2, 0:0, <[last(bid), bid]>, `sym`time)
```

返回：

| sym | time | price | last\_bid | bid |
| --- | --- | --- | --- | --- |
| A | 09:56:06 | 10.6 | 10.45 | [10.05, 10.15, 10.25, 10.35, 10.45] |
| A | 09:56:07 | 10.7 | 10.55 | [10.55] |
| B | 09:56:06 | 20.6 | 20.45 | [20.05, 20.15, 20.25, 20.35, 20.45] |

