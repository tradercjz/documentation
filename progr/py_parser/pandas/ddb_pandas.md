# DolphinDB pandas

## 概述

基于 Python 的 pandas 库（V2.1.0），DolphinDB Python Parser 开发了自身的 pandas 库，简称为 DolphinDB pandas。DolphinDB pandas 与传统的 Python pandas 存在以下不同：

* DolphinDB pandas 在设计 Series 和 DataFrame 类时引入了惰性（lazy）和非惰性（non-lazy）两种模式。这两种模式下 Series 和 DataFrame 的计算方式不同。举例来说，对于 DataFrame，non-lazy 模式下会立即执行计算，这与 Python pandas 中 DataFrame 的行为相同。而在 lazy 模式下，DolphinDB pandas 的 DataFrame 会存储所有函数调用，尽可能延迟计算，以减少计算带来的性能消耗。这种设计能更好地满足不同的计算需求。
* DolphinDB pandas 内置于 DolphinDB server 中，可以与其内的数据库、计算引擎等无缝结合，实现高效处理大规模数据、不需要额外导入数据与进行数据类型转换、并行处理数据等功能，进一步提高了数据分析效率。

目前，DolphinDB pandas 库只支持 Series 和 DataFrame 两个类。关于这些类中的函数及参数的支持性请查阅相关章节。

## 使用方法

DolphinDB server 内置了 pandas 库，直接通过 `import` 语句导入即可使用：

```
import pandas as pd
```

## 兼容性说明

DolphinDB pandas 的函行为在某些方面与 Python pandas 不一致，本节主要讲述对所有函数通用的不兼容行为：

* DolphinDB pandas 中的字符串无法转换为数字类型进行计算。
* DolphinDB pandas 中的空值作为最小值，将排在排序结果的第一位。
* complex 类型的数据在涉及到排序的行为（如 sort/groupby ）时，DolphinDB pandas 会将其转换为整型后进行排序。
* DolphinDB pandas 的函数中指定一个参数为 None 时，等同于未指定该参数。
* DolphinDB pandas 中 None 与 dolphindb.NULL 完全等价。即 None==dolphindb.NULL 的结果为 True，同时 None==None 的结果也为 True。
* DolphinDB pandas 在初始化 Series 或 DataFrame 对象时，会将传入的元素全部为 None 的 list 转换为 dolphindb.DOUBLE 类型。
* 在惰性模式下，访问数据发生越界时，会返回空的 Series 或 DataFrame。

