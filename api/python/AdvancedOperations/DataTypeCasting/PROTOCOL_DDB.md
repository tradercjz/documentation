# PROTOCOL\_DDB

PROTOCOL\_DDB 作为 DolphinDB 自定义的一套数据序列化、反序列化方案，广泛使用于 Python API、C++ API、Java API 等 API 中，且其支持的**数据形式**和**数据类型**最为全面。

* **注1**： 数据形式指 DolphinDB 类型系统中的 DATAFORM，表示数据结构的形式，通常包含 Scalar、Vector、Table 等。
* **注2**： 数据类型指 DolphinDB 类型系统中的 DATATYPE，表示数据的具体类型，通常包含 INT、DOUBLE、DATETIME 等。
* **注3**： 以下简称 Python 库 NumPy 为 **np**，pandas 为 **pd**。

## 启用 PROTOCOL\_DDB

在以下示例中，session 和 DBConnectionPool 通过设置参数 *protocol* 指定启用 PROTOCOL\_DDB 协议。

```
import dolphindb as ddb
import dolphindb.settings as keys

s = ddb.session(protocol=keys.PROTOCOL_DDB)
s.connect("localhost", 8848, "admin", "123456")

pool = ddb.DBConnectionPool("localhost", 8848, "admin", "123456", 10, protocol=keys.PROTOCOL_DDB)
```

## PROTOCOL\_DDB 数据形式支持表

PROTOCOL\_DDB 支持的数据形式如下表展示：

| 附加参数 | 数据形式 | 序列化 | 反序列化 |
| --- | --- | --- | --- |
| pickleTableToList=False | Scalar | 支持 | 支持 |
| pickleTableToList=False | Vector | 支持 | 支持 |
| pickleTableToList=False | Pair | 不支持 | 支持 |
| pickleTableToList=False | Matrix | 支持 | 支持 |
| pickleTableToList=False | Set | 支持 | 支持 |
| pickleTableToList=False | Dict | 支持 | 支持 |
| pickleTableToList=False | Table | 支持 | 支持 |
| pickleTableToList=True | Table | 不支持 | 支持 |

## 序列化 Python->DolphinDB

本节以 upload 函数为例，介绍在使用协议 PROTOCOL\_DDB 上传 Scalar、Vector，Pair 等类型数据时分别对应的 DolphinDB 数据类型。若 Python 中不存在与 DolphinDB 对应的数据类型，则该行显示为“---”。

### Scalar

下表展示上传 Scalar 型数据时，DolphinDB 与 Python 对应的数据类型与示例数据。

| Python 类型 | Python 示例数据 | DolphinDB 类型 | DolphinDB 示例数据 |
| --- | --- | --- | --- |
| NoneType | None | VOID | NULL |
| bool | True | BOOL | 1b, true |
| np.int8 | np.int8(12) | CHAR | char(12), 12c |
| np.int16 | np.int16(12) | SHORT | short(12), 12h |
| np.int32 | np.int32(12) | INT | int(12), 12 |
| np.int64 | np.int64(12) | LONG | long(12), 12l |
| int | 12 | LONG | long(12), 12l |
| np.datetime64[D] | np.datetime64("2012-01-02", "D") | DATE | 2012.01.02 |
| np.datetime64[M] | np.datetime64("2012-01", "M") | MONTH | 2012.01M |
| --- | --- | TIME | --- |
| --- | --- | MINUTE | --- |
| --- | --- | SECOND | --- |
| np.datetime64[s] | np.datetime64("2012-01-02T01:02:03", "s") | DATETIME | datetime(2012.01.02T01:02:03) |
| np.datetime64[ms] | np.datetime64("2012-01-02T01:02:03.123", "ms") | TIMESTAMP | timestamp(2012.01.02T01:02:03.123) |
| --- | --- | NANOTIME | --- |
| np.datetime64[ns] | np.datetime64("2012-01-02T01:02:03.123456789", "ns") | NANOTIMESTAMP | nanotimestamp(2012.01.02T01:02:03.123456789) |
| np.datetime64 | np.datetime64("") | NANOTIMESTAMP | nanotimestamp(NULL) |
| pd.Timestamp | pd.Timestamp("2012-01-02T01:02:03.123456789") | NANOTIMESTAMP | nanotimestamp(2012.01.02T01:02:03.123456789) |
| pd.NaTType | pd.NaT | NANOTIMESTAMP | nanotimestamp(NULL) |
| np.float32 | np.float32(1.1) | FLOAT | float(1.1), 1.1f |
| np.float64 | np.float64(1.2) | DOUBLE | double(1.2) |
| float | 1.2 | DOUBLE | double(1.2) |
| float | np.nan | DOUBLE | double(NULL) |
| str | "abc" | STRING | "abc" |
| str | "" | STRING | "" |
| --- | --- | SYMBOL | --- |
| --- | --- | UUID | --- |
| np.datetime64[h] | np.datetime64("2012-01-02T01", "h") | DATEHOUR | 2012.01.02T01 |
| --- | --- | IPADDR | --- |
| bytes | bytes("abc", encoding="UTF-8") | BLOB | "abc" |
| --- | --- | DECIMAL32 | --- |
| Decimal | decimal.Decimal("-10.21") | DECIMAL64 | decimal64(-10.21, 2) |
| Decimal | decimal.Decimal("NaN") | DECIMAL64 | decimal64(NULL, 2) |
| Decimal | decimal.Decimal(“-10.00000000000000000021“) | DECIMAL128 | decimal128(“-10.00000000000000000021“, 20) |

