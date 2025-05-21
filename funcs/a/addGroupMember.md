# addGroupMember

## 语法

`addGroupMember(userIds, groupIds)`

## 参数

**userIds** 是一个表示用户名称的字符串。

**groupIds** 是一个表示群组名称的字符串。

*userIds* 和 *groupIds* 不能同时为向量。

## 详情

把用户添加到群组：

* 添加一个用户到一个群组
* 添加多个用户到一个群组
* 添加一个用户到多个群组

该操作可能会因为组所具有的权限而使入组用户的权限发生改变。

注： 该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 例子

添加一个用户（Even）到一个群组（adm 组）：

```
addGroupMember("Even", "adm");
```

添加多个用户（Alice 和 CardiB）到一个群组（adm 组）：

```
addGroupMember(["Alice","CardiB"], "adm");
```

添加一个用户（Carlos）到多个群组（adm 组和 prof 组）：

```
addGroupMember("Carlos", ["adm","prof"]);
```

