# updateLicense

## 语法

`updateLicense()`

## 参数

无

## 详情

用于在线更新 license。先手动替换 license 文件，然后执行该函数在线更新 license，而无需重启节点。用户可通过 [getLicenseExpiration](../g/getLicenseExpiration.html) 获得当前 license 的过期时间，以判断 license
是否生效。

该函数只在执行该函数的节点生效。因此在集群环境下，需要在所有节点上运行该函数。

注：

* 待升级 license 需满足以下条件才能成功升级（可通过
  `license` 函数查看）：

  + 授权的客户名称（cilentName）和授权模式（authorization）必须与原来的 license
    相同。
  + 授权的节点个数（maxNodes），内存大小（maxMemoryPerNode），CPU
    核数（maxCoresPerNode）不小于原 license 的授权。
* 若原 license 授权模式（authorization）为
  site，则无法进行在线升级。
* 从 2.00.9 版本开始，支持将 DolphinDB 进程绑定到具体的 CPU 内核上。若待升级
  license 中修改了绑定核信息，则升级 license 后须重启 DolphinDB 以使 CPU 内核绑定的设置生效。

## 例子

```
updateLicense()
// output
authorization->commercial
licenseType->0
maxMemoryPerNode->32
maxCoresPerNode->8
clientName->test license
bindCPU->true
expiration->2022.03.01
maxNodes->8
version->
modules->-1
```

