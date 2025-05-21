# subarray

## 语法

`subarray(X, range)`

## 参数

**X** 可以是向量或矩阵。

**range** 是表示范围的数据对，范围包括下限，不包括上限。若 *range* 不在 [0,
size(X)-1] 内，则超出 [0, size(X)-1] 的值所对应的位置返回空值。

## 详情

当使用某个向量的一部分元素进行计算时，例如若使用 close[10:].avg() 的语句，系统会从向量 close
中复制数据产生一个新的向量 close[10:] 再进行计算，不仅占用更多内存而且耗时。

`subarray`
函数返回输入向量的一个子向量。它是原向量的一个视图，只记录了原向量的指针以及子向量的开始和结束位置。由于并没有分配大块内存来存储新向量，所以没有发生数据复制。所有向量的只读操作都可直接应用于
`subarray` 。

## 例子

```
x=1..100
subarray(x, 10:20);
// output
[11,12,13,14,15,16,17,18,19,20]

subarray(x, 90:);
// output
[91,92,93,94,95,96,97,98,99,100]

subarray(x, :10);
// output
[1,2,3,4,5,6,7,8,9,10]

a=rand(1000.0,20000000);
timer a.subarray(0:1000000).avg();
// output
Time elapsed: 1.5 ms

timer a[0:1000000].avg();
// output
Time elapsed: 8 ms

// subarray is read-only:
b=a.subarray(0:1000000);
b[0]=1;
// output
b[0] = 1 => Immutable sub vector doesn't support method set
```

