# jsonExtract

## 语法

`jsonExtract(json, location, type)`

## 参数

**json** LITERAL 类型标量或向量，表示符合标准 JSON 字符串。

**location** 标量/向量/元组。每个元素可以是字符串或非零整数，用于指定相应维度的位置。

* 如果为字符串，表示查询指定键对应的元素。
* 如果为整数：表示查询该整数对应位置的元素。正整数表示从头开始查询，负整数表示从尾部开始查询。

**type** 字符串标量，表示返回结果的类型，可选值为 "long", "int", "double", "string" 。

## 详情

查询 JSON 对象中指定位置的数据，并按指定类型输出结果。

**返回值：**

* 当参数 *json* 为标量时，返回标量结果；为向量时，返回向量结果。
* 返回值类型由参数 *type* 指定。
* 如果参数 *location* 指定的元素不存在，或无法解析为指定的类型，则返回空值 。

## 例子

例1 基础用法

```
A = '{"a": "hello", "b": [-100, 200.5, 300], "c": { "b" : 2} }'
jsonExtract(A, [2, 1], "int")
// output: -100

jsonExtract(A, 1, "int")
// output: NULL

jsonExtract(A, 999, "int")
// output: NULL

jsonExtract(A, ["b", 2], "int")
// output: 200

jsonExtract(A, ["c", "b"], "double")
// output: 2

B = '{"a": "hello", "b": [200, 300]}'
jsonExtract([A, B], ["c", "b"], "int")
// output: [2, NULL]

jsonExtract([A, B], [2, -1], "int")
// output: [300, 300]
```

例2 查询表中 JSON 字符串里指定位置的数据。

```
A1 = '{"a": "a1","c": { "b" : 2} }'
A2 = '{"a": "a2", "c": { "b" : 3} }'
B1 = '{"a": "b1",  "c": { "b" : 3} }'
B2 = '{"a": "b2", "c": { "b" : 4} }'
t1 = table([A1, A2] as json, [2,3] as val)
t2 = table([B1, B2] as json, [3,4] as val)

select
    jsonExtract(t1.json, "a", "string") as json1,
    jsonExtract(t2.json, "a", "string") as json2
from t1
join t2 on t1.val = t2.val
```

| json1 | json2 |
| --- | --- |
| a2 | b1 |

