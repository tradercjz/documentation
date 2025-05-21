# createGroup

## 语法

`createGroup(groupId, [userIds])`

## 参数

**groupId** 是表示组名的字符串。

**userId** 是表示组成员的字符串标量或向量。

## 详情

创建组。

组中的用户必须是已经创建了的用户。

注： 该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 例子

创建组 "production"，并且把用户 "JohnSmith" 添加到该组。

```
createGroup(`production, `JohnSmith);
```

