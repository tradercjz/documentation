# extractTextSchema

## 语法

`extractTextSchema(filename, [delimiter], [skipRows=0])`

## 参数

**filename** 字符串，表示输入数据的绝对路径或相对路径。仅支持 CSV 格式的文件。若传入其他格式文件，则无法保证数据准确性。

**delimiter** 字符串标量，表示数据文件中各列的分隔符。分隔符可以是一个或多个字符，默认是逗号（","）。

**skipRows** 是0到1024之间的整数，表示从文件头开始忽略的行数。它是一个可选参数。默认值为0。

## 详情

生成输入数据文件的表的结构。表的结构有两列：列名和数据类型。

数据文件中包含了表达时间、日期的数据时：

* 满足分隔符要求的这部分数据（日期数据分隔符包含"-"、"/"和"."，时间数据分隔符为":"）会转换为相应的类型。例如，"12:34:56"转换为SECOND类型；"23.04.10"转换为DATE类型。
* 对于不包含分隔符的数据，形如"yyMMdd"的数据同时满足0<=yy<=99，0<=MM<=12，1<=dd<=31，会被优先解析成DATE；形如"yyyyMMdd"的数据同时满足1900<=yyyy<=2100，0<=MM<=12，1<=dd<=31会被优先解析成DATE。

注： 从 2.00.10 版本开始，`loadText`
支持加载一条记录中包含多个换行符的数据文件。

## 例子

```
n=1000000
timestamp=09:30:00+rand(18000,n)
ID=rand(100,n)
qty=100*(1+rand(100,n))
price=5.0+rand(100.0,n)
t1 = table(timestamp,ID,qty,price)
saveText(t1, "/home/DolphinDB/Data/t1.txt")
schema=extractTextSchema("/home/DolphinDB/Data/t1.txt");
schema;
```

| name | type |
| --- | --- |
| timestamp | SECOND |
| ID | INT |
| qty | INT |
| price | DOUBLE |