**注意**：

* Python API 自 1.30.22.6 版本起支持数据类型 Decimal128。上传 Decimal 标量（Scalar）对象时，如果保留的小数位数（scale）小于或等于 17，则作为 Decimal64 上传；如果保留的小数位数（scale）大于 17，则作为 Decimal128 上传。
* 自 2.0.11.0 版本起，不再限制上传的 BLOB 类型数据的长度；对于上传的 SYMBOL/STRING 类型数据，其长度必须小于 256 KB。

### Vector

和 Scalar 类似，由于 DolphinDB 与 Python 的类型系统并不是一一对应的关系，因此 API 无法直接向 DolphinDB 上传 TIME、UUID 等类型的 Vector。

类型转换的处理逻辑如下：

1. 判断当前对象是否为 Vector 型数据，如 tuple、list、np.ndarray、pd.Series等。
2. 如果当前对象为 np.ndarray 等类型确定的对象时，且 np.ndarray 的 dtype 不为 object，则直接进行类型转换。该种情况下的数据转换效率较高。
3. 如果当前对象为 list 等类型不确定的对象，或者是 dtype 为 object 的 np.ndarray 对象，则需要遍历一遍上传的数据后再进行判断。在此过程中，

   * 若数据中包含空值（None, np.nan, pd.NaT），则将根据第一个非空值类型确认该 Vector 型数据的类型。
   * 若遍历过程中发现有 **两种及两种以上（注1）** 的数据类型数据，或者包含 Vector 型数据，则将会判断为 Any Vector。该种情况下需要逐个对数据进行类型转换，且需要额外遍历，转换效率较差。
4. 在判断 Vector 型数据的元素类型时，基本遵循和 Scalar 一致的判断规则，因此，Python API 也不支持直接上传 MINUTE、UUID 等类型的 Vector 型数据。
5. 如果一个 np.ndarray 对象中的元素都为长度相等的 Vector 型数据，则会优先判断为 Matrix 类型。
6. 如果上传的对象不是 np.ndarray，但是却包含长度一致的 Vector 型数据，则会作为 Any Vector 数据上传。
7. 如果上传的 Vector 中全为空值，且包含不同类型的空值，则将按照空值处理规则进行转换，如下表展示：

   | 空值组合情况 | DolphinDB 列字段类型 |
   | --- | --- |
   | 全部为 None | STRING |
   | np.nan 与 None 组合 | DOUBLE |
   | pd.NaT 与 None 组合 | NANOTIMESTAMP |
   | np.nan 与 pd.NaT 组合 | NANOTIMESTAMP |
   | None, np.nan 与 pd.NaT 组合 | NANOTIMESTAMP |
   | None, pd.NaT 或 np.nan 与非空值组合 | 非空值类型 |

* **注1**： 此处“两种及两种以上”特指 DolphinDB 类型系统中的类型，例如数据为 np.array([np.float64(12), 1.3]) ，则将被视为仅包含一种数据类型。
* **注2**： 目前版本的 DolphinDB Python API 并不支持 pd.array 的 Vector 型数据。
* **注3**： 在 list 或是 dtype 为 object 的 np.ndarray 对象中的空值类型，将全部被视为同一种空值，例如 None/np.nan/pd.NaT 等，但不包含 decimal.Decimal('NaN')。
* **注4**： 目前不支持直接上传 Array Vector 型数据，形如 np.array([[1], [2, 3]]) 的数据会作为 Any Vector 数据上传。
* **注5**： 上传 Decimal 类型的数据时
  + 若版本低于 3.0.1.0，则必须须确保 DECIMAL 类型列的所有数据具有相同的小数位数；可使用下述方式对齐小数位数：

```
>>> b = decimal.Decimal("1.23")
>>> b
Decimal('1.23')
>>> b = b.quantize(decimal.Decimal("0.000"))
>>> b
Decimal('1.230')
```

* 若版本大于等于 3.0.1.0，则无需确保 DECIMAL 类型列的所有数据具有相同的小数位数，系统会自动根据第一个非空 Decimal 数据来调整位数。
* **注6**：目前版本不支持 上传 bytes 类型 Vector 作为 BLOB 数据。

以下为 3 个常见的上传 Vector 型数据的例子：

**示例 1** 上传不包含空值的 BOOL Vector、INT Vector、DOUBLE Vector、STRING Vector、DATE Vector

相关代码示例：

