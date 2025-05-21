# groups

## 语法

`groups(X, [mode='dict'])`

## 参数

**X** 是一个向量。

**mode** 可选参数，用于指定 `groups` 返回值的数据形式，默认为
"dict"。可指定为以下值：

* "dict"：返回一个字典。字典的 key 存储 *X* 中的独特值（unique
  value）；字典的 value 为一个向量，存储该值在 *X* 中对应的下标。
* "table"：返回一个包含两列的表。字段为 "key" 和 "index"，分别存储 *X*
  中的独特值和其在 *X* 中对应的下标。
* "vector"：返回一个 array vector，按照 *X*
  中独特值升序排列，存储每个独特值在 *X* 中对应的下标。
* "tuple"：返回一个 tuple，其存储方式同 *mode*="vector"。

## 详情

对 *X* 中每一个独特值，列出其在 *X* 中的所有对应数据的下标。

若 *mode* = 'dict'，返回一个字典；若 *mode* =
'table'，返回一个数据表，其中 index 列表示下标，为数组向量类型。

## 例子

```
x=NULL NULL 12 15 12 16 15 14 NULL NULL
groups(x);

// output
16->[5]
->[0,1,8,9]
12->[2,4]
14->[7]
15->[3,6]

groups(x, "vector")
// output
[[0,1,8,9],[2,4],[7],[3,6],[5]]

groups(x, "tuple")
// output
([0,1,8,9],[2,4],[7],[3,6],[5])

groups(x, "table")
```

| key | index |
| --- | --- |
|  | [0,1,8,9] |
| 2 | [2,4] |
| 4 | [7] |
| 5 | [3,6] |
| 6 | [5] |

