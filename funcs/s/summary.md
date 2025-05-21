# summary

## 语法

`summary(X,[interpolation],[characteristic],[percentile],[precision],[partitionSampling])`

## 详情

生成数据的汇总统计信息，返回一个内存表，包含最小值、最大值、计数、均值、标准差和指定的百分位数（以升序输出）。

注：

* 若 *X* 是表，则 `summary`
  只统计表中数值类型的列，忽略非数值类型的列。
* 若 *X* 是数据源，则数据源只能包含数值类型的列，否则在进行
  `summary` 统计时会报错。

## 参数

**X** 可以是内存表、DFS 表或由 [sqlDS](sqlDS.md) 函数生成的数据源。注意：暂不支持由 `sqlDS` 生成的包含表连接的数据源。

**interpolation** 字符串，表示计算百分位采用的插值方法，可以是 'linear'（默认值）, 'nearst', 'lower',
'higher', 'midpoint'。

**characteristic** 字符串标量或向量，表示需要输出的统计特征。可选值为 'avg', 'std'。若不指定该参数，则默认同时输出 'avg' 和
'std'。

**percentile** DOUBLE 类型向量，范围是[0,100]。默认值为 [25, 50, 75]，表示返回第25, 50和75百分位数。

**precision** 大于0的 DOUBLE 类型标量，表示插值计算百分位时的迭代精度。默认值为
1e-3。当前计算结果与上一次迭代计算结果的差值小于等于该值时，将退出迭代。建议取值范围为[1.000e-3,
1.000e-9]，若值较小，则可能因迭代次数过多而导致性能下降；若值较大，则可能导致计算的结果不精确。

**partitionSampling**
正整数或(0,1]之间的浮点数。正整数表示随机选取的分区个数；浮点数表示随机选取相应比例的分区。若不指定，则表示选取所有分区。指定该参数时需要注意以下事项：

* 对于分区表：

  + 至少会选择1个分区，即当 *partitionSampling* 是浮点数，且
    partitionSampling \* 分区总个数小于1时，会选取1个分区；当 *partitionSampling*
    \* 分区总个数是大于1，但不是一个整数时，则向下取整。比如
    *partitionSampling*=0.26，分区总个数为10，则会随机选取2个分区。
  + 若指定的分区个数大于实际分区数量，则会选择所有分区。
* 对于非分区表，指定该参数不会生效；

## 例子

```
n=2022
data=1..n
value=take(1..3,n)
name=take(`APPLE`IBM`INTEL,n)
t=table(data,value,name);
summary(t, precision=0.001);
// name 非数值类型，不会输出到表中

```

输出返回：

| name | min | max | nonNullCount | count | avg | std | percentile |
| --- | --- | --- | --- | --- | --- | --- | --- |
| data | 1 | 2,022 | 2,022 | 2,022 | 1,011.5 | 583.8454 | [506.24,1011.50,1516.75] |
| value | 1 | 3 | 2,022 | 2,022 | 2 | 0.8167 | [1.00,1.99,2.99] |

```

n = 5000
data1 = take(1..5000000, n)
data2 = rand(10000000, n)
data3 = take("A" + string(0..10), n)

t = table(data1, data2, data3)
dbname = "dfs://summary"
if(existsDatabase(dbname)) {
    dropDatabase(dbname)
}
db = database(dbname, HASH, [INT, 10])
pt = createPartitionedTable(db, t, `pt, `data1)
pt.append!(t)

ds = sqlDS(<select data1,data2 from loadTable(db, `pt)>)
query_percentile = [25,50,75,90]

ds_re1 = summary(ds);

// 返回第25, 50, 75, 90 百分位值
ds_re2 = summary(ds, percentile=query_percentile, precision=0.0001);

// 分区占比为 0.6，即统计6个分区数据的信息
ds_re3 = summary(loadTable(db, `pt), percentile=query_percentile, precision=0.0001, partitionSampling=0.6);
```

