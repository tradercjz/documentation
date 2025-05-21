# winsorize

## 语法

`winsorize(X, limit, [inclusive=true], [nanPolicy='upper'])`

## 参数

**X** 是一个向量。

**limit** 是一个标量或两个元素组成的向量，表示相对于未屏蔽数据的数目，数组的每一侧要掩盖的百分比，取值为0到1之间。若为标量，表示每侧均要掩盖的百分比。若
*X* 有 n 个元素（包括 NULL值 ），第 (n \* limit[0]) 个最小的元素和第 (n \* limit[1])
个最大的元素被屏蔽，未屏蔽的数据总数为 n \*(1-sum(limit))。若 *limit* 中一个元素为0，表示此侧不掩盖。

**inclusive** 是一个标量或两个元素组成的向量，表示在每一侧被屏蔽的数据数量应被截断（true）还是四舍五入（false）。

**nanPolicy** 是一个字符串，表示如何处理 NULL 值。可取以下值，默认值为 'upper'。

* 'upper'：将 NULL 值视为最大值进行掩盖。
* 'lower'：将 NULL 值视为最小值进行掩盖。
* 'raise'：抛出异常。
* 'omit'：不掩盖 NULL 值。

## 详情

将向量 *X* 中指定百分比的极值掩盖。将第 (limits [0]) 个最低值设置为第 (limits [0])
个百分位数，将第 (limits [1]) 个最高值设置为第 (1-limits [1]) 个百分位数。

`winsorize!` 是 `winsorize`
的原地改变版本。

## 例子

```
x=1..10
// output
winsorize(x, 0.1);
[2,2,3,4,5,6,7,8,9,9]

winsorize(x, 0.12 0.17);
// output
[2,2,3,4,5,6,7,8,9,9]

winsorize(x, 0.12 0.17, inclusive=false);
// output
[2,2,3,4,5,6,7,8,8,8]

x=1..20;
x[19:]=NULL;
x;
// output
[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,]

winsorize(x, 0.1);
// output
[3,3,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,18,18]

winsorize(x, 0.1, nanPolicy='upper');
// output
[3,3,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,18,18]

winsorize(x, 0.1, nanPolicy='lower');
// output
[2,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,17,2]
```

