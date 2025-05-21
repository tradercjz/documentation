# saveTextFile

## 语法

`saveTextFile(content, filename, [append=false],
[lastModified])`

## 参数

**content** 是要写入文件的内容。

**filename** 是要保存的文件名。仅支持 CSV 格式的文件。若传入其他格式文件，则无法保证数据准确性。

**append** 是一个布尔值。True 表示追加，False表示覆盖。

**lastModified** 是最后修改的时间，显示的是1970年1月1日零时开始的秒数。

## 详情

通过追加或覆盖将字符串保存到文件中。该函数必须要用户登录后才能执行。

## 例子

```
saveTextFile("1234567890\n0987654321\nabcdefghijk\n", "/home/test/abc.txt", false, 1495762562671l);

// output
[content of file "/home/test/abc.txt"]
1234567890
0987654321
abcdefghijk
```