```
>>> s.upload({'bool_v': np.array([True, False, False], dtype="bool")})
>>> s.upload({'int_v': np.array([1, 2, 4], dtype="int32")})
>>> s.upload({'double_v': [1.2, 2.456]})
>>> s.upload({'string_v': np.array(["abc", "123"], dtype="object")})
>>> s.upload({'date_v': np.array(["2012-01-02"], dtype="datetime64[D]")})
```

可使用 typestr 方法查看已上传变量的数据类型：

```
>>> s.run("typestr(bool_v)")
FAST BOOL VECTOR
>>> s.run("typestr(int_v)")
FAST INT VECTOR
>>> s.run("typestr(double_v)")
FAST DOUBLE VECTOR
>>> s.run("typestr(string_v)")
STRING VECTOR
>>> s.run("typestr(date_v)")
FAST DATE VECTOR
```

**示例 2** 上传包含空值的 BOOL Vector、INT Vector、DOUBLE Vector、STRING Vector、DATE Vector

相关代码示例：

```
>>> s.upload({'bool_v': [True, None, False]})
>>> s.upload({'int_v': np.array([None, np.int32(2), np.int32(12)], dtype="object")})
>>> s.upload({'double_v': np.array([1.1, np.nan, 3.456])})
>>> s.upload({'string_v': ["", "abc", "123"]})
>>> s.upload({'date_v': [pd.NaT, None, np.nan, np.datetime64("2012-01-03", "D")]})
```

可使用 typestr 方法查看上传变量的数据类型：

```
>>> s.run("typestr(bool_v)")
FAST BOOL VECTOR
>>> s.run("typestr(int_v)")
FAST INT VECTOR
>>> s.run("typestr(double_v)")
FAST DOUBLE VECTOR
>>> s.run("typestr(string_v)")
STRING VECTOR
>>> s.run("typestr(date_v)")
FAST DATE VECTOR
```

**示例 3** 上传 Any Vector

上传 Any Vector 有两种方式。一种是在构造 np.ndarray 时指定 `dtype=object`；另一种则是上传一个 list/tuple 对象。须注意，这两种方式都需要包含 **两种及两种以上** 类型的数据或者包含 Vector 型的数据。

相关代码示例：

```
>>> s.upload({'list_v': [1.2, "abc"])})
>>> s.upload({'array_v': np.array([1, 1.2], dtype="object"})
>>> s.upload({'list_av': [[1, 2], [3]]})
>>> s.upload({'array_av': np.array([[1], [2, 3]], dtype="object")})
```

使用 typestr 方法查看上传变量的数据类型：

```
>>> s.run("typestr(list_v)")
ANY VECTOR
>>> s.run("typestr(array_v)")
ANY VECTOR
>>> s.run("typestr(list_av)")
ANY VECTOR
>>> s.run("typestr(array_av)")
ANY VECTOR
```

### Pair

在使用 PROTOCOL\_DDB 协议时，DolphinDB Python API 暂不支持直接上传 Pair 形式的数据。

### Matrix

如果上传的 np.ndarray 对象中包含长度一致的 Vector 型数据，则将会作为 Matrix 形式的数据上传。但是，如果上传的对象不是 np.ndarray，却包含长度一致的 Vector 型数据，则将会作为 Any Vector 数据上传。

上传 Matrix 型数据的相关代码示例：

```
>>> s.upload({'int_m': np.array([[1, 2], [2, 3], [3, 4]])})
>>> s.run("typestr(int_m)")
FAST LONG MATRIX
>>> s.upload({'any_vec': [[1, 2], [2, 3], [3, 4]]})
>>> s.run("typestr(any_vec)")
ANY VECTOR
```

**注意**：上传二维 ndarray 时，如果数据只有一行，则会被识别为 Vector 型数据而非 Matrix。

### Set

上传 Set 类型的 Python 对象，数据将会转换为 DolphinDB 中的 Set 形式。在转换时 API 将会遍历 Set 中的所有元素，将各元素作为 Scalar 数据进行逐个转换，最后数据整体作为一个 Set 上传至 DolphinDB，转换后的数据类型以对应的 DolphinDB 数据类型为准。

上传 Set 型数据的相关代码示例：

```
>>> s.upload({'long_set': {1, 2}})
>>> s.run("typestr(long_set)")
LONG SET
>>> s.upload({'double_set': {1.2, np.double(5.5), pd.NaT}})
>>> s.run("typestr(double_set)")
DOUBLE SET
```

* **注1**： DolphinDB 的 Set 数据形式目前不支持元素有多种数据类型，也不支持 Vector 作为组成元素。
* **注2**：在转换时，若 Set 中包含空值，则空值将不被视为任何一种数据类型。此外，DolphinDB 也不支持构造全为空值的 Set。

### Dict

和 Set 类似，在转换 Dict 型数据时 API 会遍历所有元素，按照对应的数据形式逐个进行类型转换，最后数据整体作为一个 Dictionary 上传至 DolphinDB。

上传 Dict 型数据的相关代码示例：

