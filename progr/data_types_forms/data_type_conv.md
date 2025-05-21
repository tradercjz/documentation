# 数据类型转换

数据类型转换可以通过数据类型转换函数或函数 [cast($)](../../funcs/c/cast.html) 来实现。

DolphinDB支持的数据类型转换函数包括 [string](../../funcs/s/string.html), [bool](../../funcs/b/bool.html), [char](../../funcs/c/char.html), [short](../../funcs/s/short.html), [int](../../funcs/i/int.html), [long](../../funcs/l/long.html), [double](../../funcs/d/double.html), [date](../../funcs/d/date.html), [month](../../funcs/m/month.html), [time](../../funcs/t/time.html), [second](../../funcs/s/second.html), [minute](../../funcs/m/minute.html), [datetime](../../funcs/d/datetime.html), [timestamp](../../funcs/t/timestamp.html), [symbol](../../funcs/s/symbol.html), [nanotime](../../funcs/n/nanotime.html), [nanotimestamp](../../funcs/n/nanotimestamp.html), [datehour](../../funcs/d/datehour.html), [uuid](../../funcs/u/uuid.html), [ipaddr](../../funcs/i/ipaddr.html), [int128](../../funcs/i/int128.html), [blob](../../funcs/b/blob.html), [complex](../../funcs/c/complex.html), [point](../../funcs/p/point.html), [duration](../../funcs/d/duration.html), [decimal32](../../funcs/d/decimal32.html), [decimal64](../../funcs/d/decimal64.html), [decimal128](../../funcs/d/decimal128.html)。

每个这样的函数都有如下三个用处：

* 创建一个新的 NULL 值变量。
* 转换字符串。
* 转换其他数据类型。

注：

* 除了 *symbol* 函数之外，所有这些函数都接受 0 或 1
  个参数。如果没有设定参数，将创建一个默认值的标量。如果参数是字符串或字符串向量，可将它转换为目标数据类型。其他类型数据，只要语义上与目标数据类型相容，也会被转换。
* [short](../../funcs/s/short.html), [int](../../funcs/i/int.html), [long](../../funcs/l/long.html)
  函数将浮点数四舍五入为整数。当输入字符串时，这些函数会从字符串的第一个字符开始逐个判断，只要是数字就保存到结果中，否则立即输出结果。

## string

```
string()=="";  // 创建一个新的字符串，默认值为""。
```

返回：true

```
string(10);
```

返回：10

```
typestr string(108.5);
```

返回：STRING

```
string(now());
```

返回：2024.02.22T15:09:40.931

注： 以 字符串形式返回当前系统时间。

## bool

```
x=bool();
x;
```

返回：null

```
typestr x;
```

返回：BOOL

