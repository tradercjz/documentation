# setAtomicLevel

## 语法

`setAtomicLevel(dbHandle, atomic)`

## 参数

**dbHandle** 是 [database](../d/database.html) 函数返回的分布式数据库句柄。

**atomic** 表示写入事务的原子性层级，决定了是否允许并发写入同一分区。可选值为 'TRANS' 和 'CHUNK'，默认值为 'TRANS'。

* 设置为'TRANS'，写入事务的原子性层级为事务，即一个事务写入多个分区时，若某个分区被其他写入事务锁定而出现写入冲突，则该事务的写入全部失败。因此，该设置下，不允许并发写入同一个分区。
* 设置为'CHUNK'，写入事务的原子性层级为分区。若一个事务写入多个分区时，某分区被其它写入事务锁定而出现冲突，系统会完成其他分区的写入，同时对之前发生冲突的分区不断尝试写入，尝试数分钟后仍冲突才放弃。此设置下，允许并发写入同一个分区，但由于不能完全保证事务的原子性，可能出现部分分区写入成功而部分分区写入失败的情况。同时由于采用了重试机制，写入速度可能较慢。

## 详情

修改分布式数据库的并发写入权限。

## 例子

```
dbPath="dfs://test"
mydb=database(dbPath, VALUE, ['AMZN','NFLX', 'NVDA'])
mydb.schema()

// output
databaseDir->dfs://test
partitionSchema->[NVDA,AMZN,NFLX]
partitionSites->
partitionTypeName->VALUE
partitionType->1
atomic->TRANS
```

```
setAtomicLevel(mydb, `CHUNK)
mydb.schema()

// output
databaseDir->dfs://test
partitionSchema->[NVDA,AMZN,NFLX]
partitionSites->
partitionTypeName->VALUE
partitionType->1
atomic->CHUNK
```