```
>>> s.upload({'long_dict': {'a': None, 'b': 1}})
>>> s.run("typestr(long_dict)")
STRING->LONG DICTIONARY
>>> s.upload({'any_dict1': {'a': 1, 'b': [1.1, 2.4], 'c': np.array([1, "a"], dtype="object")}})
>>> s.run("typestr(any_dict1)")
STRING->ANY DICTIONARY
>>> s.upload({'any_dict2': {1: [[1], [2, 3]], 2: [[1.1, np.nan], [3.3]]}})
>>> s.run("typestr(any_dict2)")
STRING->ANY DICTIONARY
```

* **注1**： DolphinDB 不支持多种数据类型作为键，支持多种数据类型作为值。
* **注2**： 在 Dict 中转换时，Vector 型数据中如果包含 Vector 型元素，将作为 Any Vector 进行转换，而非 Array Vector。
* **注3**： Dict 中的空值在转换时不视为任何一种数据类型。DolphinDB 也不支持构造全为空值的 Dict。

### Table

Table 型数据在 Python 中对应的数据类型为 pd.DataFrame，在转换时，按列进行处理，每列作为 Vector 型数据进行转换。特别的，当 pd.DataFrame 的元素中出现 Vector 型数据时，将作为 Array Vector 进行处理，且不支持 Any Vector 作为列类型，这点与 Vector 型数据的转换逻辑有较大不同。

当 Table 型数据中包含空值时，处理逻辑与 Vector 型数据保持一致。同样的，也不支持直接上传 BLOB、INT128 等类型，如需上传，需指定 \_\_DolphinDB\_Type\_\_ 进行强制类型转换才能上传，具体操作参考：[强制类型转换](ForceTypeCasting.md)。

**注意**：pd.DataFrame 中仅有一种时间类型 datetime64[ns]，对应 np.datetime64[ns]，因此，如果直接上传时间类型数据，在 DolphinDB 服务器端仅能得到 NANOTIMESTAMP 类型的数据。

**示例 1**

```
>>> df1 = pd.DataFrame({
...     'int_v': [1, 2, 3],
...     'long_v': np.array([None, 3, np.int64(3)], dtype="object"),
...     'float_v': np.array([np.nan, 1.2, 3.3], dtype="float32")
... })
>>> s.upload({'df1': df1})
>>> s.run("schema(df1)")['colDefs']
      name typeString  typeInt  extra comment
0    int_v       LONG        5    NaN
1   long_v       LONG        5    NaN
2  float_v      FLOAT       15    NaN
```

当上传的数据 `dtype=object` 时，会逐个判断数据类型，空值（None、pd.NaT、np.nan）不视为任何一种数据类型，并根据第一个非空值的数据类型作为该列的数据类型。

本例中，int\_v 列没有空值，但是在 Python pandas 中，Python 的 int 会被转换为 int64，对应 DolphinDB 的 LONG；long\_v 列 `dtype=object`，且第一个非空值为 Python int 3，对应 DolphinDB LONG，因此该列作为 LONG 进行类型转换； float\_v 列 dtype=float，因此无论是否包含空值，都会作为 FLOAT 处理。

**注意：** numpy 和 pandas 中，dtype=bool/int8/int16/int32/int64 时，不能包含空值，因此，如果需要上传包含空值的列，则需要在构造 pd.DataFrame 时，指定该列类型为 object。

**示例 2**

```
>>> df2 = pd.DataFrame({
...     'day_v': np.array(["2012-01-02", "2022-02-05"], dtype="datetime64[D]"),
...     'month_v': np.array([np.datetime64("2012-01", "M"), None], dtype="datetime64[M]"),
... })
>>> s.upload({'df2': df2})
>>> s.run("schema(df2)")['colDefs']
      name     typeString  typeInt  extra comment
0    day_v  NANOTIMESTAMP       14    NaN
1  month_v  NANOTIMESTAMP       14    NaN
```

对于时间类型，pandas 中仅有一种时间类型 datetime64[ns]，因此无法直接上传 DATE、MONTH等类型，需要指定 \_\_DolphinDB\_Type\_\_ 进行强制类型转换才能上传，具体操作参考：[强制类型转换](ForceTypeCasting.md)。

```
>>> import dolphindb.settings as keys
>>> df2.__DolphinDB_Type__ = {
...     "day_v": keys.DT_DATE,
...     "month_v": keys.DT_MONTH,
... }
...
>>> s.upload({'df2': df2})
>>> s.run("schema(df2)")['colDefs']
      name typeString  typeInt  extra comment
0    day_v       DATE        6    NaN
1  month_v      MONTH        7    NaN
```

**示例 3**

```
>>> df3 = pd.DataFrame({
...     'long_av': [[1, None], [3]],
...     'double_av': np.array([[1.1], [np.nan, 3.3]], dtype="object")
... })
>>> s.upload({'df3': df3})
>>> s.run("schema(df3)")['colDefs']
        name typeString  typeInt  extra comment
0    long_av     LONG[]       69    NaN
1  double_av   DOUBLE[]       80    NaN
```

