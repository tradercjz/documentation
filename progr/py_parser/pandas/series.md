# Series

Series 是 DolphinDB pandas 中最常用的数据结构之一。它是一维标签化的数组，每个 Series 都由两个主要部分组成：数据和索引。数据部分包含存储在 Series 中的实际值，而索引部分是用于标识和访问这些值的标签。它可以保存不同类型的数据，如数值、字符串、布尔值等。其构造如下：

## 构造函数

```
Series(data=None, index=None, lazy=False)
```

* **data**: 可以是 Python list, DolphinDB Vector, pandas Series 或空值，必须是强类型。
* **index**：可以是 Python list, DolphinDB Vector, pandas Series, 单层索引或空值，必须是强类型。暂不支持多层级索引。
* **lazy**：可选参数，为一个布尔值，默认为 True。表示是否创建一个惰性的 Series。惰性 Series 是原对象的一个视图，计算操作不会立即执行；非惰性 Series 是原对象的一个拷贝，计算操作会立即执行。

**注意**：

* 暂不支持 *data* 指定为分区表的列。
* 若 *data* 为空，在创建 Series 时，会自动填充为 None，类型为 DOUBLE。
* 若 *data* 指定为 Series，则不能指定 *index*。
* *lazy* = True 时，*index* 不能包含元素全部是 None 的 list，例如：[None,None]。

**使用前说明：**

* Series 类中函数的 *dtype* 参数只能指定为 DolphinDB 的数据类型，例如：ddb.DOUBLE, ddb.STRING。
* 目前 DolphinDB 支持的 Series 中的部分函数仅支持了部分参数，必须通过 keywords 方式传参。举例说明：DolphinDB 的 Series.groupby 函数仅支持 *by* 和 *dropna* 参数，其参数调用方式为：`Series.groupby(by=["a", "a", "b", "b"], dropna=False)`。

## 属性

### Axis

支持的 axis 属性见下表：

| 方法 | 描述 | 兼容性说明 |
| --- | --- | --- |
| Series.index | Series 的索引（axis 标签）。 | 不支持多层索引 |
| Series.values | 返回 DolphinDB 的向量。 |  |

## 转换

目前支持以下函数：

| 方法 | 描述 | 兼容性说明 |
| --- | --- | --- |
| Series.astype(dtype[]) | 将 pandas 对象转换为指定的 dtype。 | 暂不支持 *copy* 和 *errors* 参数。 |
| Series.copy() | 复制该对象的索引和数据。 | 暂不支持 *deep* 参数。 |
| Series.bool() | 返回由布尔类型标量组成的 Series 的布尔值。 |  |
| Series.to\_list() | 返回值的列表。 |  |

## 索引、迭代

目前支持以下函数：

| 方法 | 描述 | 兼容性说明 |
| --- | --- | --- |
| Series.get(key) | 从给定键的对象中获取数据。 | 对 Series 使用 get(None) 或 get(ddb.NULL) 时将返回 None。 |
| Series.at | 访问标签对应的单个值。 | 对 Series 使用 at[i]=val 修改数据时，如果 val 与原 Series 的类型不同，将会尝试类型转换。若无法转换，则报错。 通过 at 获取惰性 Series 的返回值仍是一个 Series。 |
| Series.iat | 按整数位置访问标签对应的单个值。 | 同上 |
| Series.loc | 通过标签或布尔数组访问一组行和列。 | 同上 |
| Series.iloc | 仅基于整数位置的索引以按位置选择。 | 同上 |
| Series.keys() | 返回索引的别名。 |  |
| Series.pop(item) | 从 Series 中删除数据，并将它返回。 |  |
| Series.item() | 返回由标量组成的 Series 的数据 |  |
| Series.xs(key[, axis, level, drop\_level]) | 返回 Series 指定横截面（cross-section）的数据。 |  |

## 二元运算符函数

