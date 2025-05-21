# readObject

## 语法

`readObject(handle)`

## 参数

**handle** 是文件句柄。

## 详情

可以将所有的数据类型读取到句柄中，包括标量、向量、矩阵、集合、字典和表。该函数必须要用户登录后才能执行。

## 例子

```
a1=10.5
a2=1..10
a3=cross(*,1..5,1..10)
a4=set(`IBM`MSFT`GOOG`YHOO)
a5=dict(a4.keys(),125.6 53.2 702.3 39.7)
a6=table(1 2 3 as id, `Jenny`Tom`Jack as name)
a7=(1 2 3, "hello world!", 25.6)

fout=file("test.bin","w")
fout.writeObject(a1)
fout.writeObject(a2)
fout.writeObject(a3)
fout.writeObject(a4)
fout.writeObject(a5)
fout.writeObject(a6)
fout.writeObject(a7)
fout.close();
```

上述的脚本把 7 个不同类型的对象写到一个文件中。下述的脚本将这 7 个对象从文件中读取出来，并为每个对象打印一个简短的描述。

```
fin = file("test.bin")
for(i in 0:7) print typestr fin.readObject()
fin.close();

// output
DOUBLE
FAST INT VECTOR
INT MATRIX
STRING SET
STRING->DOUBLE Dictionary
TABLE
ANY VECTOR
```

