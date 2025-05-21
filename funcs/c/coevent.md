# coevent

## 语法

`coevent(event, eventTime, window, [orderSensitive=false])`

## 参数

**event** 是一个向量，表示事件。

**eventTime** 是一个时间类型或整型类型的向量，表示事件发生时间。它的长度必须与 *event* 相同。

**window** 是一个非负整数，表示时间间隔长度。

**orderSensitive** 是一个可选的布尔值，表示是否区分两个事件的先后顺序。默认值是 false。

## 详情

统计给定的时间间隔内出现事件对的次数。如果 *eventTime* 中包含 NULL 值，系统会忽略这条记录。

返回的结果是一个表，包含 event1, event2 和 hits 三个字段。event1 和 event2 的数据类型与
*event* 相同，hits 是整数，表示事件对出现的次数。

## 例子

下例中，sensor\_id 与 time 分别为发现异常的传感器编号以及发现异常时刻。使用
`coevent` 函数统计2秒钟内两个传感器同时出现异常的次数。

```
sensor_id=`A`B`C`D`C`A`B
time=[2012.06.13T12:30:00,2012.06.13T12:30:02,2012.06.13T12:30:04,2012.06.13T12:30:05,2012.06.13T12:30:06,2012.06.13T12:30:09,2012.06.13T12:30:10];

coevent(sensor_id, time, 2);
```

| event1 | event2 | hits |
| --- | --- | --- |
| B | C | 1 |
| C | D | 2 |
| C | C | 1 |
| A | B | 2 |

```
coevent(sensor_id, time, 2, true);
```

| event1 | event2 | hits |
| --- | --- | --- |
| C | C | 1 |
| B | C | 1 |
| C | D | 1 |
| D | C | 1 |
| A | B | 2 |

