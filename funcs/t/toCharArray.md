# toCharArray

## 语法

`toCharArray(X)`

## 参数

**X** STRING/BLOB/SYMBOL 类型标量或向量。

## 详情

将字符串拆分字符向量。

* 若 *X* 是标量，返回一个向量。
* 若 *X* 是向量，返回一个数组向量。

## 例子

```
str = "It is great!\n"
print str.toCharArray()
// output
['I','t',' ','i','s',' ','g','r','e','a','t','!',10]

str1 = ["A#", "B C", "D\t"]
print str1.toCharArray()
// output
[['A','#'],['B',' ','C'],['D',9]]
```

将一个包含了 BLOB 类型的数据写入文件，需要使用 `toCharArray`
进行转换，以保证写入的数据正确。

```
//将一个向量压缩后，存入一个二进制文件
x=1..100
//BLOB 类型的字符串开头会使用4个字节来标识它的长度
y=blob(compress(x).concat())
dir = WORK_DIR+"/toCharArray.bin"
g = file(dir, "w")
//使用 toCharArray 函数对 BLOB 类型的字符串进行转换，则只会将正确的数据写入文件（头部的4个字节不会写入）
g.write(y.toCharArray())   //实际写入了467个字节
g.close()

// output
dir1 = WORK_DIR+"/toCharArray1.bin"
g1 = file(dir1, "w")
g1.write(y)    //实际写入了471个字节
g1.close()
```

相关函数：[split](../s/split.html)

