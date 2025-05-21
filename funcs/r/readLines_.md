# readLines!

## 语法

`readLines!(handle, holder, [offset=0], [length=1])`

## 参数

**handle** 是文件句柄。

**holder** 是用于保存读取的数据的变量。

**offset** 表示数据保存至holder的起始位置。

**length** 是从文件中读取的行数。

## 详情

从句柄中读取给定数量的字符串，并从指定位置开始，把读取结果保存至 *holder*
表示的变量中。函数返回实际读取的行数。

[readLines](readLines.md)
函数的每次调用都创建了一个字符串向量并返回。创建字符串向量需要一定的时间开销，所以如果在重复执行函数调用时，能重用相同的向量作为缓冲区的话，可以节约时间。
`readLines!`函数接受已存在的缓冲区作为数据容器。

下述的两个例子读取相同数量的数据 100 次，结果显示：`readLines!` 函数比
`readLines` 函数更快。

## 例子

```
 timer(100){
 fin = file("test.txt")
 do{ y=fin.readLines(1024) } while(y.size()==1024)
 fin.close()
 };
// output
Time elapsed: 79.511 ms

 timer(100){
 fin = file("test.txt")
 y=array(STRING,1024)
 do{ lines = fin.readLines!(y,0,1024) } while(lines==1024)
 fin.close()
 };

// output
Time elapsed: 56.034 ms
```

