# getAclAuditLog

## 语法

`getAclAuditLog([userId],[startTime],[endTime],[opType])`

## 详情

查询用户 *userId* 在*startTime* 到 *endTime* 这段时间内完成的，类型为 *opType* 的
ACL 操作记录。

**返回值**：一张表，包含以下字段：

* userId：表示执行操作的用户名称。
* time：表示操作发生时间。
* opType：表示操作类型。
* opDetail：操作细节说明。
* remoteIp：提交该操作的客户端 IP。
* remotePort：提交该操作的客户端端口。

*opType* 的所有取值及其对应的 opDetail 示例如下：

| opType | opDetail | Description |
| --- | --- | --- |
| login | login userId=xxx encrypted=true/false | 用户登录 |
| logout | logout userId=xxx sessionOnly=true/false | 用户登出 |
| createUser | userId=xxx groupId=xxx isAdmin=true/false | 创建用户 |
| createGroup | groupId=xxx userIds=[xxx,xxx,…] | 创建用户组 |
| resetPwd | userId=xxx | 重置用户密码 |
| changePwd |  | 修改用户密码 |
| deleteUser | userId=xxx | 删除用户 |
| deleteGroup | groupId=xxx | 删除用户组 |
| addGroupMember | userIds=[xxx,xxx,…] groupIds=[xxx,xxx,…] | 把用户添加到群组 |
| deleteGroupMember | userIds=[xxx,xxx,…] groupIds=[xxx,xxx,…] | 删除用户组的成员 |
| grant | userOrGroupId=xxx accessType=xxx objs=[xxx,xxx,…] | 授予权限 |
| deny | userOrGroupId=xxx accessType=xxx objs=[xxx,xxx,…] | 拒绝权限 |
| revokeByDFSOperation | oldObj=xxx newObjs=[xxx,xxx,…] | 进行 dropDatabase, dropTable 或 dropColumn! 删除操作时，会自动清除所有用户中与被删除内容相关的权限。 |
| replaceByDFSOperation | oldObj=xxx newObjs=[xxx,xxx,…] | 进行 renameTable 和 replaceColumn! 等修改操作时，会同步更新与被修改内容相关的权限信息 |
| revoke | userOrGroupId=xxx accessType=xxx objs=[xxx,xxx,…] | 撤回权限 |
| createCatalog | catalog=xxx | 创建 catalog |
| dropCatalog | catalog=xxx | 删除 catalog |
| renameCatalog | catalog=xxx new catalog=xxx | 重命名 catalog |
| renameSchema | catalog=xxx schema=xxx new schema=xxx | 重命名 schema |
| createSchema | catalog=xxx dbUrl=xxx schema=xxx | 创建 schema |
| dropSchema | catalog=xxx schema=xxx | 删除 schema |
| tryDropSchemaByDatabase | dbUrl=xxx | 删除数据库时，从 catalog 里删掉 db 对应的 schema |
| setMaxJobPriority | maxJobPriority=xxx | 指定提交作业的最高优先级 |
| setMaxJobParallelism | maxJobParallelism=xxx | 指定提交的作业最多可以同时并行执行的子任务数量 |
| newConnection |  | 收到新连接 |
| closeConnection |  | 关闭连接 |
| saveClusterNodes |  | 修改 nodes.cfg |
| saveClusterNodesConfigs |  | 修改 cluster.cfg |
| saveControllerConfigs |  | 修改 controller.cfg |
| loadClusterNodesConfigs |  | 读取 nodes.cfg |
| loadControllerConfigs |  | 读取 controller.cfg |

## 参数

**userId** 可选参数，字符串标量或向量，表示要查询的用户。默认为 NULL，表示查询所有用户的 ACL 操作日志。

**startTime** 可选参数，整型标量或者时间标量，表示查询的起始时间点。时间标量支持 DATE, MONTH, DATETIME, TIMESTAMP,
DATEHOUR, NANOTIMESTAMP 类型。默认值为 1970.01.01，表示 1970.01.01零点。

**endTime** 可选参数，整型标量或者时间标量，表示查询的结束时间点。时间标量支持DATE, MONTH, DATETIME, TIMESTAMP,
DATEHOUR, NANOTIMESTAMP 类型。默认值为空，表示结束时间为当前时间。*endTime* 必须大于
*startTime*。

**opType** 可选参数，字符串标量或向量，表示查询的操作类型。默认为 NULL，表示查询所有 ACL 操作类型。关于 *opType*
的详细描述参见详情。

## 例子

首先配置文件设置 *enableAuditLog*=true。然后通过 `getAclAuditLog` 查询所有 ACL
操作。

```
login("admin","123456")
createUser("user1","abcdec")
grant("user1",TABLE_READ,"*")
logout()
login("admin","123456")
getAclAuditLog()
```

返回：

| userId | time | opType | opDetail | remoteIp | remotePort |
| --- | --- | --- | --- | --- | --- |
| guest | 2025.01.02 14:26:52.738224592 | newConnection |  | 192.168.0.130 | 55,428 |
| guest | 2025.01.02 14:26:53.049518446 | login | login userId=admin encrypted=false | 192.168.0.130 | 55,428 |
| admin | 2025.01.02 14:26:53.059963095 | createUser | userId=user1 groupIds=[] isAdmin=false | 192.168.0.130 | 55,428 |
| admin | 2025.01.02 14:26:53.060387348 | grant | userOrGroupId=user1 accessType=TABLE\_READ objs=[] | 192.168.0.130 | 55,428 |
| guest | 2025.01.02 14:26:53.060426785 | logout | logout userId=admin sessionOnly=true | 192.168.0.130 | 55,428 |
| guest | 2025.01.02 14:26:53.060576365 | login | login userId=admin encrypted=false | 192.168.0.130 | 55,428 |
| guest | 2025.01.08 09:46:49.710254224 | newConnection |  | 192.168.0.130 | 41,746 |
| guest | 2025.01.08 09:46:52.124830142 | login | login userId=admin encrypted=false | 192.168.0.130 | 41,746 |
| admin | 2025.01.08 09:46:52.127153771 | createUser | userId=user1 groupIds=[] isAdmin=false | 192.168.0.130 | 41,746 |
| admin | 2025.01.08 09:46:52.127752666 | grant | userOrGroupId=user1 accessType=TABLE\_READ objs=[] | 192.168.0.130 | 41,746 |

