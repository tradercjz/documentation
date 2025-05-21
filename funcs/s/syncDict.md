# syncDict

## 语法

`syncDict(keyObj, valueObj, [sharedName], [ordered=false])`

或

`syncDict(keyType, valueType, [sharedName], [ordered=false])`

## 参数

* 第一种用法中，**keyObj** 是表示键的标量或向量，**valueObj** 是表示值的标量或向量。
* 第二种用法中，**keyType** 是字典键的数据类型； **valueType**
  是字典值的数据类型。系统支持以下键的数据类型：Logical, Integral, Floating和Temporal。字典中的值不支持
  COMPLEX, POINT 类别。

**sharedName** 为一个字符串。指定后此字典会被共享，共享的字典名为 *sharedName*。

**ordered** 一个布尔值，默认为 false，表示创建一个无序字典。当 *ordered* = true
时，创建一个有序字典。无序字典在输出或进行遍历时，其键值对不保留输入时的顺序；有序字典在输出或进行遍历时，键值对的顺序与输入顺序保持一致。

## 详情

创建一个线程安全的同步字典。同步字典允许多个线程对其进行并发读写。

## 例子

例1：

```
x=1 6 3
y=4.5 7.8 4.3
z=syncDict(x,y);
// output
3->4.3
1->4.5
6->7.8

z=syncDict(INT,DOUBLE)
z[5]=7.9
z;
// output
5->7.9

syncDict(INT,DOUBLE, `sn)
sn[5 6]=10.99 2.33
sn[5];
// output
10.99

// y 为 DECIMAL32 类型的向量，将 y 作为 value 值创建有序字典 z
x=1 3 2
y = decimal32(1.23 3 3.14, 3)
z=dict(x,y,true);
z;
// output
1->1.230
3->3.000
2->3.140
```

下面的例子中，我们分别对普通字典 z1 和同步字典 z2 并发写入。

对普通字典 z1 进行多线程并发写入会造成节点崩溃：

```
def task1(mutable d,n){
    for(i in 0..n){
        d[i]=i*2
    }
}

def task2(mutable d,n){
    for(i in 0..n){
        d[i]=i+1
    }
}
n=10000000

z1=dict(INT,INT)
jobId1=submitJob("task1",,task1,z1,n)
jobId2=submitJob("task2",,task2,z1,n);
```

同步字典 z2 允许多线程并发写入：

```
z2=syncDict(INT,INT)
jobId3=submitJob("task1",,task1,z2,n)
jobId4=submitJob("task2",,task2,z2,n)
getJobReturn(jobId3, true)
getJobReturn(jobId4, true)
z2;
```

相关函数：[array](../a/array.html), [matrix](../m/matrix.html), [dictUpdate!](../d/dictUpdate_.html), [dict](../d/dict.html)

例 2：syncDict 与 [go](../../progr/statements/go.html)
配合使用：

```
syncDict(SYMBOL,RESOURCE,`resDict)
go
resDict[`a]=10
```

