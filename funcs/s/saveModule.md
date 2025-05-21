# saveModule

## 语法

`saveModule(name, [moduleDir],
[overwrite=false])`

## 参数

**name** 是一个字符串，表示模块的名称。

**moduleDir** 是一个字符串，表示模块 dos 文件所在的目录。

**overwrite** 是一个布尔值，表示是否覆盖已有的模块 dom 文件。

## 详情

将模块序列化成扩展名为 dom 的二进制文件，可以增加代码的保密性和安全性。该函数必须要用户登录后才能执行。

如果没有指定 *moduleDir*，默认是相对目录 modules。系统搜寻相对目录 modules 的顺序如下：先到节点的 home
目录寻找，再到节点的工作目录寻找，最后到 DolphinDB 可执行文件所在目录寻找。请注意，单节点模式下，这三个目录默认为同一目录。

## 例子

假设节点 home 目录下的 modules 目录中包含了 ta.dos 以及 system/log/fileLog.dos 模块文件，将它们序列化为二进制文件。

```
saveModule("ta");

saveModule("system::log::fileLog");
```

相关函数：[loadModule](../l/loadModule.md)

