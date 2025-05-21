# bar

## 语法

`bar(X, interval, [closed='left'])`

相关函数：[dailyAlignedBar](../d/dailyAlignedBar.html)

## 参数

**X** 是一个整型/时间类型的标量或向量。

**interval** 是一个大于0的整型/DURATION 类型的标量或和 *X* 长度相同的向量。

*interval* 是 DURATION 类型时，支持以下时间单位（区分大小写）：w, d, H, m, s, ms,
us, ns。

注： 由于 *interval* 不支持年(y)和月(M)的时间单位，如果需要对
*X* 以年或月进行分组时，可以调用 [year](../y/year.html) 或 [month](../m/month.html) 对 *X* 进行转换后，指定 *interval*
为整数进行计算。可以参考例2。

**closed** 字符串，可选值为 'left' 或 'right'。 表示 *X* 中可被
*interval*
整除的元素，归为某个分组的左边界（即该组第一个元素，此时*closed*=‘left’），还是归为某个分组的右边界（即该组最后一个元素，此时*closed*=‘right’）。

对应的分组计算公式为：

*closed* = 'left'时，*X*-(*X* %
*interval*)，表示将余数为 0 的值作为一个分组的左边界。

*closed* = 'right'时，iif((*X* % *interval*) == 0,
*X*, *X* + (*interval*-(*X* % *interval*)))，表示将余数为 0
的值作为一个分组的右边界。

## 详情

`bar` 基于 *interval* 指定的长度，根据分组计算公式，对 *X*
进行分组。它返回一个和 *X* 具有相同长度的向量。

## 例子

例1.

```
bar(100,3);               // 100-(100%3)=100-1=99
// output
99

bar(0..15, 3)
// output
[0,0,0,3,3,3,6,6,6,9,9,9,12,12,12,15]

x=[7,4,5,8,9,3,3,5,2,6,12,1,0,-5,32]
bar(x, 5)
// output
[5,0,5,5,5,0,0,5,0,5,10,0,0,-5,30]

t=table(2021.01.01T01:00:00..2021.01.01T01:00:29 as time, rand(1.0, 30) as x)
select max(x) from t group by bar(time,5s)
```

| bar\_time | max\_x |
| --- | --- |
| 2021.01.01T01:00:00 | 0.539024 |
| 2021.01.01T01:00:05 | 0.793327 |
| 2021.01.01T01:00:10 | 0.958522 |
| 2021.01.01T01:00:15 | 0.96987 |
| 2021.01.01T01:00:20 | 0.827086 |
| 2021.01.01T01:00:25 | 0.617353 |

例2. 以3个月进行分组，需要将 `bar` 函数中的 *X* 转为月份：

```
t=table(take(2018.01.01T01:00:00+1..10,10) join take(2018.02.01T02:00:00+1..10,10) join take(2018.03.01T08:00:00+1..10,10) join take(2018.04.01T08:00:00+1..10,10) join take(2018.05.01T08:00:00+1..10, 10) as time, rand(1.0, 50) as x)
select max(x) from t group by bar(month(time), 3);
```

| bar | max\_x |
| --- | --- |
| 2018.01M | 0.9868 |
| 2018.04M | 0.9243 |

例3. 将日期按照周分组，计算每周的最大值。根据 *closed* 不同，计算结果有所区别。

```
t=table(2022.01.01 + 1..20  as time, rand(100, 20) as x)
```

| time | x |
| --- | --- |
| 2022.01.02 | 6 |
| 2022.01.03 | 29 |
| 2022.01.04 | 71 |
| 2022.01.05 | 56 |
| 2022.01.06 | 93 |
| 2022.01.07 | 34 |
| 2022.01.08 | 77 |
| 2022.01.09 | 18 |
| 2022.01.10 | 62 |
| 2022.01.11 | 33 |
| 2022.01.12 | 34 |
| 2022.01.13 | 64 |
| 2022.01.14 | 80 |
| 2022.01.15 | 63 |
| 2022.01.16 | 17 |
| 2022.01.17 | 66 |
| 2022.01.18 | 85 |
| 2022.01.19 | 27 |
| 2022.01.20 | 77 |
| 2022.01.21 | 27 |

```
select max(x) from t group by bar(time, 7d);
```

| bar\_time | max\_x |
| --- | --- |
| 2021.12.30 | 71 |
| 2022.01.06 | 93 |
| 2022.01.13 | 85 |
| 2022.01.20 | 77 |

```
print  select max(x) from t group by bar(time, 7d, closed='right');
```

| bar\_time | max\_x |
| --- | --- |
| 2021.01.06 | 93 |
| 2022.01.13 | 77 |
| 2022.01.20 | 85 |
| 2022.01.27 | 27 |

例4. 计算分钟 k 线时，n 需要转换为 NANOTIMESTAMP，此时若使用整型计算可能造成类型溢出，需要将数据类型转换成
LONG。

```
n = 1000000
nano = (09:30:00.000000000 + rand(long(6.5*60*60*1000000000), n)).sort!()
price = 100+cumsum(rand(0.02, n)-0.01)
volume = rand(1000, n)
symbol = rand(`600519`000001`600000`601766, n)
tradeNano = table(symbol, nano, price, volume).sortBy!(`symbol`nano)
undef(`nano`price`volume`symbol)
barMinutes = 7
itv = barMinutes*60*long(1000000000)

OHLC_nano=select first(price) as open, max(price) as high, min(price) as low, last(price) as close, sum(volume) as volume from tradeNano group by symbol, bar(nano, itv) as barStart
```

