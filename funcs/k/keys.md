# keys

## 语法

`keys(X)`

## 参数

**X** 是一个字典、数据表，或集合。

## 详情

返回一个字典中的所有键作为一个向量，或一个数据表中的列名作为一个向量，或将一个集合转化为一个向量。

## 例子

```
z=dict(INT,DOUBLE)
z[5]=7.9
z[3]=6
z.keys();
// output
[3,5]

t = table(1 2 3 as id, 4 5 6 as x, `IBM`MSFT`GOOG as name);
keys(t);
// output
["id","x","name"]

a=set(1 2 4)
a.keys();
// output
[4,2,1]
```

相关函数：[values](../v/values.html)

