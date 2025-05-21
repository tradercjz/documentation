# select

使用select语句访问表中数据。select语句总是返回一个表。

自 3.00.0 版本起，支持 catalog 结构。

## 用法

### 用法 1：读取表中的列数据。

```
select column1, column2, ... from t
select * from t //选取所有列
```

column1, column2, ... 为表 t 中的列字段名称。

### 用法 2：生成新列。

```
select expression [as colName] from t
```

expression 可以是包含表 t 中列字段的计算表达式，也可以是一个常量。若不指定 colName，当 expression
是表达式时，将表达式和其作用的列名组合生成新列名；当 expression 是常量时，将使用常量值作为新列名。

注意：当只 select 一个常量时，返回一个单行单列的表。

### 用法3：生成一个新列，其元素全为 NULL。

```
select NULL [as colName] from t
```

通过用法3生成的新列的类型为 VOID（无类型），不支持对该列进行计算操作，亦不支持追加、插入数据到 VOID 类型列和修改 VOID
类型列。其主要作用是占位。将包含空值列的表追加到其它表中（使用 append!, insert into, tableInsert
方法），则空值列的类型会自动转换为被追加列的类型，以方便后续操作。

注意：当只 select 一个 NULL 时，返回一个单行单列的空表。

以上3种用法可以结合使用，比如 `select *, expression as newCol1, NULL as newCol2 from
t`。

在 SQL 查询中，select 查询返回的结果，若为：

* 单列表：将作为向量，可以与 in 关键字结合使用；
* 单行单列的表：将作为标量，可以和操作符，如：gt、ge、lt、le、eq、ne 等结合使用;

### 用法4：通过字段序列，选择具有”相同前缀”+“连续数字“的多列。例如：col1…col10 或 col10…col1。

```
select col1...colN [as name1 ... nameN] from t
```

上述语法中的 as
关键字可选，用于为列指定别名。该语法通常用于查询包含许多列且这些列具有相似属性的多列数据。使用时需要注意以下几点：查询表中的字段名必须满足以下正则表达式的要求：

* [a-zA-Z\\_]{1,}[0-9]+：以字母（大小写均可）或下划线开头，后面可以跟着任意数量的字母、下划线，最后必须至少包含一个数字。
* 字段序列中的数字必须连续，且满足最大和最小数字之间的差必须小于等于32768。可对数字进行格式化，例如固定位数：0001,0002,…,0010,0011,…,0100,0101,…。
* 数字前的文本作为前缀。前缀必须相同。

## 例子

创建表t1，含有列timestamp, qty, price和sym.

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t1 = table(timestamp, sym, qty, price);
t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

```
select * from t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

select语句中被选中的对象不仅限于表中的列，可以是变量或函数。系统会检查选中的列是否是表中的列，如果是，那么这个列将会被当作表列处理；否则将会被当作变量列或者函数处理。

```
recordNum=1..9;
select 1..9 as recordNum, sym from t1;
```

| recordNum | sym |
| --- | --- |
| 1 | C |
| 2 | MS |
| 3 | MS |
| 4 | MS |
| 5 | IBM |
| 6 | IBM |
| 7 | C |
| 8 | C |
| 9 | C |

```
// 使用一个标量值来表示含有相同值的列
select 3 as portfolio, sym from t1;
```

| portfolio | sym |
| --- | --- |
| 3 | C |
| 3 | MS |
| 3 | MS |
| 3 | MS |
| 3 | IBM |
| 3 | IBM |
| 3 | C |
| 3 | C |
| 3 | C |

在select语句中使用函数。

```
def f(a):a+100;
select f(qty) as newQty, sym from t1;
```

| newQty | sym |
| --- | --- |
| 2300 | C |
| 2000 | MS |
| 2200 | MS |
| 3300 | MS |
| 6900 | IBM |
| 5500 | IBM |
| 1400 | C |
| 2600 | C |
| 8900 | C |

```

select last price from t1 group by sym;
```

| sym | last\_price |
| --- | --- |
| C | 51.29 |
| MS | 30.02 |
| IBM | 175.23 |

生成一列常量列：

```
t = table(1..5 as id, `a`a`a`b`b as val);
select *, 1 as cst from t
```

| id | val | cst |
| --- | --- | --- |
| 1 | a | 1 |
| 2 | a | 1 |
| 3 | a | 1 |
| 4 | b | 1 |
| 5 | b | 1 |

```
select *, 1 from t
```

| id | val | 1 |
| --- | --- | --- |
| 1 | a | 1 |
| 2 | a | 1 |
| 3 | a | 1 |
| 4 | b | 1 |
| 5 | b | 1 |

单列的查询结果和 in 关键字结合使用：

```
t = table(`APPL`IBM`AMZN`IBM`APPL`AMZN as sym, 10.1 11.2 11.3 12 10.6 10.8 as val)
t;
```

| sym | val |
| --- | --- |
| APPL | 10.1 |
| IBM | 11.2 |
| AMZN | 11.3 |
| IBM | 12 |
| APPL | 10.6 |
| AMZN | 10.8 |

```
stk = table(1 2 3 as id, `AAPL`IBM`FB as stock);
select count(*) from t where sym in select stock from stk;
// output: 2
```

下例生成一个包含空值列的表，且将该表追加到 t2 中

```
t1 = table(rand(10,3) as x)
tmp=select *, NULL from t1
typestr(tmp[`NULL])
// output: VOID VECTOR
```

将表 tmp 追加到 t2 中

```
t2 = table(1..6 as x1, 1..6 as y1)
t2.append!(tmp)
t2
```

| x1 | y1 |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 3 |  |
| 4 |  |
| 6 |  |

字段序列支持直接用在 SQL 语句中作为查询的字段或者别名：

通过字段序列查询多列并重命名：

```
t= table(`a1`a2 as sym, 2.5 1.5 as price1, 3.0 2.0 as price2, 3.5 2.5 as price3, 4.0 3.0 as price4, 4.5 3.5 as price5,
110 200 as qty1, 120 210 as qty2, 130 230 as qty3, 140 240 as qty4, 150 260 as qty5)

select price1...price5 as p1...p5 from t
```

| p1 | p2 | p3 | p4 | p5 |
| --- | --- | --- | --- | --- |
| 2.5 | 3 | 3.5 | 4 | 4.5 |
| 1.5 | 2 | 2.5 | 3 | 3.5 |

对于具有多个相似功能的列，通常列名也类似，此时可通过 fixedLengthArrayVector
结合字段序列，简化生成数组向量：

```
select fixedLengthArrayVector(price1...price5) as priceArray, fixedLengthArrayVector(qty1...qty5) as qtyArray from t
```

| priceArray | qtyArray |
| --- | --- |
| [2.5000,3.0000,3.5000,4.0000,4.5000] | [110,120,130,140,150] |
| [1.5000,2.0000,2.5000,3.0000,3.5000] | [200,210,230,240,260] |

多个字段序列间进行计算，规则同向量间计算。如下例，将分别计算 price1\*qty1 ,…, price5\*qty5：

```
select (price1...price5) * (qty1...qty5)  as amount1...amount5 from t
```

| amount1 | amount2 | amount3 | amount4 | amount5 |
| --- | --- | --- | --- | --- |
| 275 | 360 | 455 | 560 | 675 |
| 300 | 420 | 575 | 720 | 910 |

