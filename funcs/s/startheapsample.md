# startHeapSample

## 语法

`startHeapSample(sampleParameter)`

## 参数

**sampleParameter** 长整型标量，表示采样阈值，单位为字节。在分配到指定字节的内存后会，将进行一次内存采样。取值范围是 [1,
524288]，建议设置为 524288。

## 详情

用于动态启用堆内存采样。调用后将动态设置环境变量 TCMALLOC\_SAMPLE\_PARAMETER
的值，从而使开发者能够监控和分析程序的内存使用情况。仅管理员可执行该函数。

## 例子

对内存使用情况进行分析的流程如下：

1. 启用堆内存采样。
2. 在可能发生内存泄漏的操作前、后分别执行
   `dumpHeapSample`，保存两个不同的文件。通过对比两个文件，确认操作涉及到的内存分配和使用情况。
3. 关闭堆内存采样。

```
startHeapSample(524288)

dumpHeapSample("/DolphinDB/Data/heap1")
dumpHeapSample("/DolphinDB/Data/heap2")

stopHeapSample()
```

相关函数：[dumpHeapSample](../d/dumpheapsample.md), [stopHeapSample](stopheapsample.md)

