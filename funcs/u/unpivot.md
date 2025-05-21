# unpivot

## 语法

`unpivot(obj, keyColNames, valueColNames, [func])`

## 参数

**obj** 是一个表。

**keyColNames** 是表示列名的标量或向量，用于指定要在输出表中保留的列。

**valueColNames** 是一个列名向量。*valueColNames* 中的数据将转换成一列。 请注意
*valueColNames* 各列的数据类型应一致。

**func** 是一个函数。如果指定了 *func* 函数，该函数将会应用到 *valueColNames* 上，再将其合并。

## 详情

把多列的数据转换成一列。

返回一个表，列的顺序依次为 *keyColNames* 指定的各列，valueType 列和 value
列。其中，若未指定 *func* 参数，则 valueType 列存储 *valueColNames* 中的列名，否则 ，valueType 列存储
*func* 应用于 *valueColNames* 中各列的结果；value 列存储 *valueColNames*
中各列的值。

## 例子

```
t=table(1..3 as id, 2010.01.01 + 1..3 as time, 4..6 as col1, 7..9 as col2, 10..12 as col3, `aaa`bbb`ccc as col4, `ddd`eee`fff as col5, 'a' 'b' 'c' as col6);
t;
```

| id | time | col1 | col2 | col3 | col4 | col5 | col6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2010.01.02 | 4 | 7 | 10 | aaa | ddd | 'a' |
| 2 | 2010.01.03 | 5 | 8 | 11 | bbb | eee | 'b' |
| 3 | 2010.01.04 | 6 | 9 | 12 | ccc | fff | 'c' |

保留表 t 中的 id 列，将 col1 列和 col2 列转换为一列：

```
t.unpivot(keyColNames=`id, valueColNames=`col1`col2);
```

| id | valueType | value |
| --- | --- | --- |
| 1 | col1 | 4 |
| 2 | col1 | 5 |
| 3 | col1 | 6 |
| 1 | col2 | 7 |
| 2 | col2 | 8 |
| 3 | col2 | 9 |

保留表 t 中的 id 列，将 col1 列和 col2 列转换为一列，且将自定义函数应用于 col1 列和 col2 列：

```
f = def(x): x.split("col")[1];
t.unpivot(keyColNames=`id, valueColNames=`col1`col2, func=f);
```

| id | valueType | value |
| --- | --- | --- |
| 1 | 1 | 4 |
| 2 | 1 | 5 |
| 3 | 1 | 6 |
| 1 | 2 | 7 |
| 2 | 2 | 8 |
| 3 | 2 | 9 |

不保留其它列，仅仅将 col1 列和 col2 列转换为一列：

```
t.unpivot(, valueColNames=`col1`col2);
```

| valueType | value |
| --- | --- |
| col1 | 4 |
| col1 | 5 |
| col1 | 6 |
| col2 | 7 |
| col2 | 8 |
| col2 | 9 |

保留表 t 中的 id 列，将 col1 列、col2 列 和 col3 列转换为一列，且将自定义函数应用于 col1 列、col2 列和 col3 列：

```
f = def(x): x.regexReplace("col", "var")
t.unpivot(keyColNames=`id, valueColNames=`col1`col2`col3, func=f);
```

| id | valueType | value |
| --- | --- | --- |
| 1 | var1 | 4 |
| 2 | var1 | 5 |
| 3 | var1 | 6 |
| 1 | var2 | 7 |
| 2 | var2 | 8 |
| 3 | var2 | 9 |
| 1 | var3 | 10 |
| 2 | var3 | 11 |
| 3 | var3 | 12 |

```
t.unpivot(keyColNames=`time, valueColNames=`col4`col5)
```

| time | valueType | value |
| --- | --- | --- |
| 2010.01.02 | col4 | aaa |
| 2010.01.03 | col4 | bbb |
| 2010.01.04 | col4 | ccc |
| 2010.01.02 | col5 | ddd |
| 2010.01.03 | col5 | eee |
| 2010.01.04 | col5 | fff |

```
t = table(1..3 as id, 2010.01.01 + 1..3 as time, 8.1 9.2 11.3 as bid1, 12.4 11.1 10.5 as bid2, 10.1 10.2 10.3 as bid3, 10.1 10.2 10.3 as bid4, 10.1 11.2 9.3 as bid5, 7.7 8.2 10.5 as ask1, 11.4 10.1 9.5 as ask2, 9.6 9.2 11.3 as ask3, 12.1 7.2 8.3 as ask4, 10.1 12.5 8.9 as ask5);
t;
//保留 id 和 time 列，将 bid1~bid5 列转换到一个列
t1 = t.unpivot(`id`time, `bid1`bid2`bid3`bid4`bid5);
//不保留其它列，仅仅将 ask1~ask5 列转换到一个列
t2 = t.unpivot(, `ask1`ask2`ask3`ask4`ask5);
//分别将 t1 和 t2 的 valueType 和 value 列重命名后进行合并
re = rename!(t1, `valueType`value, `bid_type`bid_value) join rename!(t2, `valueType`value, `ask_type`ask_value)
re;
```

| id | time | bid\_type | bid\_value | ask\_type | ask\_value |
| --- | --- | --- | --- | --- | --- |
| 1 | 2010.01.02 | bid1 | 8.1 | ask1 | 8.1 |
| 2 | 2010.01.03 | bid1 | 9.2 | ask1 | 9.2 |
| 3 | 2010.01.04 | bid1 | 11.3 | ask1 | 11.3 |
| 1 | 2010.01.02 | bid2 | 12.4 | ask2 | 12.4 |
| 2 | 2010.01.03 | bid2 | 11.1 | ask2 | 11.1 |
| 3 | 2010.01.04 | bid2 | 10.5 | ask2 | 10.5 |
| 1 | 2010.01.02 | bid3 | 10.1 | ask3 | 10.1 |
| 2 | 2010.01.03 | bid3 | 10.2 | ask3 | 10.2 |
| 3 | 2010.01.04 | bid3 | 10.3 | ask3 | 10.3 |
| 1 | 2010.01.02 | bid4 | 10.1 | ask4 | 10.1 |
| 2 | 2010.01.03 | bid4 | 10.2 | ask4 | 10.2 |
| 3 | 2010.01.04 | bid4 | 10.3 | ask4 | 10.3 |
| 1 | 2010.01.02 | bid5 | 10.1 | ask5 | 10.1 |
| 2 | 2010.01.03 | bid5 | 11.2 | ask5 | 11.2 |
| 3 | 2010.01.04 | bid5 | 9.3 | ask5 | 9.3 |

