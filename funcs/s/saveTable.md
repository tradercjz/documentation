# saveTable

## 语法

`saveTable(dbHandle, table, [tableName], [append=false],
[compression=false])`

## 参数

**dbHandle** 是一个未分区的数据库的句柄。

**table** 是将要被保存的内存中的表。

**tableName** 是要保存的表的名称。如果没有指定，将会与内存中的表的名称相同。它需要用反引号(`)或双引号引用。

**appending** 设置了追加模式。当它为 true 时，新的表会被追加到旧的表之后。默认的设置是
false。

**compression** 设置压缩模式。当它为 true 时，表会以压缩模式保存到磁盘中。默认的设置是
false。

## 详情

将一个表保存在未分区的本地磁盘表中。该命令必须要用户登录后才能执行。

如果要把表保存至分区数据库中，需要先使用 `createPartitionedTable`
函数创建分区表，再使用 `append!` 函数或 `tableInsert`
函数把数据保存至分区表中。

注：

磁盘表仅应用于备份数据和本地计算的场景，其相较于分布式表，在使用上具有一定局限，例如不能进行权限控制等。

## 例子

```
db=database("C:/DolphinDB/Data/db1")
t=table(take(1..10,10000000) as id, rand(10,10000000) as x, rand(10.0,10000000) as y);
```

把表 t 保存为本地磁盘表：

```
saveTable(db, t);
```

指定 *tableName*：

```
saveTable(db, t, `t1);
```

指定 *tableName*，并把 *appending* 设置为 true：

```
saveTable(db, t, `t2, 1);
```

指定 *tableName*，并把 *compression* 设置为 true：

```
saveTable(db, t, `t3, 0, 1);
```

