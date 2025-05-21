# loadMvccTable

## 语法

`loadMvccTable(path, tableName)`

## 参数

**path** 是一个字符串，表示绝对路径或相对路径。

**tableName** 是一个字符串，表示表名。

## 详情

把磁盘上可并发读写的表加载到内存中。

## 例子

```
n=5
syms=`IBM`C`MS`MSFT`JPM`ORCL`FB`GE
timestamp=09:30:00+rand(18000,n)
sym=rand(syms,n)
qty=100*(1+rand(100,n))
price=5.0+rand(100.0,n)
temp=table(timestamp,sym,qty,price)
t1= mvccTable(1:0,`timestamp`sym`qty`price,[TIMESTAMP,SYMBOL,INT,DOUBLE],"/home/DolphinDB/Data","t1")
t1.append!(temp);

loadMvccTable("/home/DolphinDB/Data","t1");
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 1970.01.01T00:00:39.091 | MSFT | 4500 | 99.808702 |
| 1970.01.01T00:00:35.293 | FB | 3600 | 26.644715 |
| 1970.01.01T00:00:36.334 | MSFT | 3800 | 66.754334 |
| 1970.01.01T00:00:40.362 | ORCL | 4800 | 15.480288 |
| 1970.01.01T00:00:35.565 | MSFT | 1700 | 23.107408 |

