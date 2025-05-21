# rowAlign

## 语法

`rowAlign(left, right,
how)`

## 参数

**left/right** 是数组向量或列式元组。

注：

* *left* 和 *right*
  的长度和类型必须相同，但它们对应的每行向量的个数可以相同或不同。例如：*left*
  的长度是3，其第一行向量的长度是5，则 *right* 的长度必须是3，其每一行向量的长度可以是5或者其它值。
* 必须保证 *left*/*right* 中每行向量的数据严格有序排列。

**how** 字符串，用于指定数据对齐的方式。设置值不同，会影响 *left* 和 *right* 对齐的数据范围。可选值为：

| how(不区分大小写) | 含义 | 对齐后的最大值 | 对齐后的最小值 |
| --- | --- | --- | --- |
| "bid" | 表示 left/right 为多档买方报价数据，其数据严格降序排列。此时，仅将有效档位内的数据进行对齐。 | max(max(left), max(right)) | max(min(left), min(right)) |
| "allBid" | 表示 left/right 为多档买方报价数据，其数据严格降序排列。此时，将 left 和 right 所有数据进行对齐。 | max(max(left), max(right)) | min(min(left), min(right) |
| "ask" | 表示 left/right 为多档卖方报价数据，其数据严格升序排列。此时，仅将有效档位内的数据进行对齐。 | min(max(left), max(right)) | min(min(left), min(right)) |
| ”allAsk“ | 表示 left/right 为多档卖方报价数据，其数据严格升序排列。此时，将 left 和 right 所有数据进行对齐。 | max(max(left), max(right)) | min(min(left), min(right) |

## 详情

对 *left* 和 *right* 中的每一行向量，根据其元素值进行对齐。返回一个长度为 2 的元组，分别表示对齐后的数据在原向量中的索引。若
*left/right* 中不存在数据与 *right/left* 的元素值相等，则返回 -1。

该函数主要应用于金融场景下对多档买卖报价进行价格对齐，*left* 是某个时刻的买价/卖价，而 *right* 则是上一时刻的买价/卖价。通常结合
`rowAt` 函数，按行取出索引对应的元素。

注意：若 *left/right* 是列式元组，则返回的元组内的元素也是列式元组。

下图演示某行的 *left* 和 *right* 对齐的过程。图中标注出对齐方式为 “bid“ 和 “allBid“ ，”ask” 和
“allAsk“ 时的区别（ 蓝色背景是以 “bid“ 或 “ask“ 对齐时，超出有效档位的数据）。

通过 `rowAt` 函数可以按行取出对应索引的元素。

* *how* = "bid" 或 "allBid" 时，bid 中某行数据的对齐过程如下图所示：
  ![rowAlign1](../../images/rowAlign_1.png)
* *how* = "ask" 或 "allAsk" 时，ask 中某行数据的对齐过程如下图所示：
  ![rowAlign2](../../images/rowAlign_2.png)

## 例子

```
left = array(DOUBLE[], 0, 5).append!([9.01 9.00 8.99 8.98 8.97, 9.00 8.98 8.97 8.96 8.95, 8.99 8.97 8.95 8.93 8.91])
right = array(DOUBLE[], 0, 5).append!([9.02 9.01 9.00 8.99 8.98, 9.01 9.00 8.99 8.98 8.97, 9.00 8.98 8.97 8.96 8.95])
leftIndex, rightIndex = rowAlign(left, right, "bid")
leftIndex
//output:[[-1,0,1,2,3],[-1,0,-1,1,2],[-1,0,-1,1,-1,2]]
left.rowAt(leftIndex)
//output:[[,9.01,9.00,8.99,8.98],[,9,,8.99,8.97],[,8.99,,8.97,,8.95]]

rightIndex
//output:[[0,1,2,3,4],[0,1,2,3,4],[0,-1,1,2,3,4]]
right.rowAt(rightIndex)
//output:[[9.02,9.01,9.00,8.99,8.98],[9.01,9.00,8.99,8.98,8.97],[9.00,,8.98,8.97,8.96,8.95]]

// 输出 left 与 right 数据对齐后的买方报价
left.rowAt(leftIndex).nullFill(right.rowAt(rightIndex))
//output:[[9.02,9.01,9,8.99,8.98],[9.01,9.00,8.99,8.98,8.97],[9.00,8.99,8.98,8.97,8.96,8.95]]

// 假定 bid 对应的 qty 如下
 leftBidQty = array(INT[], 0, 5).append!([10 5 15 20 13, 12 15 20 21 18, 7 8 9 9 10])
 rightBidQty = array(INT[], 0, 5).append!([8 12 10 12 8, 10 5 15 18 13, 12 15 20 21 19])

// 计算 left 和 right 五档报价对应委托量的变化
leftBidQty.rowAt(leftIndex).nullFill(0) - rightBidQty.rowAt(rightIndex).nullFill(0)
//output:[[-8,-2,-5,3,12],[-10,7,-15,-3,7],[-12,7,-15,-12,-21,-10]]

leftIndex, rightIndex = rowAlign(left, right, "allBid")
leftIndex
//output:[[-1,0,1,2],[-1,-1,0,1,2],[-1,0,-1,1,2]]

rightIndex
//output:[[0,1,2,-1],[0,1,2,-1,-1],[0,-1,1,2,-1]]

left = array(DOUBLE[], 0, 3).append!([8.99 9.00 9.01, 8.97 8.99 9.00, 8.95 8.97 8.99])
right = array(DOUBLE[], 0, 3).append!([9.00 9.01 9.02, 8.99 9.00 9.01, 8.97 8.98 9.00])
leftIndex, rightIndex = rowAlign(left, right, "ask")
leftIndex
//output:[[0,1,2],[0,1,2],[0,1,-1,2]]

rightIndex
//output:[[-1,0,1],[-1,0,1],[-1,0,1,-1]]

leftIndex, rightIndex = rowAlign(left, right, "allAsk")
leftIndex
//output:[[0,1,2,-1],[0,1,2,-1],[0,1,-1,2,-1]]

rightIndex
//output:[[-1,0,1,2],[-1,0,1,2],[-1,0,1,-1,2]]

sym = `st1`st2`st3
left = [[3.1,2.5,2.8], [3.1,3.3], [3.2,2.9,3.3]]
left.setColumnarTuple!()
right = [[3.1,2.5,2.8], [3.1,3.3], [3.2,2.9,3.3]]
right.setColumnarTuple!()
rowAlign(left, right, "bid")
//output:[([0,1,2],[0,1],[0,1,2]), ([0,1,2],[0,1],[0,1,2])]
```

