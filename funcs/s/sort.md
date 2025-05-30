# sort

## 语法

`sort(X, [ascending=true])`

[sort!](sort_.md) 是 `sort`
的原地版本。

## 参数

**X** 可以是向量。

**ascending** 是一个布尔值，表示按升序排序还是按降序排序。默认值为 true（按升序排序）。

## 详情

返回一个排序后的向量。

## 例子

```
x=9 1 5;
x;
// output
[9,1,5]

y=sort(x);
y;
// output
[1,5,9]

sort(x, false);  // 逆序排序
// output
[9,5,1]

x=1 4 2 5 6 3$2:3;
x;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 2 | 6 |
| 4 | 5 | 3 |

```
sort x;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

sort! 函数排序并修改输入。

```
x=9 1 5;
sort!(x);
x;

[1 5 9];
```

相关函数：[isort](../i/isort.md)

