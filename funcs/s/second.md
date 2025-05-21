# second

## 语法

`second(X)`

## 详情

返回对应的秒数，返回值的类型是 SECOND，一个时间值。

## 参数

**X** 可以是整数/时间类型/字符串类型的标量或向量。

## 例子

```
second();
```

返回：null

```
second(1)
```

返回：00:00:01

```
second("19:36:12");
```

返回：19:36:12

```
second(now());
```

返回：16:01:32

```
second 2012.12.03 01:22:01;
```

返回：01:22:01

```
second(61);
```

返回：00:01:01

```
second("09:00:01")
```

返回：09:00:01

**相关信息**

* [minute](../m/minute.html "minute")
* [hour](../h/hour.html "hour")
* [date](../d/date.html "date")
* [month](../m/month.html "month")
* [year](../y/year.html "year")

