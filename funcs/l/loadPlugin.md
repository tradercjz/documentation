# loadPlugin

## 语法

`loadPlugin(filepath)`

## 参数

**filepath**
是文本文件的绝对路径。例如：/home/DolphinDB\_Linux64\_V2.00.10/server/plugins/mysql/PluginMySQL.txt。

自2.00.11版本起，可以将其指定为插件名（大小写敏感）。系统会根据插件名称和配置项 *pluginDir* 拼接出插件的加载路径。

## 详情

加载 DolphinDB 插件。该函数必须要用户登录后才能执行。

注：

* 在产品体验阶段，如果未自行创建用户或管理员账号，可以使用 DolphinDB
  提供的初始管理员账号（admin）及密码（123456）。在生产环境中，务必使用具备中等以上安全强度的用户或管理员密码。
* 加载前请确保有对应插件的使用权限。收费插件需要另行购买。

来自 DolphinDB 插件市场的插件在使用 [installPlugin](../i/installPlugin.md)
命令安装后，会在<server路径>/plugins/<插件名称>路径下生成一个命名方式为
"Plugin" + "插件名称"的 txt 格式的插件描述文件和相关的二进制文件（Windows 版本下为 .dll，Linux 版本下为 .so）。例如，安装在
Windows 版本 DolphinDB server 2.00.10 的 odbc 插件描述文件存储于：

```
../DolphinDB_Win64_V2.00.10/server/plugins/odbc/PluginODBC.txt
```

该文件包含以下内容：

```
odbc,libPluginODBC.dll,2.00.10
odbcQuery,query,system,2,5,0
odbcConnect,connect,system,1,2,0
odbcClose,close,system,1,1,0
odbcExecute,execute,system,2,2,0
odbcAppend,append,system,3,5,0
```

该文件格式如下：

* 第一行：插件名称、lib 文件、版本号，用 “,” 分隔；
* 其他行用于描述该插件提供的函数，依次包含以下信息：lib 文件中的某个函数的名称、对应的 DolphinDB 函数的名称、函数的类型（operator
  表示运算符，system 表示系统函数）、函数所需的最小参数个数、函数所需的最大参数个数、是否为聚合函数（1 表示聚合函数，0
  表示非聚合函数）、是否为序列函数（1表示序列函数，0表示非序列函数）。

## 例子

**加载来自插件市场的插件**

以在 Windows 操作系统上安装 MQTT 插件为例，加载方法有两种：

* 使用插件描述文件的绝对路径加载插件：

  ```
  installPlugin("mqtt")
  loadPlugin("D:/TEST/DolphinDB_Win64_V2.00.10/server/plugins/mqtt/PluginMQTT.txt")
  ```

  注： 在 Windows
  操作系统中使用绝对路径加载插件时，务必确保路径中使用"/"代替"\"。
* 或指定插件名称：

  ```
  installPlugin("mqtt")
  loadPlugin("mqtt")
  ```

**加载自行编译的插件**

以 DolphinDB Linux 版本的 odbc 插件为例，其描述文件 odbc.txt 内容如下：

```
odbc,libPluginODBC.so,2.00.10
odbcQuery,query,system,2,5,0
odbcConnect,connect,system,1,2,0
odbcClose,close,system,1,1,0
odbcExecute,execute,system,2,2,0
odbcAppend,append,system,3,5,0

```

odbc 插件提供了 5 个函数：`query`, `connect`,
`close`, `execute` 和
`append`，需要加载插件后才能使用。下面的例子介绍了如何加载 odbc 插件，并调用 odbc 插件提供的函数。

```
loadPlugin("/home/DolphinDB/server/plugins/odbc/odbc.txt")
//或者通过插件名进行加载
loadPlugin("odbc")
use odbc
ConnStr="Driver=MySQL;Data Source=odbc_test;Server=127.0.0.1;Uid=root;Pwd=123456;Database=odbc_test"
conn=connect(connStr)      // 创建 MySQL 连接

t=query(conn,"select * from test")
close(conn)
```

**相关信息**

* [installPlugin](../i/installPlugin.html "installPlugin")
* [listRemotePlugins](listRemotePlugins.html "listRemotePlugins")

