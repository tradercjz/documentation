# 文件操作

文件操作包括：

* 列出文件清单
* 打开和关闭文件
* 以及文件中读写游标的移动。

## 列出文件清单

可以使用 [files](../../funcs/f/files.html)
函数来列出一个文件夹下的文件和子文件夹目录。它返回以下信息：

* 文件名
* 是否为文件夹（0表示文件，1表示文件夹）
* 文件大小
* 上次访问时间
* 上次修改时间

```
files("C:/DolphinDB");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| LICENSE\_AND\_AGREEMENT.txt | 0 | 22558 | 1495508675000 | 1483773234998 |
| README\_WIN.txt | 0 | 5104 | 1495508675000 | 1483866232680 |
| server | 1 | 0 | 1496624932437 | 1496624932437 |
| THIRD\_PARTY\_SOFTWARE\_LICENS... | 0 | 8435 | 1495508675000 | 1483628426506 |

```
files("C:/DolphinDB", "readme%");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| README\_WIN.txt | 0 | 5104 | 1495508675000 | 1483866232680 |

我们也可以使用SQL语句来操作返回的表。

```
select * from files("C:/DolphinDB") where filename like "DolphinDB%";
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| DolphinDB 1.lnk | 0 | 824 | 1499933602000 | 1500344826000 |
| DolphinDB 2.lnk | 0 | 790 | 1499933685000 | 1501832205000 |
| DolphinDB 3.lnk | 0 | 1006 | 1501829666000 | 1501832213000 |
| DolphinDB 4(acl).lnk | 0 | 872 | 1501829402000 | 1502626190412 |

## 打开/关闭文件

使用file函数以指定模式打开文件。打开模式有6种："r", "r+", "w", "w+", "a", "a+"（详情参考
[file](../../funcs/f/file.html) 函数） [close](../../funcs/c/close.html) 命令用来关闭打开的文件。

```
fout=file("C:/DolphinDB/test.txt","w");
fout.writeLine("hello world!");

1

fout.close();
fin = file("C:/DolphinDB/test.txt");
print fin.readLine();

hello world!

fin.close();
```

下例中，使用一个函数打开文件。当函数结束时，这个文件自动被关闭。大部分情况下，我们不必显式地关闭文件，除非必须立刻关闭文件。当系统关闭时，所有打开的文件都会被关闭。

```
def myread(f): file(f).readLine()
myread("C:/DolphinDB/test.txt");

Hello World!
```

## 在一个文件中移动读写游标

当系统从一个文件读数据或向一个文件写数据时，内部文件读写游标会向前移动。用户可以通过 [seek](../../funcs/s/seek.html) 函数手动操作这个游标。除了接受一个文件句柄参数，seek
函数还可以接受其他两个参数：偏移量和起始位置。偏移量可以是正负值，起始位置必须是以下之一：HEAD，CURRENT，或TAIL。如果操作成功，seek
函数返回内部游标的最终位置。

```
// 写一个函数来显示文件的长度
def fileLength(f): file(f).seek(0, TAIL)
fileLength("C:/DolphinDB/test.txt");

14

// 将内部游标移动到文件开始处
fin=file("C:/DolphinDB/test.txt")
fin.readLine();

Hello World!
fin.seek(0, HEAD);

0
fin.readLine();

Hello World!
```

