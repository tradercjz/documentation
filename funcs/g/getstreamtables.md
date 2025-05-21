# getStreamTables

## 语法

`getStreamTables([option=0])`

## 详情

获取流数据表的信息，返回一个表，包含如下列：

* name：表的名称。
* shared：是否为共享表。
* persisted：是否为持久化表。
* cachePurgeEnabled：是否为定时清理的非持久化流表。
* loaded：是否已加载到内存。
* columns：表所包含的列数。
* rowsInMemory：内存中的行数。
* totalRows：写入流表的总行数。
* memoryUsed：表所占用的内存大小，单位为字节。

注： 若持久化表没被加载到内存时，则只返回 name, persisted 和 loaded 字段，其它字段返回
NULL。

## 参数

`option` 整型标量，表示需要获取的流表的类型。可取以下值：

* 0：获取所有流表
* 1：获取持久化流表
* 2：获取非持久化流表

## 例子

```
id=`XOM`GS`AAPL;
x=102.1 33.4 73.6;

rt=streamTable(id, x);
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades1;
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades2;

getStreamTables()
```

| name | shared | persisted | cachePurgeEnabled | loaded | columns | rowsInMemory | totalRows | memoryUsed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rt | false | false | false | true | 2 | 3 | 3 | 152 |
| trades1 | true | false | false | true | 4 | 0 | 0 | 240 |
| trades2 | true | false | false | true | 4 | 0 | 0 | 240 |

