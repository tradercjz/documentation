# exists

## 语法

`exists(path)`

## 参数

**path** 字符串标量或向量，表示服务器端文件或文件夹的路径。

## 详情

检查指定的文件或文件夹是否存在。`exists` 函数也能在分布式文件系统中使用。

## 例子

```
t=table(1..10 as ID, rand(1.0, 10) as x);
saveText(t, "/home/DolphinDB/Data/t.txt");

exists("/home/DolphinDB/Data/t.txt");
// output
true
exists("/home/DolphinDB/Data/t1.txt");
// output
false
exists("/home/DolphinDB/Data");
// output
true

exists(["/home/DolphinDB/Data/t.txt","/home/DolphinDB/Data/t1.txt","/home/DolphinDB/Data"]);
// output
[true,false,true]
```

在分布式文件系统中检查文件或文件夹是否存在（以下脚本需要在集群中的数据节点/计算节点中执行）：

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)

db = database("dfs://valueDB", VALUE, 2017.08.07..2017.08.11)
pt = db.createPartitionedTable(t, `pt, `date);
pt.append!(t);

exists("dfs://valueDB/20170807");
// output
true
```

