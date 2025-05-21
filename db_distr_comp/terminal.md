# DolphinDB 终端

DolphinDB 终端（DolphinDB Terminal）是一个命令行交互式工具，用于连接到远程的 DolphinDB
服务器执行命令。使用终端的优点是可以快速连接到远端数据库上执行一些交互命令和脚本。缺点是没有图形化界面，不适用于开发和执行大量复杂代码。

DolphinDB 终端和 DolphinDB 服务器用的是同一个程序，1.10.4及以上版本方可支持。当用户启动 DolphinDB
的时候，如果指定参数 `remoteHost` 和 `remotePort`，当前进程将被启动为 DolphinDB
终端。如果服务器不允许guest用户登录，启动时可参数 `uid` 和 `pwd`
指定用户名和密码，也可以在启动后的终端中通过 login 命令登录。DolphinDB 的工作非常简单，接受用户的输入并发送到远程服务器执行，最后把执行结果在终端显示。因此
DolphinDB 终端不需要 license，也不需要系统初始化脚本 dolphindb.dos 以及其它配置文件。DolphinDB
的终端可以是跨操作系统的，例如Windows上的终端可以访问Linux的DolphinDB的服务器。

## 基本用法

下面的命令是在 Linux 上启动 DolphinDB 终端的示例。由于默认 shell 不支持命令上下回滚，所以需要借助
rlwrap 命令来实现。

```
rlwrap -r ./dolphindb -remoteHost 127.0.0.1 -remotePort 8848 -uid admin -pwd 123456
```

下面的命令是在 Windows 上启动 DolphinDB 终端的示例。

```
dolphindb.exe -remoteHost 127.0.0.1 -remotePort 8848 -uid admin -pwd 123456
```

成功登入后，系统会显示 DolphinDB Termninal，如下：

```
DolphinDB Terminal 1.10.4 (Build:2020.04.03). Copyright (c) 2011~2019 DolphinDB, Inc.
```

如果启动终端时不指定登录信息，可以在连接后使用 login 命令。

```
>DolphinDB Terminal 1.10.4 (Build:2020.04.03). Copyright (c) 2011~2019 DolphinDB, Inc.
>login("admin","123456");
```

DolphinDB 终端支持单行或多行脚本。只要在代码末尾加上分号 `;` 或者
`go` 语句，系统就会将代码发送到远端执行。通过分号 `;` 单句提交示例如下：

```
1+2;
```

多句提交示例如下：

```
def myFunc(x,y){
    return x+y
}
myFunc(1,2);
```

由于分号 `;`
会触发解析它们之前的代码，如果将其放在自定义函数中间，会造成函数定义无法完整传送到远端，从而造成解析错误，例如:

```
def myFunc(x,y){
    return x+y;
}
myFunc(1,2);

//抛出语法接异常
Syntax Error: [line #2] } expected to end function definition
```

退出终端使用 quit 指令。

```
quit + Enter
```

为方便在任何工作目录下启动终端，可以将 DolphinDB 可执行文件目录（即包含 dolphindb 或者
dolphindb.exe 的目录），添加到系统的搜索路径中。Linux 上可以 export 到 `PATH`

```
export PATH=/your/dolphindb/excutable/path:$PATH
```

在 Windows 上可以将可执行文件路径添加到系统环境变量 `Path`
中。格式为分号加全路径（注意分号必须是英文分号）。路径设置完成后，可以通过打开 dos 或者 PowerShell 窗口，在任意目录下，通过 dolphindb
命令启动终端。

## 本地执行脚本

通过终端交互式或批量执行脚本覆盖了大部分的应用场景。但是某些场景下，需要同时能够在本地和远端执行脚本。譬如，本地读取一个 csv
文件，然后追加到运行在远端 DolphinDB 数据库中。这种模式我们称之为 `命令行本地脚本执行`。下面是在 Linux
上启动命令行本地脚本执行的示范：

```
./dolphindb  -run /home/usr1/test.dos

```

Windows 上启动命令行本地脚本执行非常类似：

```
dolphindb.exe -run c:/users/usr1/test.dos
```

启动命令行本地脚本执行，只要通过启动参数 run 指定一个本地的脚本文件，同时不指定参数 remoteHost
即可。本质上是启动了一个 DolphinDB 的工作站（workstation） 来执行脚本，完成后退出。因此，命令行本地执行脚本文件的配置跟工作站的配置一样，需要
dolphindb.lic 和 dolphindb.dos。在 Windows 下，还需要 tzdb 目录。

那么在本地脚本执行过程中，如何连接到远端数据库进行操作呢？我们需要通过 xdb 函数创建一个到远程数据库的连接，然后使用
remoteRun 函数执行一个脚本或进行rpc调用。DolphinDB 对 rpc
调用进行了扩展，不仅可以调用远端服务器上定义的函数，也可以将本地的函数序列化到远端服务器执行。如果需要执行的脚本比较复杂，一般我们建议定义成一个本地的函数，然后通过
rpc 调用来完成。

下面的脚本文件 `test.dos`，演示了如何将本地的一个 csv
文件，写入到远程的一个分布式数据库表中。

```
def appendData(dbPath, partitionTable, t1){
    pt = loadTable(dbPath, partitionTable)
    return tableInsert(pt, t1)
}

conn=xdb("127.0.0.1",8848,"admin","123456")
remoteRun(conn, appendData, "dfs://db1", "pt", loadText("c:/users/usr1/data.csv"))
```

我们首先定义一个函数
`appendData`，将一个内存表写入到指定的数据库表中。然后创建一个远程连接 conn。最后通过
`loadText` 函数加载本地的 csv 文件，rpc 调用 `appendData`
函数。

## 远程执行脚本

DolphinDB 终端可以让用户方便地连接到远端 DolphinDB
服务器，并以交互的方式执行命令。但是如果所有需要执行的脚本已经写在一个脚本文件中，那么我们有更简单的办法在远端服务器上批处理执行这些脚本。只要在启动 DolphinDB
终端的命令中额外指定一个参数 `run`，即可将 `run`
参数指定的本地脚本文件发送到远端服务器上执行。执行完成后终端马上退出。我们称这种模式为命令行远程脚本执行。使用示例如下。

注： `/home/usr1/test.dos`
是本地而非远程服务器上的脚本文件。

```
./dolphindb -remoteHost 127.0.0.1 -remotePort 8848 -uid admin -pwd 123456 -run /home/usr1/test.dos
```

命令行远程脚本执行是 DolphinDB
终端的一个特殊应用。相对于终端模式，优点是无需在终端中输入代码，可以执行更复杂的代码，以及用于重复执行特定任务。例如，定期连接到远端服务器数据库执行脚本中的代码，执行完即退出。缺点是，没有交互模式。

注： 通过 `-run` 使用远端服务器执行本地脚本文件时，如遇异常，返回非 0
值。

