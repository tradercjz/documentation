# setMemLimitOfAllTempResults

## 语法

`setMemLimitOfAllTempResults()`

## 参数

**memLimit** 一个数值型标量，必须大于0且不能大于 *maxMemSize* 的设置值。

## 详情

某些分布式查询操作（例如表连接、GROUP BY、CONTEXT BY、PIVOT
BY），可能会产生临时表用于存储查询中产生的结果。该函数用于在线设置这些临时表允许占用的内存上限，单位为 GB。可通过
`getMemLimitOfAllTempResults` 查看设置是否生效。

注：

* 该函数只能由管理员在数据节点/计算节点上执行。
* 此函数修改的配置值在系统重启后将失效。若需要配置值永久生效，请更改配置文件中的
  *memLimitOfAllTempResults*。

## 例子

```
setMemLimitOfAllTempResults(3.0)
```

相关函数：[getMemLimitOfAllTempResults](../g/getmemlimitofalltempresults.html)

