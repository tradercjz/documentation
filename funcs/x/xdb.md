# xdb

## 语法

`xdb(siteAlias, [userId], [password],
[enableSSL])`

或

`xdb(host, port, [userId], [password],
[enableSSL])`

## 参数

**siteAlias** 是远程节点的别名。它需要在配置文件中定义。

**host** 是远程节点的主机名（IP 地址或站点）。

**port** 是远程节点的端口号。

**userId** 和 **password** 可选参数。基于用户的配置文件。如果管理员启用用户访问控制，需要输入用户名和密码。

**enableSSL** 可选参数。布尔值，表示是否使用 SSL 协议进行加密通信。默认值为 false。

## 详情

连接到节点的远程站点。如果连接成功，则返回远程连接的句柄。

## 例子

```
h2=xdb("local8081");
h2;
// output
"Conn[localhost:8081:1166953221]"

h21=xdb("localhost",8081);
h21;
// output
"Conn[localhost:8081:1441295757]"

h4=xdb("local8083","userAdm","passAdm");
h4;
// output
"Conn[localhost:8083:1166953221]"

h41=xdb("localhost",8083, "user001","pass001");
h41;
// output
"Conn[localhost:8083:597793698]"
```

