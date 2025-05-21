# oneHot

## 语法

`oneHot(obj, encodingColumns)`

## 参数

**obj** 是一个内存表。

**encodingColumns** 是一个字符串或者字符串向量，指定用于编码的列名。

## 详情

对指定的列进行独热编码（one-hot），返回编码后的表，列的顺序为编码列，非编码列。其中，编码列的列名格式为：原字段名\_值。

## 例子

```
t = table( take(`Tom`Lily`Jim, 10) as name, take(true false, 10) as gender, take(21..23,10) as age);
oneHot(t, `name`gender);
```

输出返回：

| name\_Tom | name\_Lily | name\_Jim | gender\_1 | gender\_0 | age |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 | 21 |
| 0 | 1 | 0 | 0 | 1 | 22 |
| 0 | 0 | 1 | 1 | 0 | 23 |
| 1 | 0 | 0 | 0 | 1 | 21 |
| 0 | 1 | 0 | 1 | 0 | 22 |
| 0 | 0 | 1 | 0 | 1 | 23 |
| 1 | 0 | 0 | 1 | 0 | 21 |
| 0 | 1 | 0 | 0 | 1 | 22 |
| 0 | 0 | 1 | 1 | 0 | 23 |
| 1 | 0 | 0 | 0 | 1 | 21 |

