# removeTopicOffset

## 语法

`removeTopicOffset(topic)`

## 参数

**topic** 是 [subscribeTable](../s/subscribeTable.html) 函数返回的订阅主题。

## 详情

删除给定订阅主题（topic）的持久化保存的最新一条已经处理订阅数据的偏移量（在 [subscribeTable](../s/subscribeTable.html)
函数中通过指定 *persistOffset* 参数为 true 获得）。

