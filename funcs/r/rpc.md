# rpc

## 语法

`rpc(nodeAlias, func, args, ...)`

## 参数

**nodeAlias** 是远程节点的别名。

**func** 是函数，它不能被引用。这个函数可以是内置函数或调用节点上的用户自定义函数。

**args** 是函数的参数。

## 详情

在指定的远程节点上调用本地函数，并把结果返回到本地节点。这个函数可以是内置函数或调用节点上的用户自定义函数。函数的参数暂不支持值为函数定义的字典。

调用节点和远程节点必须在同一集群。否则，我们需要使用 [remoteRun](remoteRun.html) 函数。详情请参考 [BatchJobManagement](../../sys_man/BatchJobManagement.html)。

## 例子

* 远程调用用户定义函数

  ```
  rpc("nodeA", def(x,y):x+y, 10, 15)
  ```
* 远程调用部分应用

  ```
  rpc("nodeA", getRecentJobs{10})
  ```
* 远程调用引用了用户定义函数的内置函数

  ```
  def jobDemo(n){
      s = 0
      for (x in 1 : n) {
         s += sum(sin rand(1.0, 100000000)-0.5)
             print("iteration " + x + " " + s)
      }
      return s
  };
  // the node "DFS_NODE2" is located in the same cluster as the local node.
  rpc("DFS_NODE2", submitJob, "jobDemo3", "job demo", jobDemo, 10);
  // output:
  jobDemo3

  rpc("DFS_NODE2", getJobReturn, "jobDemo3")
  // output:
  -3426.577521
  ```

