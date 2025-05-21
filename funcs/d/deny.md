# deny

## 语法

`deny(userId|groupId, accessType, [objs])`

## 参数

**userId** | **groupId** 是表示用户名或组名的字符串。

**accessType** 权限类型/内存限制。

**objs** 标量或向量，表示权限类型的应用对象/约束规则。也可以指定为 \*，表示全局。当 *accessType* 指定为 COMPUTE\_GROUP\_EXEC 时，*objs*
必须为对应的计算组名。

注：

* 管理共享内存表、流数据表或流计算引擎的权限时，*objs* 必须为 "tableName@nodeAlias"
  或"nodeAlias:tableName"。
* 管理 IMOLTP 引擎库表权限时，*objs* 必须为 "oltp://database/table@nodeAlias" 或
  "oltp://database@nodeAlias"。

*accessType* 和 *objs* 的取值请参照 [用户权限管理](../g/../../tutorials/ACL_and_Security.md) 权限类型表。

## 详情

拒绝某个用户或某个组的权限。管理员可以通过该命令拒绝用户所有权限（*accessType*），但普通用户在拥有相关的
OWNER 权限后，只能通过该命令拒绝以下权限：TABLE\_READ, TABLE\_WRITE, TABLE\_INSERT, TABLE\_UPDATE,
TABLE\_DELETE, DB\_READ, DB\_WRITE, DB\_INSERT, DB\_UPDATE, DB\_DELETE, DBOBJ\_DELETE,
DBOBJ\_CREATE 和 VIEW\_EXEC。

注： 该函数可在控制节点、数据节点和计算节点运行。

## 例子

组 "research" 中的所有成员都不能向表 dfs://db1/t1 中写入数据：

```
deny(`research, TABLE_WRITE, "dfs://db1/t1")
```

组 "research" 中的所有成员都不能在数据库 dfs://db1 和 dfs://db2 中创建表：

```
deny("research", DBOBJ_CREATE, ["dfs://db1","dfs://db2"])
```

用户 "AlexSmith" 不能删除数据库：

```
deny("AlexSmith", DB_MANAGE)
```

用户 "AlexSmith" 不能执行脚本：

```
deny("AlexSmith", SCRIPT_EXEC)
```

用户 "AlexSmith" 不能测试脚本：

```
deny("AlexSmith", TEST_EXEC)
```

