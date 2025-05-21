# dailyAlignedBar

## 语法

`dailyAlignedBar(X, timeOffset, n, [timeEnd],
[mergeSessionEnd=false])`

相关函数：[bar](../b/bar.html)

## 参数

**X** 时间类型向量，支持以下的类型：SECOND, TIME, NANOTIME, DATETIME, TIMESTAMP 或
NANOTIMESTAMP。

**timeOffset** 标量或向量，表示每个时段的起始时刻。与 *X* 精度一致，可以是 SECOND、TIME 或 NANOTIME
类型的标量或向量。如果 *timeOffset* 是一个向量，它必须是递增的。

**n** 是一个正整数或 DURATION 类型数据，表示时间区间长度。 *n* 取正整数时，其单位为 *timeOffset* 的最小精度。
*n* 取 DURATION 类型数据时，其单位不能是 y, M, w, d, B。

**timeEnd** 可选参数，表示每个时段的结束时刻。和 timeOffset 的类型和长度必须一致。

**mergeSessionEnd** 为可选参数，是一个布尔值，表示若某个时段的最后时刻为某个区间的起始时刻，是否将其并入之前的区间。默认值为
false。

## 详情

按照给定的起始时刻 *timeOffset* （与结束时刻 *timeEnd* ）以及时间区间长度（由 *n* 指定），划分时间区间，返回
*X* 中每个元素所属的时间区间起始时刻，结果为与 *X* 长度相同的向量。具体而言，对于 *X* 中的每个元素，计算
X-((X-timeOffset)%n)。

时间区间一般包括左边界，不包括右边界。但若指定 *mergeSessionEnd* =
true，且某个时段的最后时刻为某个区间的起始时刻，则将其并入之前的区间。

该函数支持隔夜时段。

## 例子

以下例子中均使用了随机模拟数据。结果中的 price 列之值每次执行均会有所不同。

例1. 中国股票市场每天有两个交易时段：上午9:30-11:30和下午1:00-3:00。计算每个交易时段中的60分钟均价。

```
sessionsBegin = 09:30:00 13:00:00
ts = 2019.11.01T09:30:00..2019.11.01T11:30:00 join 2019.11.01T13:00:00..2019.11.01T15:00:00
t = table(ts, rand(10.0, size(ts)) as price);

select avg(price) as price, count(*) as count from t group by dailyAlignedBar(ts, sessionsBegin, 60*60) as k60;
```

| k60 | price | count |
| --- | --- | --- |
| 2019.11.01T09:30:00 | 5.031685383252463 | 3600 |
| 2019.11.01T10:30:00 | 5.022667285786399 | 3600 |
| 2019.11.01T11:30:00 | 4.930270051117987 | 1 |
| 2019.11.01T13:00:00 | 4.931854071494632 | 3600 |
| 2019.11.01T14:00:00 | 4.979529541734115 | 3600 |
| 2019.11.01T15:00:00 | 0.961996954865754 | 1 |

由于每个区间包括左边界，不包括右边界，若每个交易时段的结束时刻（上午11:30与下午3:00）恰好是区间边界，若不指定
*timeEnd* 与
*mergeSessionEnd*，则时段的结束时刻会单独作为一区间，如上例所示。多数情况下，会希望此类结束时刻归入前一区间。可参照以下脚本。

```
sessionsEnd = 11:30:00 15:00:00;
select avg(price) as price, count(*) as count from t group by dailyAlignedBar(ts, sessionsBegin, 60*60, sessionsEnd, true) as k60;
```

| k60 | price | count |
| --- | --- | --- |
| 2019.11.01T09:30:00 | 5.031685383252463 | 3600 |
| 2019.11.01T10:30:00 | 5.022641627015316 | 3601 |
| 2019.11.01T13:00:00 | 4.931854071494632 | 3600 |
| 2019.11.01T14:00:00 | 4.978413870368697 | 3601 |

例2. 隔夜时段。期货市场每天有两个交易时段：下午1:30-4:30和晚上10:30-凌晨2:30。使用
`dailyAlignedBar` 函数计算每个交易时段中的7分钟均价。

```
sessions = 13:30:00 22:30:00
ts = 2019.11.01T13:30:00..2019.11.01T16:30:00 join 2019.11.01T22:30:00..2019.11.02T02:30:00
ts = ts join (ts+60*60*24)
t = table(ts, rand(10.0, size(ts)) as price)
select avg(price) as price, count(*) as count from t group by dailyAlignedBar(ts, sessions, 7m) as k7;
```

例3. 计算分钟 k 线时，*n* 需要转换为
NANOTIMESTAMP，此时若使用整型计算可能造成类型溢出，需要将数据类型转换成 LONG。

```
n = 1000000
nano=(09:30:00.000000000 + rand(long(6.5*60*60*1000000000), n)).sort!()
sessionStartNano=09:30:00.000000000
price = 100+cumsum(rand(0.02, n)-0.01)
volume = rand(1000, n)
symbol = rand(`600519`000001`600000`601766, n)
tradeNano=table(symbol, nano, price, volume).sortBy!(`symbol`nano)
undef(`nano`price`volume`symbol)
barMinutes=7
itv = barMinutes*60*long(1000000000)

OHLC_nano=select first(price) as open, max(price) as high, min(price) as low, last(price) as close, sum(volume) as volume from tradeNano group by symbol, dailyAlignedBar(nano, sessionStartNano, itv) as barStart

```

