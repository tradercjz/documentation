# restoreSettings

## 语法

`restoreSettings(fileName, [overwrite=false])`

## 参数

**fileName** STRING 类型标量，指定备份文件的路径，可以为绝对路径或相对于 <HomeDir> 的相对路径。

**overwrite** BOOL 类型标量，表示是否将当前数据库系统的用户、用户权限和函数视图更新为与备份文件完全一致：

* false：默认值，表示在恢复过程中仅添加备份文件中存在但当前系统中不存在的用户及其权限、函数视图。对于当前系统已存在的用户和函数视图，不会做任何修改。
* true：表示将当前系统的用户、用户权限和函数视图设置为与备份文件完全一致，即删除当前系统中不存在于备份文件中的用户和函数视图，并添加备份文件中保存的用户及其权限、函数视图。

## 详情

此函数只能由管理员在控制节点执行，将备份文件中保存的用户、用户权限和函数视图恢复到当前集群。

备份文件由函数 [backupSettings](../b/backupsettings.html)
生成，与之搭配可以在数据库迁移时实现用户、用户权限及函数视图的迁移。

函数返回一个向量，依次列出已成功恢复的用户名和函数视图名称。

## 例子

下例以用户及权限为例，函数视图规则与之类似。

当前集群有用户 A 和 B，备份文件中保存了用户 A，C 。

```
// 集群中A、B及其权限不变，增加用户C及其权限
restoreSettings(fileName="/home/ddb/backup/permission.back", overwrite=false)
// 集群中A的权限更新为与备份文件一致，删除用户B，增加用户C及其权限
restoreSettings(fileName="/home/ddb/backup/permission.back", overwrite=true)
```

相关函数： [backupSettings](../b/backupsettings.html)

