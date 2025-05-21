# getLoadedPlugins

## 语法

`getLoadedPlugins()`

## 详情

获取当前节点已加载的插件列表。

## 参数

无

## 返回值

一张表，包含以下字段：

* plugin：STRING，插件名称。
* version：STRING，插件的版本（*PluginXXX.txt* 文件的版本）
* user：STRING，加载该插件的用户名称。
* time：TIMESTAMP，加载该插件的时间。

## 例子

```
login("admin","123456")
loadPlugin("zip")
login("user1","123456")
loadPlugin("httpclient")

getLoadedPlugins()
```

返回结果：

| plugin | version | user | time |
| --- | --- | --- | --- |
| zip | 3.00.1 | admin | 2024.09.01T10:00:01.000 |
| httpClient | 3.00.1 | user1 | 2024.09.01T10:00:02.000 |

