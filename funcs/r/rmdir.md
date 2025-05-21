# rmdir

## 语法

`rmdir(directory,
[recursive=false],
[keepRootDir=false])`

## 参数

**directory** 必备参数，用于指定要删除的文件夹名称。如果该目录不为空，则通过设定 *recursive* 的值为 true
可以删除所有子目录和文件

**recursive** 布尔值，可选参数，用于是否删除所有指定文件夹所有子目录及其中文件。默认值为 false。

**keepRootDir** 布尔值，可选参数，用于指定是否保留根目录。默认值为 false。当设置为 true
时，仅删除子目录和文件，而不会删除根目录。

注： 若设置
*keepRootDir*=true，则必须设置 *recursive*=true。

## 详情

删除目录。默认情况下，要删除的目录必须为空。如果目录不为空仍然要删除它时，请设置 *recursive*
的值为true。

注： 该命令在用户登录后才能执行。

## 例子

```
files("/home/test");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| dir1 | 1 | 0 | 1496650004836 | 1496650004836 |
| dir2 | 1 | 0 | 1496650002210 | 1496650002210 |
| dir3 | 1 | 0 | 1496649999597 | 1496649999597 |

```
// delete a directory. dir1 is empty, dir2 is not empty.
rmdir("/home/test/dir1");
rmdir("/home/test/dir2");
// output
Failed to remove directory [/home/test/dir2] with error code 145

// Delete a directory recursively
rmdir("/home/test/dir2", true);

files("/home/test");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| dir3 | 1 | 0 | 1496649999597 | 1496649999597 |

