# dropStreamTable

## 语法

`dropStreamTable(tableName,[force=false])`

## 详情

删除流数据表。如果流数据表启用了持久化，该函数也会将磁盘上持久化的数据删除。

如果流数据表已经持久化到磁盘但是尚未加载到内存，管理员用户可以通过设置参数 *force* 为 true，直接删除磁盘上的持久化数据。

如果要删除高可用流数据表，只需在 Raft
组中的任意一个数据节点/计算节点上执行该函数即可，其他数据节点/计算节点上名称相同的高可用流数据表也会被删除。

## 参数

**tableName** 是一个字符串，表示流数据表的名称。

**force** 是一个布尔标量，表示是否在内存没有该流数据表时强制删除同名持久化文件。默认值为 false。

## 例子

删除普通流数据表：

```
colNames = `timestamp`sym`qty`price
colTypes = [TIMESTAMP,SYMBOL,INT,DOUBLE]
t=streamTable(1:0,colNames,colTypes)
enableTableShareAndPersistence(t,`trades);

dropStreamTable(`trades);
```

删除未加载到内存的持久化流数据表：

```
colNames = `timestamp`sym`qty`price
colTypes = [TIMESTAMP,SYMBOL,INT,DOUBLE]
t=streamTable(1:0,colNames,colTypes)
enableTableShareAndPersistence(t,`trades);

//删除内存中的流数据表
undef(`trades,SHARED)

//删除持久化流表失败
dropStreamTable(`trades)
//dropStreamTable("trades") => Can't find stream table trades

// admin 设置force为true,成功删除
dropStreamTable(tableName=`trades,force=true)
```

删除高可用流数据表：

```
colNames = `timestamp`sym`qty`price
colTypes = [TIMESTAMP,SYMBOL,INT,DOUBLE]
t=table(1:0,colNames,colTypes)
haStreamTable(11,t,`trades,100000);

dropStreamTable(`trades);
```

