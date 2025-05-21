# toJson

## 语法

`toJson(X)`

## 参数

**X** 可以是任意数据类型。

## 详情

将 DolphinDB 对象转换为 JSON 字符串。该 JSON
字符串包含了5个键值对：name（变量名），form（数据结构），type（数据类型），size（长度），value（值）。

针对不同数据形式，`toJson` 最大可转换的数据长度不同：

| 数据形式 | 最大长度 |
| --- | --- |
| matrix | 300000 |
| set | 300000 |
| vector | 300000 |
| dict 键值对 | 300000 |
| table | 100000 |

## 例子

```
x=1 2 3
y=toJson(x)
y;
// output
{"name":"x","form":"vector","type":"int","size":"3","value":[1,2,3]}

t=table(1 2 3 as id, 10 20 30 as val)
toJson(t);
// output
{"name":"t","form":"table","size":"3","value":[{"name":"id","form":"vector","type":"int","size":"3","value":[1,2,3]},{"name":"val","form":"vector","type":"int","size":"3","value":[10,20,30]}]}

//set的长度超过30000，toJson最多只能转换前30000个元素
x=set(1..400001)
y=toJson(x)
size(fromJson(y))
// output
300000
```

相关函数：[fromJson](../f/fromJson.html)

