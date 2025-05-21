# license

## 语法

`license([fileName], [pubKeyFile], [read=false])`

## 详情

显示 DolphinDB 的许可证信息。

注： 若不指定 *fileName*，则默认读取保存在内存中的 license 信息

返回值说明：

| 参数 | 含义 |
| --- | --- |
| authorization | 授权的类型：trial（试用版）/test（测试版）/commercial（商业版）。 |
| licenseType | 许可证验证类型，有以下可选值：1：机器指纹绑定；2：在线验证；3：license server；0：其他方式 |
| maxMemoryPerNode | 每个节点的内存上限，单位为 GB。 |
| bindCores | 进程绑定的 CPU 内核的编号（从0开始）。注意，仅当 bindCPU 为 true 时有效。 |
| maxCoresPerNode | 每个节点允许最大 CPU 核数。 |
| clientName | 客户名称。 |
| port | 为节点绑定的端口号。仅 License Server 和连接它的节点会返回此字段。 |
| bindCPU | 进程是否绑定 CPU。 |
| expiration | 许可证到期时间。 |
| maxNodes | 集群允许的最大节点数。 |
| version | server 的版本号。用户只能使用不高于 version 版本的 server。若为空，则对版本没有限制。 |
| modules | 可用模块的编码。若为 13 则表示支持所有模块；若为 -1 则表示不支持任何模块。 |
| moduleNames | 与 *modules* 有关，返回具体的模块名。目前支持返回：orderbook, internalFunction, cep, gpu。社区版返回为空。 |
| productKey | 当前产品类型。目前支持返回：DOLPHIN, IOTBASIC, IOTPRO, SHARK, SWORDFISH。 |

## 参数

**fileName** 可选参数。需要指定的 license 文件的路径。

**pubKeyFile** 可选参数。需要指定的公钥文件的路径。

**read** 可选参数。布尔值，表示是否关闭对 license 文件的校检功能。默认值为 false，表示进行校检。

## 例子

```
license();
```

返回：

```
clientName->internal
bindCPU->true
maxNodes->128
moduleNames-> orderbook internalFunction cep gpu
productKey->DOLPHIN
version->3.10
modules->15
authorization->trial
maxMemoryPerNode->512
licenseType->0
bindCores->
maxCoresPerNode->128
port->0
expiration->2024.09.30
```

