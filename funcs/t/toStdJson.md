# toStdJson

## 语法

`toStdJson(obj)`

## 参数

**obj** 的数据形式不可为 matrix 或 pair；数据类型不可为
UUID, IPADDR, INT128, COMPRESSED 以及系统类型。

## 详情

将 DolphinDB 对象转换为标准 JSON 类型。

* 转化 bool 值时，返回 true 或 false 值。
* 转换空值时，将除了 STRING 类型空值以外的其他所有类型空值都转换为null。

## 例子

```
x=1 2 3
toStdJson(x);
// output:
[1, 2, 3]

t=table(1 2 3 as id, 10 20 30 as val)
toStdJson(t);
// output:
[{"id": 1,"val": 10},{"id": 2,"val": 20},{"id": 3,"val": 30}]

b = set(2012.06.13T13:30:10 2017.07.10T14:10:12)
toStdJson(b);
// output:
["2017.07.10 14:10:12","2012.06.13 13:30:10"]

b = dict(INT,DATETIME)
b[0] = 2012.06.13 13:30:10
b[1] = 2017.07.10 14:10:12
toStdJson(b);
// output:
{"1": "2017.07.10 14:10:12","0": "2012.06.13 13:30:10"}

t1=table(`x`y`z as b, 2012.06.13 13:30:10 2012.06.13 13:30:10 2012.06.13 13:30:10 as c,10.8 7.6 3.5 as F)
toStdJson(t1);
// output:
[{"b": "x","c": "2012.06.13 13:30:10","F": 10.8},{"b": "y","c": "2012.06.13 13:30:10","F": 7.6},{"b": "z","c": "2012.06.13 13:30:10","F": 3.5}]
```

相关函数：[toJson](toJson.html)

