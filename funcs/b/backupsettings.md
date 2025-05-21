# backupSettings

## 语法

`backupSettings(fileName, [userPermission=true],
[functionView=true])`

## 参数

**fileName** STRING 类型标量，指定备份文件的存储路径，可以为绝对路径或相对于 <HomeDir> 的相对路径。

**userPermission** BOOL 类型标量，表示是否备份用户权限。默认值为 true，表示备份用户权限。

**functionView** BOOL 类型标量，表示是否备份函数视图。默认值为 true，表示备份函数视图。

## 详情

此函数只能由管理员在控制节点执行，备份当前数据库系统中的所有用户、用户权限信息和函数视图，并将备份文件保存到指定路径。

函数返回一个向量，依次列出已成功备份的用户名和函数视图名称。

与函数 [restoreSettings](../r/restoresettings.html)
搭配使用，可以在数据库迁移时实现用户、用户权限及函数视图的迁移。

## 例子

```
// 备份用户、权限信息、函数视图
backupSettings(fileName="/home/ddb/backup/permission.back", userPermission=true, functionView=true)
// 备份用户、权限信息，不备份函数视图
backupSettings(fileName="/home/ddb/backup/permission.back", userPermission=true, functionView=false)
// 备份用户、函数视图，不备份权限信息
backupSettings(fileName="/home/ddb/backup/permission.back", userPermission=false, functionView=true)
// 备份用户，不备份权限信息和函数视图
backupSettings(fileName="/home/ddb/backup/permission.back", userPermission=false, functionView=false)
```

相关函数：[restoreSettings](../r/restoresettings.html)

