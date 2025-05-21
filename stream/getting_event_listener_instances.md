# 获取事件监听器实例

在 CEP 引擎中，`getEventListener` 是 monitor 的一个成员方法，可用于查询当前 monitor
中已注册的事件监听器实例。若指定 *listenerName*，则返回对应的事件监听器实例，否则返回所有事件监听器实例。

返回值为事件监听器实例，或一个字典（键为事件监听器名称， 值为事件监听器实例）。

**语法**

```
getEventListener([listenerName])
```

**参数**

**listenerName** 字符串标量，表示事件监听器名称。

**示例**

```
listeners = getEventListener('Stock')
```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
