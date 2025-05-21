# remoteRunCompatible

## 语法

`remoteRunCompatible(conn, script, args)`

### 参数

**conn** 是远程数据库的连接句柄。

**script** 是要执行的脚本或函数名。

**args** 可选的可变长度参数。如果 *script* 是函数名，*args* 是函数的参数。

## 详情

将脚本或函数传输到远程数据库执行。

remoteRunCompatible 与 remoteRun 的区别在于：

* remoteRunCompatible 对本地和远程数据库的版本没有限制。
* remoteRun 在本地数据库为 3.00 版本时，不支持远程数据库的版本低于3.00。

## 例子

第一种用法：*script*
是脚本，则表示在远程节点上执行脚本。

```
conn =
              xdb(host="localhost",port=8848,userId="admin",password=123456);
            remoteRunCompatible(conn, "avg(1..100)");
```

结果为
50.5。

第二种用法：*script* 是函数名

* 如果 script 加了单引号，双引号或者反引号，那么表示在远程节点上调用函数。函数是定义在远程节点上，但是参数由本地节点传过去。

在远程节点增加函数视图 myAvg

`def myAvg(x){ return avg(x)+2 }
addFunctionView(myAvg)`

连接远程节点调用视图

```
conn =  xdb("localhost",8848,`admin,`123456);
            remoteRunCompatible(conn, "myAvg", 1..100);
```

结果为
52.5。

* 如果 script 不加单引号，双引号或者反引号，那么表示调用的函数定义在本地节点上。参数也是由本地节点传过去。

在本地节点定义同名函数 myAvg

`def myAvg(x){ return avg(x)+1
}`

在远程节点执行此函数

```
conn =  xdb("localhost",8848,`admin,`123456);
            remoteRunCompatible(conn, myAvg, 1..100);
```

结果为
51.5。

相关函数：[remoteRun](remoteRun.html)

