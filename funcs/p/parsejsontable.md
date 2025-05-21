# parseJsonTable

## 语法

`parseJsonTable(json, [schema],
[keyCaseSensitive=true])`

## 参数

**json** 包含 JSON 对象的字符串标量或向量。当 *json* 是字符串标量时，可以包含1个或多个 JSON 对象。暂不支持 JSON
数组和递归 JSON 对象。

**schema** 可选参数，表对象，用于指定各字段的数据类型。它可以包含以下列（必须包含 name 和 type 列）：

| 列名 | 含义 |
| --- | --- |
| name | 字符串，表示列名 |
| type | 字符串，表示各列的数据类型。 |
| format | 字符串，表示数据文件中日期或时间列的格式 |

如果不指定 *schema*，则函数将前10个 JSON 对象，自动解析表结构。

**keyCaseSensitive** 可选参数，表示 key 的名称是否大小写敏感。true（默认值）表示大小写敏感，false 表示大小写不敏感。

## 详情

将 JSON 对象解析为内存表。

* 当 *json* 是包含多个 JSON 对象的字符串时，每个对象都将转换为表的一行数据；例如，`{"ID":10,
  "NAME":"Riquelme","Club":"Boca Juniors"}`；
* 当 *json* 是字符串向量时，向量中每个 json 元素转换为表的一行数据。例如，[json1, json2, json3]。
* 当以上两种条件中的 json 包含空值时，即 {}，在转换后的表中，该空值所在行的位置相应留空。

## 例子

```
json1='{"ID":1, "NAME":"cc"}{"NAME":"dd"}'
parseJsonTable(json1)
```

返回：

| ID | NAME |
| --- | --- |
| 1 | cc |
|  | dd |

```
json2 = '{"col_test":"20190522150407"}'
schemaTB = table(["col_test"] as name, ["DATETIME"] as type, ["yyyyMMddHHmmss"] as format)
parseJsonTable(json2, schemaTB)

```

返回：

| col\_test |
| --- |
| 2019.05.22T15:04:07 |

当 *json* 是包含两个 JSON 对象的字符串时：

```
json3='{"ID":11, "NAME":"dd"}'
schemaTB1 = table(["ID", "NAME", "col_test"] as name, ["INT", "STRING", "DATETIME"] as type, [,,"yyyyMMddHHmmss"] as format)
parseJsonTable(concat([json2,json3]),schemaTB1)
```

返回：

| ID | NAME | col\_test |
| --- | --- | --- |
|  |  | 2019.05.22T15:04:07 |
| 11 | dd |  |

当 *json* 是字符串向量时：

```
parseJsonTable([json2,json3],schemaTB1)
```

返回：

| ID | NAME | col\_test |
| --- | --- | --- |
|  |  | 2019.05.22T15:04:07 |
| 11 | dd |  |

下例中定义了一个有三行数据的 json 对象 home，第三行数据为空（{}）。在第四行中，`parseJsonTable` 按照第三行中
*schemaLiga* 中定义的 *schema* 转换为名为 formation 的内存表。

```
home = ['{"Num":10, "Name":"Ronaldo","Goal":"3","MatchDay":"20120322"}','{"Num":3, "Name":"Carlos","Goal":"1","MatchDay":"20120322"}','{}'];
schemaLiga = table(["Num","Name","Goal","MatchDay"] as name, ["INT","STRING","INT","DATE"] as type, [,,,"yyyyMMdd"] as format);
formation = parseJsonTable(home,schemaLiga);
formation;
```

返回：

| Num | Name | Goal | MatchDay |
| --- | --- | --- | --- |
| 10 | Ronaldo | 3 | 2012.03.22 |
| 3 | Carlos | 1 | 2012.03.22 |
|  |  |  |  |

打印结果显示，原属于 json 对象 home 的第三行显示为空。