如上例所示，当上传的 pd.DataFrame 中某一列包含 Vector 型数据时，该列将作为 Array Vector 进行类型转换，而非 Any Vector。

**示例 4：**

Python API 自 3.0.0.0 版本起，支持上传 pandas 扩展类型：Boolean/Int8/Int16/Int32/Int64/Float32/Float64/String。以下为使用示例：

```
>>> import pandas as pd
>>> df4 = pd.DataFrame({
...     'bool': pd.Series([True, False, None], dtype=pd.BooleanDtype()),
...     'int64': pd.Series([1, -100, None], dtype=pd.Int64Dtype()),
...     'float64': pd.Series([1.1, -0.23, None], dtype=pd.Float64Dtype()),
...     'string': pd.Series(["abc", "def", None], dtype=pd.StringDtype()),
... })
...
>>> df4.dtypes
bool              boolean
int64               Int64
float64           Float64
string     string[python]
dtype: object
>>> s.upload({'df4': df4})
>>> s.run("schema(df4)")['colDefs']
      name typeString  typeInt  extra comment
0     bool       BOOL        1    NaN
1    int64       LONG        5    NaN
2  float64     DOUBLE       16    NaN
3   string     STRING       18    NaN

// output

      name typeString  typeInt  extra comment
0     bool       BOOL        1    NaN
1    int64       LONG        5    NaN
2  float64     DOUBLE       16    NaN
3   string     STRING       18    NaN

```

以下为 pandas ExtensionDtype 和 DolphinDB 的数据类型对照表。其中关于强制类型转换的更多说明可参阅[强制类型转换](ForceTypeCasting.md)。

| **pandas ExtensionDtype** | **DolphinDB 类型** | **说明** |
| --- | --- | --- |
| BooleanDtype | BOOL |  |
| Int8Dtype | CHAR |  |
| Int16Dtype | SHORT |  |
| Int32Dtype | INT |  |
| Int64Dtype | LONG |  |
| Float32Dtype | FLOAT |  |
| Float64Dtype | DOUBLE |  |
| StringDtype | SYMBOL | 需强制类型转换 |
| StringDtype | STRING |  |
| StringDtype | UUID | 需强制类型转换 |
| StringDtype | IPADDR | 需强制类型转换 |
| StringDtype | INT128 | 需强制类型转换 |
| StringDtype | BLOB | 需强制类型转换 |

**示例 5：**

Python API 自 1.30.22.4 版本起，支持上传 Pandas2.0 PyArrow 作为数据后端的 DataFrame。以下为使用示例：

```
>>> import pandas as pd # pandas version >= 2.0.0
>>> df5 = pd.DataFrame({
...     'int64': pd.Series([1, 2, None, 4], dtype="int64[pyarrow]"),
...     'float64': pd.Series([1.1, 2.2, None, 4.4], dtype="float64[pyarrow]"),
...     'string': pd.Series(["aa", "bb", None, "cc"], dtype="string[pyarrow]"),
... })
...
>>> df5.dtypes
int64       int64[pyarrow]
float64    double[pyarrow]
string     string[pyarrow]
dtype: object
>>> s.upload({'df5': df5})
>>> s.run("schema(df5)")['colDefs']
      name typeString  typeInt  extra comment
0    int64       LONG        5    NaN
1  float64     DOUBLE       16    NaN
2   string     STRING       18    NaN
```

以下为 DataFrame/Series、PyArrow 和 DolphinDB 的数据类型对照表。其中关于强制类型转换的更多说明可参阅[强制类型转换](ForceTypeCasting.md)。

| **DataFrame/Series 类型** | **PyArrow 类型** | **DolphinDB 类型** | **说明** |
| --- | --- | --- | --- |
| bool[pyarrow] | pa.bool\_() | BOOL |  |
| int8[pyarrow] | pa.int8() | CHAR |  |
| int16[pyarrow] | pa.int16() | SHORT |  |
| int32[pyarrow] | pa.int32() | INT |  |
| int64[pyarrow] | pa.int64() | LONG |  |
| date32[day][pyarrow] | pa.date32() | DATE |  |
| date32[day][pyarrow] | pa.date32() | MONTH | 需要强制类型转换 |
| time32[ms][pyarrow] | pa.time32(“ms“) | TIME |  |
| time32[s][pyarrow] | pa.time32(“s“) | MINUTE | 需要强制类型转换 |
| time32[s][pyarrow] | pa.time32(“s“) | SECOND |  |
| timestamp[s][pyarrow] | pa.timestamp(“s“) | DATETIME |  |
| timestamp[ms][pyarrow] | pa.timestamp(“ms“) | TIMESTAMP |  |
| time64[ns][pyarrow] | pa.time64(“ns“) | NANOTIME |  |
| timestamp[ns][pyarrow] | pa.timestamp(“ns“) | NANOTIMESTAMP |  |
| float[pyarrow] | pa.float32() | FLOAT |  |
| double[pyarrow] | pa.float64() | DOUBLE |  |
| dictionary<values=string, indices=int32, ordered=0>[pyarrow] | pa.dictionary(pa.int32(), pa.utf8()) | SYMBOL |  |
| string[pyarrow] | pa.utf8() | STRING |  |
| fixed\_size\_binary[16][pyarrow] | pa.binary(16) | UUID | 需要强制类型转换 |
| timestamp[s][pyarrow] | pa.timestamp(“s“) | DATEHOUR | 需要强制类型转换 |
| string[pyarrow] | pa.utf8() | IPADDR | 需要强制类型转换 |
| fixed\_size\_binary[16][pyarrow] | pa.binary(16) | INT128 |  |
| large\_binary[pyarrow] | pa.large\_binary() | BLOB |  |
| decimal128(38, S)[pyarrow] | pa.decimal128(38, S) | DECIMAL32(S) | 需要强制类型转换 |
| decimal128(38, S)[pyarrow] | pa.decimal128(38, S) | DECIMAL64(S) | 需要强制类型转换 |
| decimal128(38, S)[pyarrow] | pa.decimal128(38, S) | DECIMAL128(S) |  |
| list<item: T>[pyarrow]例：list<item: int32>[pyarrow] | pa.list\_(T)例：pa.list\_(pa.int32()) | ARRAYVECTOR例：INT ARRAYVECTOR | list\_ 嵌套对应 arrayvector |

