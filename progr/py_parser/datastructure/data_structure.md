# 数据结构

列表（list），元组（tuple），字典（dict），集合（set）是 Python 最基础的数据结构。Python Parser 支持这些基础数据结构的同时进行了拓展，以更好地支持 DolphinDB 的运行环境，如：在 Python 的数据结构中支持定义 DolphinDB 对象，支持将 Python 对象转换为 DolphinDB 对象等。

## Python Parser 对象支持的操作方法

| 方法 | 含义 |
| --- | --- |
| type(obj) | 查看对象的类型 |
| dir(obj) | 查看对象支持的方法 |
| help(obj) | 查看对象的方法定义 |
| id(obj) | 返回对象的唯一标识符（对象的地址） |
| str(obj) | 将对象转化为字符串 |
| len(obj) | 返回对象的长度 |
| hash(obj) | 获取对象的哈希值 |
| range(stop) or range(start, stop[, step]) | 获取一个整数列表（可迭代对象） |
| iter(iterable) | 生成迭代器 |

## Python Parser 数据结构与 DolphinDB 数据结构的对比

下表中的内置函数是指 DolphinDB 的内置函数。若 DolphinDB 和 Python Parser 存在同名函数，则系统优先解析为 Python 的内置函数，若需要使用 DolphinDB 的内置函数，则需要通过 import dolphindb as ddb 导入 dolphindb 库，调用该库中的函数。

| **DolphinDB** | **Python Parser** |
| --- | --- |
| scalar | 保持一致 |
| regular vector | list.toddb()，其中 list 必须是强类型的 |
| any vector | list.toddb() 或 tuple.toddb() |
| HUGE vector | 内置函数 [bigarray](../../../funcs/b/bigarray.html) 创建 |
| array vector | 内置函数 [arrayVector](../../../funcs/a/arrayVector.html) 创建 |
| subarray | 内置函数 [subarray](../../../funcs/a/arrayVector.html) 创建 |
| pair ( : ) | 内置函数 [pair](../../../funcs/p/pair.html) 创建 |
| matrix / cast（ $ ） | 通过内置函数 [matrix](../../../funcs/m/matrix.html) 转换 |
| set | set.toddb() / ddb.set |
| dict / | dict.toddb() / ddb.dict |
| table | 通过内置函数 [table](../../../funcs/t/table.html) 转换 |

**注意**：

* DolphinDB 中不允许通过 [NULL, NULL] 的方式创建 VOID 类型的向量，但 Python Parser 中可以通过 [None, None].toddb() 创建类型为 ANY 空向量。

