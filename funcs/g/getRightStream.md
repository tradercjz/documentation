# getRightStream

## 语法

`getRightStream(joinEngine)`

## 参数

**joinEngine** 创建连接引擎返回的对象。目前 DolphinDB 支持的连接引擎有：

* createAsofJoinEngine
* createEquiJoinEngine
* createLookupJoinEngine
* createWindowJoinEngine
* createLeftSemiJoinEngine

## 详情

返回连接引擎右表的表结构对象。向该对象注入的数据，会注入到 *joinEngine* 中。

通过该函数，可以将一个引擎的计算结果直接注入到连接引擎中，实现引擎间的级联。

使用案例请参考 [getLeftStream](getLeftStream.md)。