注：Python API 自 1.30.22.6 版本起支持数据类型 Decimal128。1.30.22.5 及之前的版本上传 pyarrow.decimal128 默认作为 DECIMAL64 上传，1.30.22.6 版本起将默认作为 DECIMAL128 上传，可以通过指定类型的方式上传为 DECIMAL32/64。

如上例所示，当上传的 pd.DataFrame 中某一列包含 Vector 型数据时，该列将作为 Array Vector 进行类型转换，而非 Any Vector。

## 反序列化 DolphinDB -> Python(设置 pickleTableToList=False)

以下示例以 run 函数为例，介绍不同 DolphinDB 数据类型和数值通过该方式下载时对应的 Python 对象。

**注意**： 由于 numpy 和 pandas 具有 dtype，故下文中，Python 类型中的 np.datetime64[D]，表示该对象的类型为 numpy.datetime64，且 dtype=datetime64[D]。

### Scalar

| DolphinDB 类型 | DolphinDB 数据 | Python 类型 | Python 数据 |
| --- | --- | --- | --- |
| VOID | NULL | NoneType | None |
| INT | int(NULL) | NoneType | None |
| STRING | string(NULL) | NoneType | None |
| BOOL | true | bool | True |
| CHAR | 'a' | int | 97 |
| SHORT | 224h | int | 224 |
| INT | 16 | int | 16 |
| LONG | 3000l | int | 3000 |
| DATE | 2013.06.13 | np.datetime64[D] | 2013-06-13 |
| MONTH | 2012.06M | np.datetime64[M] | 2012-06 |
| TIME | 13:30:10.008 | np.datetime64[ms] | 1970-01-01T13:30:10.008 |
| MINUTE | 13:30m | np.datetime64[m] | 1970-01-01T13:30 |
| SECOND | 13:30:10 | np.datetime64[s] | 1970-01-01T13:30:10 |
| DATETIME | 2012.06.13T13:30:10 | np.datetime64[s] | 2012-06-13T13:30:10 |
| TIMESTAMP | 2012.06.13T13:30:10.008 | np.datetime64[ms] | 2012-06-13T13:30:10.008 |
| NANOTIME | 13:30:10.008007006 | np.datetime64[ns] | 1970-01-01T13:30:10.008007006 |
| NANOTIMESTAMP | 2012.06.13T13:30:10.008007006 | np.datetime64[ns] | 2012-06-13T13:30:10.008007006 |
| FLOAT | 2.1f | float | 2.0999999046325684 |
| DOUBLE | 2.1 | float | 2.1 |
| SYMBOL | --- | --- | --- |
| STRING | "Hello" | str | "Hello" |
| UUID | uuid("5d212a78-cc48-e3b1-4235-b4d91473ee87") | str | "5d212a78-cc48-e3b1-4235-b4d91473ee87" |
| DATEHOUR | datehour(2012.06.13T13:30:10) | np.datetime64[h] | 2012-06-13T13 |
| IPADDR | ipaddr("192.168.1.13") | str | "192.168.1.13" |
| INT128 | int128("e1671797c52e15f763380b45e841ec32") | str | "e1671797c52e15f763380b45e841ec32" |
| BLOB | blob("xxxyyyzzz") | str | "xxxyyyzzz" |
| DECIMAL32 | decimal32(1.111, 4) | decimal.Decimal | 1.1110 |
| DECIMAL64 | decimal64(1.123456789, 5) | decimal.Decimal | 1.12345 |

* **注1：** DolphinDB 中的空值不仅有 VOID 类型，还有 INT、STRING 等类型的空值，这些空值 Scalar 都对应 Python API 的空值 None。
* **注2：** DolphinDB 中不存在 Scalar 形式的 SYMBOL 数据。

