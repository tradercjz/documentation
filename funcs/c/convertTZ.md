# convertTZ

## 语法

`convertTZ(obj, srcTZ, destTZ)`

## 参数

**obj** 可以是 DATETIME, TIMESTAMP, NANOTIMESTAMP 类型的时间标量或向量。

**srcTZ** 和 **destTZ** 都是字符串，表示时区。

## 详情

把 *srcTZ* 时区的时间 *obj* 转换成 *destTZ* 时区的时间。

## 例子

```
convertTZ(2016.04.25T08:25:45,"US/Eastern","Asia/Shanghai");
// output
2016.04.25T20:25:45
```

