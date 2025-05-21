# addVolumes

## 语法

`addVolumes(volumes)`

## 参数

**volumes** 是字符串标量或向量，表示磁盘卷的路径。

## 详情

动态增加磁盘卷，使新增磁盘卷马上可以使用而无需重启集群。

注： 此命令并不会改变集群配置文件。使用该命令后请更改配置文件，否则集群重启后将不能写入新增的磁盘卷。

## 例子

```
addVolumes("/home/dolphindb/data")
```

