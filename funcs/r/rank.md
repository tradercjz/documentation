# rank

## 语法

`rank(X, [ascending=true],
[groupNum], [ignoreNA=true], [tiesMethod='min'], [percent=false],
[precision])`

## 参数

**X** 是一个向量、矩阵或表。

**ascending** 是一个布尔值，表示是否按升序排序。默认值是 true。

**groupNum** 是一个正整数，指定该参数后，元素将分成指定数量的组，按组进行排序。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值，默认值为 true。false 表示 NULL 作为最小值参与排名。

**tiesMethod** 是一个字符串，表示如何对具有相同值的元素进行排名。

* 'min' 表示取最小排名。
* 'max' 表示取最大排名。
* 'average' 表示取排名的均值。
* 'first' 表示按照原数据的顺序排名。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名。

**precision** 是一个 [1, 15] 范围内的整数，用于设置参与排序的值的精度。若两个值之差的绝对值小于等于 10^(-precision)
，则认为两值相等。

注： 指定 *precision* 参数后，*X* 只能是数值型对象。且
*tiesMethod* 不能指定为 'first'。

## 详情

基于 *ascending* 指定的排序顺序，返回 *X* 中每个元素的排名（从0开始排序）。

* 若 *X* 是向量，返回一个与*X*等长的向量：
  + 如果指定了 *groupNum*，则将排序后的 *X* 分成
    *groupNum* 个组。返回 *X* 中每个元素对应的组编号（从0开始编号）。

    注：
    - 若 *X* 不能被均分，则前 mod(size(X), groupNum) 组将多存放一个元素。例如
      *X* 的元素个数为6，*groupNum* =
      4，排名后的第1和2个元素属于组0，第3和4个元素属于组1，第5个和第6个元素分别属于组2和组3。
    - 若 *X* 中相同元素分别属于不同的组，则所有相同元素返回最小的组号。
  + 如果 *ignoreNA* = true，则 NULL 值不参与排序，结果中 NULL
    值的排名为空。
* 若 *X* 是矩阵或表，在每列内进行上述计算，返回一个与 *X* 维度相同的矩阵或表。

## 例子

```
rank(45 16 32 21);
// output
[3,0,2,1]

rank(45 16 32 21, false);
// output
[0,3,1,2]

rank(9 1 6 1 3 3);
// output
[5,0,4,0,2,2]
// 两个相同的元素有相同的排名

rank(X=9 5 4 8 1 3 6 2 7, groupNum=3);
// output
[2,1,1,2,0,0,1,0,2]

rank(X=9 5 4 8 1 3 6 2 7, groupNum=6)
// output
[5,2,1,4,0,1,2,0,3]

rank(X=9 5 4 8 1 3 6 2 7, ascending=false, groupNum=3);
// output
[0,1,1,0,2,2,1,2,0]

rank(X=1 2 2 3, tiesMethod='min');
// output
[0,1,1,3]

rank(X=1 2 2 3, tiesMethod='average');
// output
[0,1.5,1.5,3]

rank(X=1 2 2 3, tiesMethod='first');
// output
[0,1,2,3]

rank(1 NULL NULL 3);
// output
[0,,,1]

rank(X=1 NULL NULL 3, ignoreNA=false);
// output
[2,0,0,3]

t=table(1 1 1 2 2 2 2 as id, 3 5 4 6 2 7 1 as x)
t
```

| id | x |
| --- | --- |
| 1 | 3 |
| 1 | 5 |
| 1 | 4 |
| 2 | 6 |
| 2 | 2 |
| 2 | 7 |
| 2 | 1 |

```
select *, rank(x) from t context by id;
```

| id | x | rank\_x |
| --- | --- | --- |
| 1 | 3 | 0 |
| 1 | 5 | 2 |
| 1 | 4 | 1 |
| 2 | 6 | 2 |
| 2 | 2 | 1 |
| 2 | 7 | 3 |
| 2 | 1 | 0 |