### Vector

DolphinDB 中的 Vector 数据一般对应 Python 中的 numpy.ndarray。特别的，Any Vector 对应 Python 中的 list （1.30.17.1及之前版本的 API 对应 numpy.ndarray）。

下表给出各类型 Vector 所对应 numpy.ndarray 的 dtype：

| DolphinDB类型 | np.dtype |
| --- | --- |
| BOOL（不含空值） | bool |
| CHAR（不含空值） | int8 |
| SHORT（不含空值） | int16 |
| INT（不含空值） | int32 |
| LONG（不含空值） | int64 |
| DATE | datetime64[D] |
| MONTH | datetime64[M] |
| TIME、TIMESTAMP | datetime64[ms] |
| MINUTE | datetime64[m] |
| SECOND、DATETIME | datetime64[s] |
| NANOTIME、NANOTIMESTAMP | datetime64[ns] |
| FLOAT | float32 |
| DOUBLE、CHAR（含空值）、SHORT（含空值）、INT（含空值）、LONG（含空值） | float64 |
| DATEHOUR | datetime64[h] |
| BOOL（含空值）、SYMBOL、STRING、UUID、IPADDR、INT128、BLOB、DECIMAL32、DECIMAL64、Array Vector | object |

* **注1** ：numpy.ndarray 中没有整型的空值，因此如果 DolphinDB 整型的 Vector 中包含空值，则会强制转换为 float64，空值变为 np.nan。
* **注2** ：BOOL Vector 中如果包含空值，则会转换为 `dtype=object` 的 np.ndarray，而非 `dtype=bool`。
* **注3** ： DolphinDB Array Vector 下载到 Python 所对应的 dtype 为 object，其中每一项元素都是原始 ArrayVector 的一个元素转换而成的 np.ndarray。
* **注4** ： 若使用 1.30.17.2 及之后版本的 Python API，则 DolphinDB Any Vector 下载到 Python 对应的数据类型为 list；若使用 1.30.17.2 及之前版本的 Python API，则 DolphinDB Any Vector 下载到 Python 对应的数据类型为 np.ndarray。
* **注5** ： 自 1.30.22.3 版本起，API 支持下载类型为 Decimal32 Array Vector 和 Decimal64 Array Vector 的数据。

下载 Vector 型数据的相关代码示例：

```
>>> re = s.run("[true, false]")
>>> re
[ True False]
>>> type(re)
<class 'numpy.ndarray'>
>>> re.dtype
bool

>>> re = s.run("[true, None]")
>>> re
[True None]
>>> re.dtype
object
```

上例中，首先下载一个不含空值的 BOOL Vector，可以看到对应的 Python 对象为 np.ndarray，且 `dtype=bool`；如果下载的 BOOL Vector 中包含空值，则对应的 dtype 变为 object。和 BOOL 不同，如果下载的整型向量中包含空值，则 `dtype=float64`。

```
>>> re = s.run("[1, 2, 3, NULL]")
>>> re
[ 1.  2.  3. nan]
>>> re.dtype
float64
```

如果下载的 Vector 为 Array Vector，则 API 会遍历每个元素，将所有元素逐个按照 Vector 的转换规则进行转换。示例中下载的 INT Array Vector 某一元素中包含空值，因此，其他不含空值的元素对应 dtype=int32，包含空值的元素则对应 dtype=float64。

```
>>> s.run("arrayVector(2 3 4, [1, 2, 3, NULL])")
[array([1, 2], dtype=int32) array([3], dtype=int32) array([nan])]

>>> re = s.run('''(1, 2, [12, "aaa"])''')
>>> re
[1, 2, [12, 'aaa']]
>>> type(re)
<class 'list'>
>>> type(re[2])
<class 'list'>
```

如果下载的 Vector 为 Any Vector，则 API 会遍历每个元素，按照每个元素的转换规则进行转换。示例中的 Any Vector 嵌套了另一个 Any Vector，两者都被转换为 list 类型。如果 Python API 版本等于或低于 1.30.17.1，则 Any Vector 数据将会被转换为 np.ndarray，且 dtype=object。

### Pair

DolphinDB 中的 Pair 类型对应 Python 中的 list，其中每一个元素都将按照 Scalar 的规则进行转换。

上传 Pair 型数据的相关代码示例：

```
>>> s.run("100:0")
[100, 0]
```

### Matrix

DolphinDB 中的 Matrix 类型对应 Python 中的 np.ndarray。不同数据类型与 np.dtype 对应关系如下表所示：

| DolphinDB类型 | np.dtype |
| --- | --- |
| BOOL（不含空值） | bool |
| CHAR（不含空值） | int8 |
| SHORT（不含空值） | int16 |
| INT（不含空值） | int32 |
| LONG（不含空值） | int64 |
| DATE | datetime64[D] |
| MONTH | datetime64[M] |
| TIME、TIMESTAMP | datetime64[ms] |
| MINUTE | datetime64[m] |
| SECOND、DATETIME | datetime64[s] |
| NANOTIME、NANOTIMESTAMP | datetime64[ns] |
| FLOAT | float32 |
| DOUBLE、CHAR（含空值）、SHORT（含空值）、INT（含空值）、LONG（含空值） | float64 |
| DATEHOUR | datetime64[h] |
| BOOL（含空值） | object |

