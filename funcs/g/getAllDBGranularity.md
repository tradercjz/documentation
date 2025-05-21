# getAllDBGranularity

## 语法

`getAllDBGranularity()`

## 参数

无

## 详情

该函数只能在数据节点上执行，用于列出该节点上所有数据库的分区粒度。

返回结果是一个字典，其中：

* key：数据库的名称。
* value：分区粒度，结果为 TABLE 或者 DATABASE。详细说明可参考 [database](../d/database.html)的参数*chunkGranularity*。

## 例子

```
getAllDBGranularity()

// output:
/valuedb->TABLE
```

