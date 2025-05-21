# getUserListOfAllClusters

## 语法

`getUserListOfAllClusters()`

## 参数

无

## 详情

查询多集群管理系统中所有集群的用户信息。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

**返回值**：一个字典（dictionary），其中：

* key：集群名称。
* value：该集群下的用户名称列表。

## 例子

```
getUserListOfAllClusters()

/* Output:
masterOfMaster->["user1","user2","admin"]
MoMSender->["admin","user2"]
*/
```

