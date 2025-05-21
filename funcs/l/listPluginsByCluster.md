# listPluginsByCluster

## 语法

`listPluginsByCluster(clusterName)`

## 参数

**clusterName** 字符串标量，表示要查询的集群名称。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

## 详情

获取集群中每个节点上插件的安装情况。

**返回值**：一个表，包含以下字段：

* plugin：插件名称。
* version：插件版本。
* user：安装该插件的用户名称。
* time：插件安装时间，单位为毫秒。
* node：插件安装所在的节点名称。

## 例子

```
// MoMSender 集群节点:
installPlugin("mysql")
loadPlugin("mysql")

// MoM 集群:
listPluginsByCluster("MoMSender")

```

| plugin | version | user | time | node |
| --- | --- | --- | --- | --- |
| mysql | 3.00.3 | admin | 2025.05.24T17:10:42.300 | dnode1 |
| zip | 3.00.3 | admin | 2025.05.24T17:10:42.285 | dnode1 |
| mysql | 3.00.1.3 | admin | 2025.05.24T17:10:49.135 | controller8899 |
| zip | 3.00.3 | admin | 2025.05.24T17:10:49.120 | controller8899 |