支持 Python pandas.Series 中的所有[二元运算符函数](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#binary-operator-functions)。但需要注意以下几点：

* 所有函数均不支持 *level* 参数。
* 所有函数中的 *other* 参数仅支持 scalar, DolphinDB vector, list, Series 四种数据类型，不支持 DataFrame。
* 若 **eq** 函数的 *other* 参数是 scalar，则不能指定 *fill\_value* 参数。
* **combine** 函数中 *func* 参数仅支持内置函数，不支持用户自定义函数。

## 函数应用、GroupBy 和窗口

以下函数的 *func* 参数只能是 pandas 内置函数、自定义函数（包括 lambda 表达式）。暂不支持 \*\*kwargs 参数。

| 方法 | 兼容性说明 |
| --- | --- |
| Series.apply(func[, args]) | 不支持参数 *convert\_dtype* |
| Series.agg(func) | 不支持参数 *axis* |
| Series.aggregate(func) | 不支持参数 *axis* |
| Series.transform(func) | 不支持参数 *axis* |
| Series.groupby(by,dropna=True) | 不支持参数 *axis*, *level*, *as\_index*, *sort*, *group\_keys*, *squeeze*, *observed* |
| rolling | 不支持参数 *center*, *win\_type*, *on*, *axis*, *closed*, *step*, *method* |
| ewm | 不支持参数 *ignor*e, *axis*, *times*, *method* |
| map | 不支持指定 *arg* 参数为 Series |

## 计算/描述性统计

已经支持 [Computations / descriptive stats](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#computations-descriptive-stats) 中的以下函数：**abs**, **all**, **any**, **autocorr**, **between**, **corr**, **count**, **cov**, **diff**, **kurt**, **kurtosis**, **mad**, **max**, **mean**, **median**, **min**, **mode**, **nlargest**, **nsmallest**, **prod**, **sem**, **skew**, **std**, **sum**, **var**, **unique**, **nunique**, **is\_unique**, **is\_monotonic\_increasing**, **is\_monotonic\_decreasing**, **value\_counts**。

**注意**：

* 所有函数均不支持 *axis*, *skipna*, *bool\_only*, *fill\_value*, *min\_count*, *ddof* 参数。
* 除 **count**, **mad**, **max**, **mean**, **median**, **min**, **prod**, **skew**, **sum**, **sem**, **std**, **var** 函数外，其它函数均不支持 *level* 参数。
* 此外，部分函数暂时还不支持某些参数，详见下表：

| method | 兼容性说明 |
| --- | --- |
| **corr** | 不支持参数 *method*, *min\_periods* |
| **cov** | 不支持参数 *min\_period*, *ddof* |
| **diff** | 不支持参数 *periods* |
| **kurt** | 不支持参数所有参数 |
| **kurtosis** | 不支持参数所有参数 |
| **std** | 不支持参数 *ddof* |
| **value\_counts** | 不支持参数 *bins* |

## 重新索引/选择/标签操作

目前支持 [Reindexing / selection / label manipulation](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#reindexing-selection-label-manipulation) 中的以下函数：**drop**, **drop\_duplicates**, **first**, **head**, **idxmax**, **idxmin**, **isin**, **last**, **reindex**, **reset\_index**。部分函数暂时还不支持某些参数，详见下表：

| method | 兼容性说明 |
| --- | --- |
| **drop** | 不支持参数 *axis*, *columns*, *inplace*, *errors* |
| **drop\_duplicates** | 不支持参数 *inplace*, *ignore\_index* |
| **idxmax/idxmin** | 不支持参数 *axis* |
| **reindex** | 不支持参数 *copy*, *level*, *tolerance* |
| **reset\_index** | 不支持参数 *inplace*, *allow\_duplicates* |
| **head** | 不允许参数 *n* = 0 |
| **take** | 不支持参数 *axis* |

## 缺失数据处理

目前支持 [Missing data handling](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#missing-data-handling) 中的以下函数：**backfill**, **isnull**, **notnull**, **pad**。

**注意**：所有函数均不支持 *axis* 和 *downcast*, *inplace*, *limit* 参数。

## 重塑、排序

目前支持 [Reshaping, sorting](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#reshaping-sorting) 中的以下函数：**argsort**, **argmin**, **argmax**, **sort\_values**, **sort\_index** 函数。

**注意**：所有函数都不支持 *axis* 参数。部分函数不支持某些参数，详见下表：

| method | 兼容性说明 |
| --- | --- |
| **argsort** | 不支持参数 *kind*, *na\_position* |
| **sort\_values/sort\_index** | 不支持参数 *inplace*, *kind*, *na\_position* |

## 组合/比较/连接/合并

已经支持 [Combining / comparing / joining / merging](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#combining-comparing-joining-merging) 中的函数。部分函数不支持某些参数，详见下表：

| method | 兼容性说明 |
| --- | --- |
| **compare** | 仅支持 *align\_axis* =1 |
| **update** |  |

## 时间序列相关

已经支持 [Time Series-related](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#time-series-related) 中的大部分函数。暂不支持 **tz\_convert** 和 **tz\_localize** 函数。部分已支持的函数的兼容性，详见下表：

| method | 兼容性说明 |
| --- | --- |
| **asfreq** | 不支持参数 *method*, *how*, *normalize*, *fill\_value* |
| **asof** | 不支持参数 *subset* |
| **shift** | 不支持参数 *axis*, 参数 *freq* 仅支持 [asfreq](../../../funcs/a/asFreq.md) 中列出的规则 |
| **resample** | 不支持参数 *on*, *loffset*, *base*, *group\_keys* |
| **at\_time** | 不支持参数 *asof*, *axis* |
| **between\_time** | 不支持参数 *include\_start*, *include\_end*, *axis* |

## 创建 Series

* 不指定 index，则索引值从 0 开始。

```
s = pd.Series([20, 21, 12])
print(s)
// output：
0  20
1  21
2  12
dtype: INT
```

* 指定单列索引

```
pd.Series([20, 21, 12], ['London', 'New York', 'Helsinki'])
print(s)
// output：
  London  20
New York  21
Helsinki  12
dtype: INT
```

## 访问 Series

```
city = ['London', 'New York', 'Helsinki']
s = pd.Series([20, 21, 12], city)
```

（1）隐式访问

* 访问单个元素

```
s[0]
s.iloc[0]
s.iat[0]
// output: 20
```

* 访问多行

```
s[[0,2]]
s.iloc[[0,2]]
// output:
London     20
Helsinki   12
dtype: INT
```

* 切片访问

```
s[0:3]
s.iloc[0:3]
// output：
  London  20
New York  21
Helsinki  12
dtype: INT
```

```
s[:2]
s.iloc[:2]
// output：
  London  20
New York  21
dtype: INT
```

```
s[1:]
s.iloc[1:]
// output：
New York  21
Helsinki  12
dtype: INT
```

```
s[:]
s.iloc[:]
// output：
  London  20
New York  21
Helsinki  12
dtype: INT
```

（2）显式访问

* 单标签访问单个元素

```
s['London']
s.loc['London']
// output：20
```

* 单标签访问多个元素

```
s[['London', 'New York']]
s.loc[['London', 'New York']]
// output:
  kind
  A  20
  B  21
dtype: INT
```

* 切片访问

```
s['London':'Helsinki']
s.loc['London':'Helsinki']
// output:
    city  kind
  London     A  20
New York     B  21
Helsinki     A  12
dtype: INT
```

```
s[:]
s.loc[:]
// output:
    city  kind
  London     A  20
New York     B  21
Helsinki     A  12
dtype: INT
```

**注意**：暂不支持多标签访问时，通过切片访问全元素

```
s[:, 'A']
s.loc[:, 'A']
```

## 更新 Series

（1）追加数据

暂不支持。

（2）更新数据

* 直接修改元素：支持通过索引修改，暂不支持通过下标修改。

  ```
  s.loc["London"] = 33
  s[1] = 33 # supported
  ```
* 通过 update 函数更新数据

```
city = ['London', 'New York', 'Helsinki']
s = pd.Series([20, 21, 12], city)
s.update(pd.Series([50,60], index=['London', 'Helsinki']))
s

// output
  London  50
New York  21
Helsinki  60
dtype: INT
```

（3） 删除 Series 数据

* drop

```
s.drop(["London"])
```

## Series 间的运算

* 基础的运算规则：索引值对齐后进行运算。例如：如果 s1 中没有对应 s 的索引，则计算结果为 NaN。

```
s=pd.Series([12, 15],["London","New York"])
city = ['London', 'Helsinki']
s1 = pd.Series([33, 25], city)
s + s1
// output：
Helsinki  NaN
  London   45
New York  NaN
dtype: INT
```

