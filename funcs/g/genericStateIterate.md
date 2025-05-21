# genericStateIterate

## 语法

`genericStateIterate(X, initial, window, func)`

## 参数

**X** 表中的字段或对表字段其应用向量函数的计算结果。通过元组方式传入多个列字段。传入 [] 表示不指定该参数。

**initial** 表中的字段或对表字段应用向量函数的计算结果。其作用是对输出表的第1~*window* 个计算结果进行填充。

**window** 非负整数，表示窗口的长度（以元素个数衡量）。

**func** 用户自定义的无状态函数，其返回值必须是标量，以部分应用的方式接收参数。当
*window* > 0 时，其第一个参数为当前记录向前取 *window* 个计算结果组成的向量；当 *window* = 0 时，其第一个参数为当前记录向前取1个计算结果。其后参数依次为
*X* 指定的列。

## 详情

基于以元素个数衡量的窗口进行迭代计算。

假设 *X* 指定为 [X1, X2, ..., Xn]，该函数计算结果对应输出表中的列为 factor，初始化字段为
initial，*window* 为 w，迭代函数为 func。

对于输入的第 k 条记录（k = 1, 2 …），其计算逻辑为：

* 当 w = 0 时：

  + k = 1 时：factor[0] = func(initial[0]，, X1[0],
    X2[0], … , Xn[0])
  + k > 1 时：factor[k-1] = func(factor[(k-2)],
    X1[k-1], X2[k-1], … , Xn[k-1])
* 当 w >0 时：
  + k <= w 时：factor[k-1] = initial[k-1]
  + k > w 时：factor[k-1] = func(factor[(k-1-w):k-1], X1[k-1], X2[k-1],
    … , Xn[k-1])

注意：数据对用于索引时，不包含右边界的值，即 (k-1-w):k-1 的范围是 [k-1-w, k-1)。

## 例子

```
// define a function
def myfunc(x, w){
re = sum(x*w)
return re
}

dateTime = 2021.09.09T09:30:00.000 2021.09.09T09:31:00.000 2021.09.09T09:32:00.000 2021.09.09T09:33:00.000 2021.09.09T09:34:00.000
securityID = `600021`600021`600021`600021`600021
volume = 310 280 300 290 240
price = 1.5 1.6 1.7 1.6 1.5
t = table(1:0, `dateTime`securityID`volume`price, [TIMESTAMP, SYMBOL, INT, DOUBLE])
tableInsert(t, dateTime, securityID, volume, price)
output = table(100:0, `securityID`dateTime`factor1, [SYMBOL, TIMESTAMP, DOUBLE])

engine = createReactiveStateEngine(name="test", metrics=[<dateTime>, <genericStateIterate(volume,price,3,myfunc{,})>], dummyTable=t, outputTable=output, keyColumn=`SecurityID, keepOrder=true)
engine.append!(t)
dropAggregator(`test)
```

| securityID | dateTime | factor1 |
| --- | --- | --- |
| 600021 | 2021.09.09T09:30:00.000 | 1.5 |
| 600021 | 2021.09.09T09:31:00.000 | 1.6 |
| 600021 | 2021.09.09T09:32:00.000 | 1.7 |
| 600021 | 2021.09.09T09:33:00.000 | 1,392 |
| 600021 | 2021.09.09T09:34:00.000 | 334,872 |

上例计算过程如下：

* 由于窗口为 3，因此对于前 3 条数据，以 price 的值作为 factor1 的输出；
* 第 4 条数据到来时，历史窗口的数据为 [1.5, 1.6, 1.7]，当前 volume 的值为 290，因此调用自定义函数 myfunc([1.5,
  1.6, 1.7], 290) = 1392；
* 第 5 条数据到来时，历史窗口的数据为 [1.6, 1.7, 1392]，当前 volume 的值为 240，因此调用自定义函数 myfunc([1.6,
  1.7, 1392], 240) = 334872；
* 若之后继续有数据注入，其计算过程以此类推。

相关函数：[genericTStateIterate](genericTStateIterate.html)

