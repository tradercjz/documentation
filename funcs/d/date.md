# date

## 语法

`date(X)`

## 详情

返回对应的日期。返回值的类型是 DATE，一个时间值。如果参数 *X* 不是日期，则返回值是 1970.01.01 +
*X* 天的日期。

## 参数

**X** 可以是时间标量、向量或整数。

## 例子

```
date();
```

返回：null

```
date(1)
```

返回：1970.01.02

```
date(`2011.10.12);
```

返回：2011.10.12

```
date(now());
```

返回：2024.02.22

```
date 2012.12.03 01:22:01;
```

返回：2012.12.03

```
date(2016.03M);
```

返回：2016.03.01

**相关信息**

* [second](../s/second.html "second")
* [minute](../m/minute.html "minute")
* [month](../m/month.html "month")
* [hour](../h/hour.html "hour")
* [year](../y/year.html "year")

