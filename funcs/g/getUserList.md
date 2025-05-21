# getUserList

## 语法

`getUserList()`

## 详情

返回包含除管理员之外的所有用户名称的向量。

注： 该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 例子

```
login(`admin, `123456);
getUserList().sort();
// output
["AA","AAA","BB","BBB","CC","DeionSanders","EliManning","JoeFlacco"]
```