```
bool(`true);
```

返回：true

```
bool(`false);
```

返回：false

```
bool(`true`false)
```

返回：[true, false]

```
bool(100.2);
```

返回：true

```
bool(0);
```

返回：false

## decimal32

```
a=decimal32(142, 2)
a
```

返回：142.00

```
b=decimal32(1\7, 6)
b
```

返回：0.142857

```
a+b
```

返回：142.142857

```
a*b
```

返回：20.28569400

```
decimal32("3.1415926535", 4)
```

返回：3.1415

一个 DECIMAL 类型向量里的所有元素的类型和 scale 必须相同，例如：

```
d1=[1.23$DECIMAL32(4), 3$DECIMAL32(4), 3.14$DECIMAL32(4)];
```

返回：[1.2300,3.0000,3.1400]

```
typestr(d1);
```

返回：FAST DECIMAL32 VECTOR

```
d2=[1.23$DECIMAL32(4), 3$DECIMAL32(4), 3.14$DECIMAL32(3)];
```

返回：(1.2300,3.0000,3.140)

```
typestr(d2);
```

返回：ANY VECTOR

将 STRING 或 SYMBOL 类型转换为 DECIMAL 类型时，不同版本服务器的处理方式存在差别。2.00.10
之前版本会将超出 *scale* 的小数部分直接舍去。而 2.00.10 及之后的版本，会将超出 *scale*
的小数部分进行四舍五入。例如，对于以下的转换：

```
symbol(["1.341", "4.5677"])$DECIMAL32(2)
```

2.00.10 之前的版本，结果为：[1.34,4.56]

2.00.10 及之后的版本，结果为：[1.34,4.57]

## decimal64

```
a=decimal64(142, 2)
a
```

返回：142.00

```
b=decimal64(1\7, 6)
b
```

返回：0.142857

```
a+b
```

返回：142.142857

```
a*b
```

返回：20.28569400

```
decimal64("3.1415926535", 4)
```

返回：3.1415

一个 DECIMAL 类型向量里的所有元素的类型和 scale 必须相同，例如：

```
d1=[1.23$DECIMAL64(4), 3$DECIMAL64(4), 3.14$DECIMAL64(4)];
```

返回：[1.2300,3.0000,3.1400]

```
typestr(d1);
```

返回：FAST DECIMAL64 VECTOR

如果元素的 scale 不同，则会创建并输出元组：

```
d2=[1.23$DECIMAL64(4), 3$DECIMAL64(4), 3.14$DECIMAL64(3)];
```

返回：(1.2300,3.0000,3.140)

```
typestr(d2);
```

返回：ANY VECTOR

将 STRING 或 SYMBOL 类型转换为 DECIMAL 类型时，不同版本服务器的处理方式存在差别。2.00.10
之前版本会将超出 *scale* 的小数部分直接舍去。而 2.00.10 及之后的版本，会将超出 *scale*
的小数部分进行四舍五入。例如，对于以下的转换：

```
symbol(["1.341", "4.5677"])$DECIMAL64(2)
```

2.00.10 之前的版本，结果为：[1.34,4.56]

2.00.10 及之后的版本，结果为：[1.34,4.57]

## decimal128

```
a=decimal128(142, 2)
a
```

返回：142.00

```
b=decimal128(1\7, 6)
b
```

返回：0.142857

```
a+b
```

返回：142.142857

```
a*b
```

返回：20.28569400

```
decimal128("3.1415926535", 4)
```

返回：3.1416

一个 DECIMAL 类型向量里的所有元素的类型和 scale 必须相同，例如：

```
d1=[1.23$DECIMAL128(4), 3$DECIMAL128(4), 3.14$DECIMAL128(4)];
```

返回：[1.2300,3.0000,3.1400]

```
typestr(d1);
```

返回：FAST DECIMAL128 VECTOR

如果元素的 scale 不同，则会创建并输出元组：

```
d2=[1.23$DECIMAL128(4), 3$DECIMAL128(4), 3.14$DECIMAL128(3)];
```

返回：(1.2300,3.0000,3.140)

```
typestr(d2);
```

返回：ANY VECTOR

## int

```
x=int();
x;
```

返回：null

```
typestr x;
```

返回：INT

```
int(`10.9);
```

返回：10

```
int(2147483647);
```

返回：2,147,483,647

注： INT 数据类型的最大值为 231 -1 = 2,147,483,647。

```
int(2147483648);
```

由于2,147,483,648 超出了 INT 数据类型的最大值，因此返回：null

## short

```
x=short();
x;
```

返回：null

```
typestr x;
```

返回：SHORT

```
short(`12.3);
```

返回：12

```
short(`120.9c);
```

返回：120

```
short(32767);
```

返回：32,767

注： SHORT 数据类型的范围是[ -215+1, 215 -1] =
[-32767, 32767]。如果 *X* 超出了该范围，将会发生[溢出](../../funcs/s/../../progr/data_types.html#chap4_sect_data_type_description__section_oxj_hty_jxb)。

```
short(32768);
//Output
null

short(65578);
//Output
42

