# removeNode

## 语法

`removeNode(alias, [force=false])`

## 详情

删除集群中名为 *alias* 的计算节点。仅限 admin 用户调用。

此函数仅适用于 Linux 版本的 server。

## 参数

**alias** STRING 类型的标量或向量，代表需要删除的计算节点的别名。

**force** BOOL 类型的标量，表示是否强制删除节点：

* 当值为 false（默认值）时 ，表示不强制删除，即仅当节点处于关闭状态时才会删除。
* 当值为 true 时，表示强制删除，如果节点尚未关闭，则集群将会先关闭目标节点，然后再删除。此操作可能导致该节点正在进行的计算任务终止。

## 例子

删除别名为 "cnode1" 的计算节点，删除前需要手动关闭该节点。

```
removeNode(alias="cnode1")
```

强制删除别名为 "cnode2", "cnode3" 的计算节点。

```
removeNode(alias=`cnode2`cnode3, force=true)
```

