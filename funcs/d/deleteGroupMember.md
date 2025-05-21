# deleteGroupMember

## 语法

`deleteGroupMember(userIds, groupIds)`

## 参数

**userIds** 是表示用户名称的字符串标量或向量。

**groupIds** 是表示群组名称的字符串标量或向量。

*userIds* 和 *groupIds* 不能同时为向量。

## 详情

删除多个组中的同一个成员，或删除同一个组中的多个成员。

注： 该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 例子

```
deleteGroupMember(`AlexEdwards`ElizabethRoberts, `production);
```

**相关信息**

* [deleteGroup](deleteGroup.html "deleteGroup")
* [deleteUser](deleteUser.html "deleteUser")

