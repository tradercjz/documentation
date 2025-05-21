# getCacheEngineMemSize

## 语法

`getCacheEngineMemSize()`

## 参数

无

## 详情

查看当前节点下 OLAP 引擎的 Cache Engine 的内存情况，单位为字节。

返回一个 ANY VECTOR：

第1个元素表示 Cache Engine 正在使用的内存量；

第2个元素表示 Cache Engine 保存的列文件占用的内存；

第3个元素表示指向列文件的指针所占用的内存；

第4个元素表示 Cache Engine 允许使用的内存上限。

## 例子

```
setCacheEngineMemSize(0.4)
getCacheEngineMemSize()
// output
(0,0,0,429496729)
```

相关函数： [setCacheEngineMemSize](../s/setCacheEngineMemSize.html)

