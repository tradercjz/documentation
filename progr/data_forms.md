# 数据形式

DolphinDB 支持以下数据形式：

| 名称 | ID | 例子 |
| --- | --- | --- |
| 标量 | 0 | 5, 1.3, 2012.11.15, `hello |
| 向量 | 1 | * 常规向量：5 4 8 或 [5, 4, 8] * 元组：(1 2 3, ["I","M","G"], 2.5) * 数组向量：[arrayVector](data_types_forms/arrayVector.md) * 大数组：[bigArray](data_types_forms/BigArray.md) * 列式元组：[columnar   tuple](data_types_forms/columnarTuple.md) |
| 数据对 | 2 | 3:5; 'a':'c'; "Tom":"John"。参考：  * [pair](../funcs/p/pair.md) |
| 矩阵 | 3 | 1..6$2:3 or reshape(1..6, 2:3)。参考：  * 普通矩阵：[matrix](../funcs/m/matrix.md) * 索引矩阵：[setIndexedMatrix!](../funcs/s/setIndexedMatrix_.md) * 索引序列：[indexedSeries](../funcs/i/isIndexedSeries.md), [setIndexedSeries!](../funcs/s/setIndexedSeries_.md) |
| 集合 | 4 | [set](../funcs/s/set.md) |
| 字典 | 5 | * 有序/无序字典：[dict](../funcs/d/dict.md) * 有序/无序同步字典：[syncDict](../funcs/s/syncDict.md) |
| 表 | 6 | * 内存表：   + 常规表：[table](../funcs/t/table.md)   + 索引表：[indexedTable](../funcs/i/indexedTable.md)   + 键值表：[keyedTable](../funcs/k/keyedTable.md)   + 流数据表：[streamTable](../funcs/s/streamTable.md),[haStreamTable](../funcs/h/haStreamTable.md), [keyedStreamTable](../funcs/k/keyedStreamTable.md)   + 缓存表：[cachedTable](../funcs/c/cachedTable.md)   + 分区表：[createPartitionedTable](../funcs/c/createPartitionedTable.md)   + 跨进程共享内存表：[createIPCInMemoryTable](../funcs/c/createIPCInMemoryTable.md) * 分布式表：   + 分区表：[createPartitionedTable](../funcs/c/createPartitionedTable.md)   + 维度表：[createTable](../funcs/c/createTable.md) * 多版本并发控制表：[mvccTable](../funcs/m/mvccTable.md) |
| 张量 | 10 | 通过 [tensor](../funcs/t/tensor.md) 函数，创建张量。例如：  1 维张量：`tensor(1..100)`  2 维张量：`tensor(1..10$5:2)`  3 维张量：`tensor((rand(1.0, 6)$3:2, rand(1.0, 6)$3:2))`  …  n 维张量，其中 n 不能大于10。  注意：   * 目前张量仅支持如下类型：BOOL, CHAR, SHORT, INT, LONG, FLOAT, DOUBLE。 |

可以通过 [form](../funcs/f/form.md) 函数来取得一个变量或者常量的数据形式。

```
form false;
// output: 0

form `TEST;
// output: 0

form `t1`t2`t3;
// output: 1

form 1 2 3;
// output: 1

x= 1 2 3
if(form(x) == VECTOR){y=1};
y;
// output: 1

form 1..6$2:3;
// output: 3

form(tensor(1..10$5:2))
// output: 10
```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
