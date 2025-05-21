# 数据类型

## Python Parser 支持的类型

与 Python 类似，Python Parser 的数据类型涵盖整数、浮点数、字符串、布尔值、空值、变量和常量等。不同之处在于，Python Parser 的数据类型与 DolphinDB 中的数据类型保持兼容。例如：None 对应 DolphinDB 的 VOID；整数的精度与 DolphinDB 的整数类型保持一致，而不是任意的精度。

以下表格对比了 DolphinDB、Python Parser 和 Python 中的数据类型。在 Python 列中留空表示 Python 不支持对应类型：

| **数据类型** | **DolphinDB** | **Python Parser** | **Python** |
| --- | --- | --- | --- |
| VOID | NULL | None | None |
| BOOL | 1b, 0b, true, false | 1b, 0b, True, False, bool(1) | True, False |
| CHAR | 'a', 97c | 97c, char('a') |  |
| SHORT | 122h | 122h |  |
| INT | 21 | 21 | 21 |
| LONG | 22l | 22l |  |
| DATE | 2013.06.13 | 2013.06.13 | 2013-06-13 |
| MONTH | 2012.06M | 2012.06M | 2012-06 |
| TIME | 13:30:10.008 | 13:30:10.008 | 13:30:10.008 |
| MINUTE | 13:30m | 13:30m | 13:30 |
| SECOND | 13:30:10 | 13:30:10 | 13:30:10 |
| DATETIME | 2012.06.13 13:30:10 or 2012.06.13T13:30:10 | 2012.06.13 13:30:10 or 2012.06.13T13:30:10 | 2012-06-13 13:30:10 |
| TIMESTAMP | 2012.06.13 13:30:10.008 or 2012.06.13T13:30:10.008 | 2012.06.13 13:30:10.008 or 2012.06.13T13:30:10.008 | 2012-06-13 13:30:10.008000 |
| NANOTIME | 13:30:10.008007006 | 13:30:10.008007006 | 13:30:10.008007006 |
| NANOTIMESTAMP | 2012.06.13 13:30:10.008007006 or 2012.06.13T13:30:10.008007006 | 2012.06.13 13:30:10.008007006 or 2012.06.13T13:30:10.008007006 | 2012.06.13 13:30:10.008007006 |
| FLOAT | 2.1f（单精度） | 2.1f（单精度） | 2.1（双精度） |
| DOUBLE | 2.1, 2.1F（双精度） | 2.1, 2.1F（双精度） |  |
| SYMBOL | symbol([`A,`B,`C]) | symbol(\[`A,`B,`C].toddb()) |  |
| STRING | "Hello" or 'Hello' or `Hello | "Hello" or 'Hello' or `Hello or """Hello""" or '''Hello''' | "Hello" or 'Hello' or """Hello""" or '''Hello''' |
| UUID | uuid("9d457e79-1bed-d6c2-3612-b0d31c1881f6") | uuid("9d457e79-1bed-d6c2-3612-b0d31c1881f6") | 9d457e79-1bed-d6c2-3612-b0d31c1881f6 |
| FUNCTIONDEF | def f1(a,b) {return a+b;} | def f1(a,b): return a+b |  |
| HANDLE | file handle, socket handle, and db handle | file handle, socket handle, and db handle |  |
| CODE | <1+2> | <1+2> |  |
| DATASOURCE | data source | data source |  |
| RESOURCE | model (kmeans) | model (kmeans) |  |
| ANY | (1,2,3) | (1,2,3) | (1,2,3) |
| COMPRESSED | compress(seq(1,10), "delta") | compress(seq(1,10), "delta") |  |
| ANY DICTIONARY | {“a”:1,"b":2} | {"a":1,"b":2} | {"a":1,"b":2} |
| DATEHOUR | datehour(2012.06.13 13:30:10) or datehour(2012.06.13T13:30:10) | 使用ddb的datehour函数生成datehour(2012.06.13 13:30:10) or datehour(2012.06.13T13:30:10) | 2012-06-13 13:30:10 |
| IPADDR | ipaddr("192.168.1.13") | ipaddr("192.168.1.13") | ipaddress.IPv4Address("192.168.1.13") |
| INT128 | int128("e1671797c52e15f763380b45e841ec32") | int128("e1671797c52e15f763380b45e841ec32") |  |
| BLOB | blob(str) | blob(str) |  |
| COMPLEX | complex(2, 5) | complex(2, 5) | complex(2, 5) |
| POINT | point(117.60972, 24.118418) | point(117.60972, 24.118418) |  |
| DURATION | 1s, 3M, 5y, 200ms | 1s, 3M, 5y, 200ms |  |
| DECIMAL32(S) | 3.1415926$DECIMAL32(3), decimal32(3.1415926, 3) | decimal32(3.1415926, 3) | decimal.Decimal(3.1415926)，Python 的 decimal 类型不区分32/64/128位，其最大支持位数由 Python 版本和机器硬件决定 |
| DECIMAL64(S) | 3.1415926$DECIMAL64(3), 3.141P, decimal64(3.1415926, 3) | decimal64(3.1415926, 3) |  |
| DECIMAL128(S) | 3.1415926$DECIMAL128(3), decimal128(3.1415926, 3) | decimal128(3.1415926, 3) |  |

## 查看数据类型

使用 `type` 函数可以查看对象的数据类型：

```
type(None)
// output: dolphindb.SCALAR.VOID
```

## 保留字

### 常量保留字

Python Parser 支持 Python 的部分保留字，如：True, False, None 等，其和 DolphinDB 的常量保留字兼容，见下表：

| **Python** | **DolphinDB** |
| --- | --- |
| True | ddb.true |
| False | ddb.false |
| None | ddb.VOID |

在调用 DolphinDB 内置函数时，若需要输入一些仅 DolphinDB 支持的保留字，可通过 dolphindb 模块来调用，如：

```
import dolphindb as ddb
ddb.NULL
ddb.VOID
ddb.pi
ddb.e
ddb.HINT_KEEPORDER
ddb.RANGE
...
```

使用 `is` 操作符判断两个变量是否为同一对象：

```
None is ddb.VOID
// output: true
None is ddb.NULL
// output: false
```

### 编程保留字

Python Parser 兼容了 Python 与 DolphinDB 大部分的编程保留字，暂不支持以下保留字：`global`, `nonlocal`, `del`, `yield`, `match`, `async`, `await`, `with`。

```
def zero(s):
    a = int(s)
    assert a > 0,"a超出范围"
    return a

zero("-2")
// output: Testing case adhocTesting_"a超出范围" failed
```

```
n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0:
        continue
    print(n)
// output:
1
3
5
7
9
```

raise 语句仅支持 raise expression

```
def test_exception():
    try:
            raise "asdf"
    except Exception as ex:
            assert ex[0]=="USER"

    print("test_exception test pass")

test_exception()
```