short(32789)
//Output
-32747
```

## long

```
x=long();
x;
```

返回：null

```
typestr x;
```

返回：LONG

```
long(`10.9);
```

返回：10

```
long(9223372036854775807l);
```

返回：9,223,372,036,854,775,807

注： LONG 数据类型的最大值是263-1 =
9,223,372,036,854,775,807。

```
long(9223372036854775808l);
```

返回：9,223,372,036,854,775,807

## char

```
x=char();
x;
```

返回：null

```
typestr x;
```

返回：CHAR

```
a=char(99);
a;
```

返回：'c'

```
typestr a;
```

返回：CHAR

```
char(a+5);
```

返回：'h'

```
char("990");
```

返回：`Failed to convert the string to CHAR`

注： `char` 函数会把输入的字符串识别为 ASCII 码，超出 ASCII
码范围的输入字符无法转换。

## double

```
x=double();  // 创建一个 DOUBLE 类型的变量，默认值为0。
x;
```

返回：null

```
typestr x;
```

返回：DOUBLE

```
typestr double(`10);
```

返回：DOUBLE

```
double(`10.9);
```

返回：10.9

```
double(now());
```

返回：1,708,616,927,949

注： 该例子首先使用 `now` 函数获得当前系统时间 2024.02.22
15:50:15.528，`double` 函数将该时间转换为 1,708,616,927,949。

## date

```
date();
```

返回：null

```
date(1)
```

返回：1970.01.02

```
date(`2011.10.12);
```

返回：2011.10.12

```
date(now());
```

返回：2024.02.22

```
date 2012.12.03 01:22:01;
```

返回：2012.12.03

```
date(2016.03M);
```

返回：2016.03.01

## datehour

```
datehour(1)
```

返回：1970.01.01T01

```
datehour(2012.06.13 13:30:10);
```

返回：2012.06.13T13

```
datehour([2012.06.15 15:32:10.158,2012.06.15 17:30:10.008]);
```

返回：[2012.06.15T15,2012.06.15T17]

```
datehour(2012.01M)
```

返回：2012.01.01T00

## datetime

```
datetime(1)
```

返回：1970.01.01 00:00:01

```
datetime(2009.11.10);
```

返回：2009.11.10 00:00:00

```
typestr datetime(2009.11.10);
```

返回：DATETIME

```
datetime(now());
```

返回：2024.02.22 15:55:39

```
datetime(2012.01M)
```

返回：2012.01.01T00:00:00

## timestamp

```
timestamp(1)
```

返回：1970.01.01 00:00:00.001

```
timestamp(2016.10.12);
```

返回：2016.10.12 00:00:00.000

```
timestamp(2016.10.12)+1;
```

返回：2016.10.12 00:00:00.001

```
timestamp(now());
```

返回：2024.02.22 15:57:33.291

```
timestamp(2012.01M)
```

返回：2012.01.01T00:00:00.000

## month

```
month();
```

返回：null

```
month(`2012.12);
```

返回：2012.12M

```
month(2012.12.23);  // 把一个 DATE 类型的数据转换成 MONTH 类型。
```

返回：2012.12M

```
month(now());  // 把一个 TIMESTAMP 类型的数据转换成 MONTH 类型。
```

返回：2024.02M

## second

```
second();
```

返回：null

```
second(1)
```

返回：00:00:01

```
second("19:36:12");
```

返回：19:36:12

```
second(now());
```

返回：16:01:32

```
second 2012.12.03 01:22:01;
```

返回：01:22:01

```
second(61);
```

返回：00:01:01

```
second("09:00:01")
```

返回：09:00:01

## minute

```
minute();
```

返回：null

```
minute(1)
```

返回：00:01m

```
minute(now());
```

返回：16:02m

## hour

```
hour(2012.12.03 01:22:01);
```

返回：1

## time

```
time();
```

返回：null

```
time(1)
```

返回：00:00:00.001

```
time("12:32:56.356");
```

返回：12:32:56.356

```
time(now());
```

返回：16:03:36.529

## symbol

```
x=`XOM`y;
typestr(x);
```

返回：STRING VECTOR

```
y=symbol(x);
y;
```

返回：["XOM","y"]

```
typestr(y);
```

返回：FAST SYMBOL VECTOR

## nanotime

```
nanotime(1000000000);
```

返回：00:00:01.000000000

```
nanotime(12:06:09 13:08:01);
```

返回：[12:06:09.000000000,13:08:01.000000000]

```
nanotime(2012.12.03 01:22:01.123456789);
```

返回：01:22:01.123456789

```
nanotime('13:30:10.008007006');
```

返回：13:30:10.008007006

## nanotimestamp

```
nanotimestamp(1);
```

返回：1970.01.01 00:00:00.000000001

```
nanotimestamp(1000000000);
```

返回：1970.01.01 00:00:01.000000000

```
nanotimestamp(2012.12.03 12:06:09 2012.12.03 13:08:01);
```

返回：[2012.12.03 12:06:09.000000000,2012.12.03 13:08:01.000000000]

```
nanotimestamp(2012.12.03 01:22:01.123456789);
```

返回：2012.12.03 01:22:01.123456789

```
nanotimestamp('2012.12.03 13:30:10.008007006');
```

返回：2012.12.03 13:30:10.008007006

```
nanotimestamp(now());
```

返回：2024.02.22 16:14:28.627000000

```
nanotimestamp(2012.01M)
```

返回：2012.01.01T00:00:00.000000000

## uuid

```
uuid("");
```

返回：00000000-0000-0000-0000-000000000000

```
a=uuid("9d457e79-1bed-d6c2-3612-b0d31c1881f6");
a;
```

返回：9d457e79-1bed-d6c2-3612-b0d31c1881f6

```
typestr(a);
```

返回：UUID

## ipaddr

```
a=ipaddr("192.168.1.13");
a;
```

返回：192.168.1.13

```
typestr(a);
```

返回：IPADDR

## int128

```
a=int128("e1671797c52e15f763380b45e841ec32")
```

返回：e1671797c52e15f763380b45e841ec32

```
typestr(a);
```

返回：INT128

## duration

```
y=duration("20H")
y
```

返回：20H

```
typestr(y)
```

返回：DURATION

```
duration("3XNYS")
```

返回：3XNYS

不指定时间单位，取时间列 time 的单位 s：

```
t=table(take(2018.01.01T01:00:00+1..10,10) join take(2018.01.01T02:00:00+1..10,10) join take(2018.01.01T08:00:00+1..10,10) as time, rand(1.0, 30) as x);
select max(x) from t group by bar(time, 5);
```

| bar\_time | max\_x |
| --- | --- |
| 2018.01.01T01:00:00 | 0.8824 |
| 2018.01.01T01:00:05 | 0.8027 |
| 2018.01.01T01:00:10 | 0.572 |
| 2018.01.01T02:00:00 | 0.8875 |
| 2018.01.01T02:00:05 | 0.8542 |
| 2018.01.01T02:00:10 | 0.4287 |
| 2018.01.01T08:00:00 | 0.9294 |
| 2018.01.01T08:00:05 | 0.9804 |
| 2018.01.01T08:00:10 | 0.2147 |

指定单位为 m，对时间列按照1分钟进行分组：

```
select max(x) from t group by bar(time, 1m);
```

| bar\_time | max\_x |
| --- | --- |
| 2018.01.01T01:00:00 | 0.8824 |
| 2018.01.01T02:00:00 | 0.8875 |
| 2018.01.01T08:00:00 | 0.9804 |

## cast(X, dataTypeName) / $

```
x=8.9$INT;
x;
```

返回：9

```
x=1..10;
x;
```

返回：[1,2,3,4,5,6,7,8,9,10]

```
typestr x;
```

返回：FAST INT VECTOR

```
x/2;
```

返回：[0,1,1,2,2,3,3,4,4,5]

```
x=x$DOUBLE;
typestr x;
```

返回：FAST DOUBLE VECTOR

```
x/2;
```

返回：[0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]

```
x=`IBM`MS;
typestr x;
```

返回：STRING VECTOR

```
x=x$SYMBOL;
typestr x;
```

返回：FAST SYMBOL VECTOR

```
x=`128.9;
typestr x;
```

返回：STRING

```
x=x$INT;
x;
```

返回：128

```
typestr x;
```

返回：INT

以下这个例子将向量转换为矩阵：

```
m=1..8$2:4;
m;
```

得到：

| 0 | 1 | 2 | 3 |
| --- | --- | --- | --- |
| 1 | 3 | 5 | 7 |
| 2 | 4 | 6 | 8 |

以下例子改变一个矩阵的形状：

```
m$4:2;
```

得到：

| 0 | 1 |
| --- | --- |
| 1 | 5 |
| 2 | 6 |
| 3 | 7 |
| 4 | 8 |

```
m$1:size(m);
```

得到：

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |

