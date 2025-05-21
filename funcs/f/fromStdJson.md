# fromStdJson

## 语法

`fromStdJson(X)`

## 参数

**X** 符合标准 JSON 格式的字符串，或由这些字符串组成的向量。

## 详情

将标准 JSON 文本转化为符合 DolphinDB 规范的数据。

转换规则说明：

| JSON 数据类型 | 对应 DolphinDB 数据类型/形式 |
| --- | --- |
| 对象 | 转换为字典，key 类型始终为 STRING；如果其 value 由多种类型组成，那么 value 的类型为 ANY。 |
| 数组 | 向量 |
| 字符串 | 优先解析为 TEMPORAL 类型；如果解析失败，则转换为 STRING。 |
| 数字 | DOUBLE |
| 布尔值 | BOOL |
| null | NULL |

注：

该函数会自动解析表示转义的特殊字符，如 `\n`、`\r` 等。

## 例子

```
X = "\"\\u4e2d\\u6587\"";
fromStdJson(X);
//output: 中文

X = "\"\\u4e2d\\n\\u6587\"";
fromStdJson(X);
//output: 中
//        文

X = "[1, 2, 3]";
fromStdJson(X);
//output:[1,2,3]

X = "[1, null, false, \"2012.06.13 13:30:10\", [\"\\u5d4c\\u5957\\u6570\\u7ec4\"]]";
fromStdJson(X);
//output:(1,,false,2012.06.13T13:30:10,["嵌套数组"])

X = "{\"1\": \"2017.07.10 14:10:12\",\"0\": \"2012.06.13 13:30:10\"}";
fromStdJson(X);
//output:1->2017.07.10T14:10:12
//       0->2012.06.13T13:30:10
```

相关函数：[toStdJson](../t/toStdJson.md)

