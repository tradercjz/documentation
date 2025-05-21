# setSystem

## 语法

`setSystem(paramName, paramValue)`

## 参数

**paramName** 是参数名，**paramValue** 是对应的参数值。

## 详情

`setSystem` 用于设置以下的系统级参数：

* 在命令行窗口显示的对象的最大行数
* 在命令行窗口显示的对象的最大行宽

只有管理员有权限执行 `setSystem` 命令。

## 例子

```
setSystem("rows", 30);
setSystem("width", 200);
```

