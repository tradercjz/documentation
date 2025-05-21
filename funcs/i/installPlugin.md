# installPlugin

## 语法

`installPlugin(pluginName, [pluginVersion],
[pluginServerAddr])`

## 详情

下载并解压指定名称的插件的二进制文件（Windows 版本 server 使用 .dll，Linux 版本 server 使用
.so）和插件描述文件（.txt）到 DolphinDB
的插件目录（/server/plugins/）下。返回插件描述文件的完整路径。后续可通过该路径加载插件。

可通过 [listRemotePlugins](../l/listRemotePlugins.md) 函数查看所支持的插件名称及版本信息。

## 参数

**pluginName** STRING 类型，用于指定插件名称。

**pluginVersion** 可选，STRING 类型，用于指定插件版本。如果不指定该参数，则使用插件的最新版本。

**pluginServerAddr** 可选，STRING 类型，用于指定插件仓库的 HTTP 地址。如果不配置该参数，使用默认的 HTTP
地址："http://plugins.dolphindb.cn/plugins"。如果 DolphinDB 服务位于国外，建议填写
"http://plugins.dolphindb.com/plugins" 以提高查询速度。

## 例子

在 Linux 中下载指定的插件：

```
installPlugin("mysql")
```

返回：
/home/DolphinDB\_Linux64\_V2.00.10/server/plugins/mysql/PluginMySQL.txt

通过 `loadPlugin` 加载插件：

```
loadPlugin("mysql")
```

**相关信息**

* [listRemotePlugins](../l/listRemotePlugins.html "listRemotePlugins")
* [loadPlugin](../l/loadPlugin.html "loadPlugin")

