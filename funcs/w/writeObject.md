# writeObject

## 语法

`writeObject(handle, object)`

## 详情

*object*
是要写入的数据，可以把所有类型的数据结构（包括标量、向量、矩阵、集合、字典和表）写入句柄。该函数必须要用户登录后才能执行。

## 例子

```
a1=10.5
a2=1..10
a3=cross(*,1..5,1..10)
a4=set(`IBM`MSFT`GOOG`YHOO)
a5=dict(a4.keys(),125.6 53.2 702.3 39.7)
a6=table(1 2 3 as id, `Jenny`Tom`Jack as name)
a7=(1 2 3, "hello world!", 25.6);
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

