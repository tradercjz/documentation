# movingTopNIndex

## 语法

`movingTopNIndex(X, window, top, [ascending=true], [fixed=false],
[tiesMethod='oldest'])`

## 参数

**X** 是一个数值型/时间类型的向量。注意：从 2.00.10 版本开始，*X* 中的空值不参与排序。

**window** 必须是不小于2的正整数，表示窗口长度。

**top** 是一个大于1，小于等于 *window* 的整数。

**ascending** 是一个布尔值，表示窗口内值的排序方式。true 表示升序，false 表示降序。

**fixed** 是一个布尔值。表示输出的数组向量每行的长度是否固定为 *top*。默认值为 false。设置为 true 时所有窗口的长度相同，前(
*top* - 1)个窗口内缺少的索引用 NULL 填充。

**tiesMethod** 字符串。在滑动窗口内对 X 进行排序后，如果有多个具有相同值的元素无法全部进入前
*top*，可以通过该参数来指定选择元素的方式。可选值为：

* 'oldest'：从最早进入窗口的元素开始选取，直至达到 *top* 个。
* 'latest'：从最晚进入窗口的元素开始向前选取，直至达到 *top* 个。

## 详情

返回一个数组向量，表示 *X* 在每一个滑动窗口内按照指定顺序排序后的前 *top* 个元素所对应的索引。

**首发版本**：2.00.4

## 例子

```
S = 2 5 6 1 2 4 5 6 9 0

m1 = movingTopNIndex(X=S, window=4, top=2, ascending=true, fixed=true)
m1;
// output
[[,0],[0,1],[0,1],[3,0],[3,4],[3,4],[3,4],[4,5],[5,6],[9,6]]

m2 = movingTopNIndex(X=S, window=4, top=2, ascending=false, fixed=true)
m2;
// output
[[,0],[1,0],[2,1],[2,1],[2,1],[2,5],[6,5],[7,6],[8,7],[8,7]]

m3 = movingTopNIndex(X=S, window=4, top=2, ascending=true, fixed=false)
print m3;
// output
[[0],[0,1],[0,1],[3,0],[3,4],[3,4],[3,4],[4,5],[5,6],[9,6]]

S[m1[0]]
// output
[,2,2,1,1,1,1,2,4,0]

S[m3[0]]
// output
[2,2,2,1,1,1,1,2,4,0]

X = [5, 8, 1, 9, 7, 3, 1, NULL, 0, 8, 7, 7]
movingTopNIndex(X=X, window=4, top=2, ascending=true, fixed=true)
// 2.00.10 之前的版本，X 中的空值也参与排序，结果是：
[[00i,0],[0,1],[2,0],[2,0],[2,4],[2,5],[6,5],[7,6],[7,8],[7,8],[7,8],[8,10]]

// 2.00.10 及之后版本，X 中的空值会被忽略，结果是：
[[00i,0],[0,1],[2,0],[2,0],[2,4],[2,5],[6,5],[6,5],[8,6],[8,6],[8,10],[8,10]]

X = [2, 1, 4, 3, 4, 3, 4]

// 第6个滑动窗口中，X 排序后是 1 2 3 3 4 4，只取前3个排名，根据 tiesMethod 的设置值来选取哪个3被选取

// tiesMethod 未指定，则取默认值 'oldest'，即选取第一次出现的3，其对应 X 中的索引是3
movingTopNIndex(X,6,3)

// output
[[0],[1,0],[1,0,2],[1,0,3],[1,0,3],[1,0,3],[1,3,5]]]

// tiesMethod = 'latest'，即选最后一次出现的3，其对应 X 中的索引是5
movingTopNIndex(X,6,3,tiesMethod="latest")

// output
[[0],[1,0],[1,0,2],[1,0,3],[1,0,3],[1,0,5],[1,3,5]]
```