下载 Matrix 型数据的相关代码示例：

```
>>> s.run("""
...     mtx = 1..12$4:3;
...     mtx.rename!(1 2 3 4, `c1`c2`c3);
...     mtx
... """)
[array([[ 1,  5,  9],
       [ 2,  6, 10],
       [ 3,  7, 11],
       [ 4,  8, 12]], dtype=int32), array([1, 2, 3, 4], dtype=int32), array(['c1', 'c2', 'c3'], dtype=object)]
```

与上传数据时不同，虽然 Matrix 直接对应二维 np.ndarray，但是 API 在下载 Matrix 型数据时会包含其行名和列名的信息。如果 Matrix 数据中不包含行名（或列名），则使用 None 代替。

* **注1：** 时间类型的 Matrix 在 PROTOCOL\_DDB 协议中的对应规则与 Vector 类似，但在 PROTOCOL\_PICKLE 协议中则全部对应 datetime64[ns]，请参考 [Pickle](PROTOCOL_PICKLE.md)。

### Set

DolphinDB 中的 Set 数据形式对应 Python set 类型，在转换时，API 会将 Set 中的每个元素作为 Scalar 进行转换。有关具体每种数据类型对应的 Python 类型，请参考本节 Scalar 部分的转换规则。

**注意：** 目前仅支持 CHAR、SHORT、INT、LONG、FLOAT、DOUBLE、STRING、SYMBOL Set 转换为 Python 对象。

下载 Set 型数据的相关代码示例：

```
>>> re = s.run("set(1..5)")
>>> re
{1, 2, 3, 4, 5}
>>> type(re)
<class 'set'>
```

### Dict

DolphinDB 中的 Dict 数据形式对应 Python 中的 dict 类型。在转换时，API 会遍历 Dict 中的所有键值对，并将键作为 Scalar 进行转换；同时根据值本身的数据形式、数据类型进行转换，转换规则请参考本文中对应数据形式的规则。

下载 Dict 型数据的相关代码示例：

```
>>> re = s.run('''{"a": 123, "b": [1.1, 2.2]}''')
>>> re
{'b': array([1.1, 2.2]), 'a': 123}
>>> type(re)
<class 'dict'>
```

### Table

DolphinDB 中的 Table 数据形式对应 Python 中的 pandas.DataFrame 类型。在转换时，API 会将 Table 型数据的每一列作为 Vector 类型进行处理。

特别的，不同于 Vector 的处理，当 Table 型数据为时间类型时，Python pandas 仅支持一种时间类型 datetime64[ns]，因此下载的时间类型都会转换为 datetime64[ns]。

**注意：** 目前 API 仅支持 Array Vector 列的下载，不支持 Any Vector 列的下载。

## 反序列化 DolphinDB -> Python(设置 pickleTableToList=True)

开启附加参数 pickleTableToList 后，如果执行脚本的返回值数据形式为 Table，则对应的 Python 对象为 list 而非 pd.DataFrame。其中，list 中的每一元素（np.ndarray）都表示 Table 中的一列。

PROTOCOL\_DDB 协议的附加参数仅在 API 端做处理，不会作为 flag 的一部分发送至 DolphinDB。API 收到数据后，不会再将数据拼接为 pd.DataFrame，而是将每一列放入 list 中。

### Table

和 Vector 型数据的转换流程不同，每一列在转换时仍旧视为是 Table 中的一列，而非单独的 Vector，因此时间类型会被转换为 datetime64[ns]。

* **注1**： 如果下载 Table 型数据的数据列为 Array Vector 列，须确保每个元素的长度一致，其对应数据类型为二维 np.ndarray。

下载 Table 型数据的相关代码示例：

```
>>> re = s.run("table([1, NULL] as a, [2012.01.02, NULL] as b)", pickleTableToList=True)
>>> re
[array([ 1., nan]), array(['2012-01-02T00:00:00.000000000',                           'NaT'],
      dtype='datetime64[ns]')]
>>> type(re)
<class 'list'>
>>> re[0].dtype
float64
>>> re[1].dtype
datetime64[ns]

>>> s.run("table(arrayVector(1 2 3, [1, 2, 3]) as a)", pickleTableToList=True)
[array([[1],
       [2],
       [3]], dtype=int32)]
```

上例中，指定附加参数 pickleTableToList 后下载的 Table 数据，转换为每个元素都是 np.ndarray 的 list。如果下载的 Table 中整型数据列中包含空值，则对应 dtype=float64；如果下载时间类型列，则全部对应 datetime64[ns]；如果下载 Array Vector 数据列，则需要其中的每个元素都长度相等。

