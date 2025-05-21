# genericTStateIterate

## 语法

`genericTStateIterate(T, X, initial, window, func, [leftClosed =
false])`

## 参数

**T** 非严格递增的时间类型或整型的向量，且不能包含 NULL 值。注意，时间乱序的数据在计算中会被直接丢弃。

**X** 表中的字段或对其应用向量函数的计算结果。若不指定，需要置为[]；若需要输入多个列变量，需要用元组表示。

**initial** 用于初始化的列字段，作为初始化窗口内元素的输出，初始化窗口为 [t0, t0 + *window*)（t0
为第一条数据的时间戳，以时间衡量窗口）。*initial* 可以是输入表中的字段或对其应用向量函数的计算结果。

**window** 正整型或 DURATION 标量，表示初始化窗口和历史窗口的长度。当 *window* 为整数时，其单位与 T 一致。

**func** 无状态函数，为用户自定义函数，其返回值必须是标量。以部分应用的形式传入。*func* 参数个数为 1（历史窗口内的数据）+
*X* 指定的列数，第一个参数对应历史窗口的元素值，之后的参数依次对应 X *指定列的元素值*。除前述参数外，若 *func*
包含其他固定的常量参数，则需以部分应用的形式指定。

**leftClosed** 布尔值，表示历史窗口是否包含左边界的数据，默认为 false。

## 详情

基于以时间衡量的窗口进行迭代计算。

假设时间列为 *T*，*X* 指定为 [X1, X2, ..., Xn]，该函数计算结果对应输出表中的列为
factor，初始化字段为 *initial*，*window* 为 w，迭代函数为 func。

以 Tk 表示第 k 条数据的时间戳，对于第 k 条记录(k = 1, 2 ...)，其计算逻辑为：

* Tk ∈ [T1, T1+w)：factor[k] = initial[k]
* 其他情况下，第 k+1 条记录对应的窗口为 (Tk-w, Tk] (leftClosed=false) / [Tk-w, Tk]
  (leftClosed=true)：factor[k] = func(subFactor, X1[k], X2[k], ... , Xn[k])，其中
  subFactor 为当前窗口范围内 factor 的值。

注：

数据对用于索引时，不包含右边界的值，即 (k-w):k 的范围是 [k-w, k)。

## 例子

指定 *leftClosed*=false：

```
// define a function
def myfunc(x, w){
     re = sum(x*w)
     return re
    }

dateTime = 2021.09.09T09:28:00.000 2021.09.09T09:28:30.000 2021.09.09T09:30:00.000 2021.09.09T09:31:00.000 2021.09.09T09:32:00.000
securityID = `600021`600021`600021`600021`600021
volume = 310 280 300 290 240
price = 1.5 1.6 1.7 1.6 1.5
t = table(1:0, `dateTime`securityID`volume`price, [TIMESTAMP, SYMBOL, INT, DOUBLE])
tableInsert(t, dateTime, securityID, volume, price)
output = table(100:0, `securityID`dateTime`factor1, [SYMBOL, TIMESTAMP, DOUBLE])

engine = createReactiveStateEngine(name="test", metrics=[<dateTime>, <genericTStateIterate(dateTime,volume,price,2m,myfunc{,})>], dummyTable=t, outputTable=output, keyColumn=`SecurityID, keepOrder=true)
engine.append!(t)
dropAggregator(`test)
```

| securityID | dateTime | factor1 |
| --- | --- | --- |
| 600021 | 2021.09.09T09:28:00.000 | 1.5 |
| 600021 | 2021.09.09T09:28:30.000 | 1.6 |
| 600021 | 2021.09.09T09:30:00.000 | 930 |
| 600021 | 2021.09.09T09:31:00.000 | 270,164 |
| 600021 | 2021.09.09T09:32:00.000 | 65,062,560 |

上例计算过程如下：

* 由于第 1 条数据的时间戳为 09:28:00.000 窗口为 2 min，因此初始化窗口为 [2021.09.09T09:28:00.000,
  2021.09.09T09:30:00.000)，前 2 条数据均属于该窗口，因此直接输出 price 的值。
* 第 3 条记录对应的窗口为 (2021.09.09T09:26:30.000, 2021.09.09T09:28:30.000]，该历史窗口内的元素为
  [1.5, 1.6]，当前 volume 的值为 300，因此调用自定义函数 myfunc([1.5, 1.6], 300) = 930；
* 同理第 4 条记录对应的窗口为 (2021.09.09T09:28:00.000, 2021.09.09T09:30:00.000]，该历史窗口内的元素为
  [1.6, 930]，当前 volume 的值为 290，因此调用自定义函数 myfunc([1.6, 930], 290) = 270164；
* 以此类推。

指定 *leftClosed*=true:

```
engine = createReactiveStateEngine(name="test", metrics=[<dateTime>, <genericTStateIterate(dateTime,volume,price,2m,myfunc{,},true)>], dummyTable=t, outputTable=output, keyColumn=`SecurityID, keepOrder=true)
```

| securityID | dateTime | factor1 |
| --- | --- | --- |
| 600021 | 2021.09.09T09:28:00.000 | 1.5 |
| 600021 | 2021.09.09T09:28:30.000 | 1.6 |
| 600021 | 2021.09.09T09:30:00.000 | 930 |
| 600021 | 2021.09.09T09:31:00.000 | 270,599 |
| 600021 | 2021.09.09T09:32:00.000 | 65,166,960 |

上例计算过程如下：

* 由于第 1 条数据的时间戳为 09:28:00.000 窗口为 2 min，因此初始化窗口为 [2021.09.09T09:28:00.000,
  2021.09.09T09:30:00.000)，前 2 条数据均属于该窗口，因此直接以 price 的值作为 factor1 的输出。
* 第 3 条记录对应的窗口为 [2021.09.09T09:26:30.000, 2021.09.09T09:28:30.000]，该历史窗口内的元素为
  [1.5, 1.6]，当前 volume 的值为 300，因此调用自定义函数 myfunc([1.5, 1.6], 300) = 930；
* 同理第 4 条记录对应的窗口为 [2021.09.09T09:28:00.000, 2021.09.09T09:30:00.000]，该历史窗口内的元素为
  [1.5, 1.6, 930]，当前 volume 的值为 290，因此调用自定义函数 myfunc([1.5, 1.6, 930], 290) =
  270599；
* 以此类推。

相关函数：[genericStateIterate](genericStateIterate.html)

