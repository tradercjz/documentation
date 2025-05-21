# dumpHeapSample

## 语法

`dumpHeapSample(filename)`

## 参数

**filename** 字符串标量，表示堆内存快照的路径。

## 详情

生成当前堆内存的快照。调用此函数后，系统会记录当前的内存使用情况，包括已分配的内存块、它们的大小和状态等信息。仅管理员可执行该函数。

## 例子

对内存使用情况进行分析的流程如下：

1. 启用堆内存采样：可在启动 DolphinDB 前，设置环境变量 TCMALLOC\_SAMPLE\_PARAMETER 为1-524288之间的值（建议值
   524288）；或通过函数 `startHeapSample` 动态开启。
2. 在可能发生内存泄漏的操作前、后分别执行
   `dumpHeapSample`，保存两个不同的文件。通过对比两个文件，确认操作涉及到的内存分配和使用情况。
3. 关闭堆内存采样。

```
startHeapSample(524288)

dumpHeapSample("/DolphinDB/Data/heap1")
dumpHeapSample("/DolphinDB/Data/heap2")

stopHeapSample()
```

相关函数：[startHeapSample](../s/startheapsample.md),
[stopHeapSample](../s/stopheapsample.md)

