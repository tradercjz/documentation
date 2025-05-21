# 指定计算某一天的因子
orderTB = loadTable("dfs://TL_Level2", "entrust")
df = pd.DataFrame(orderTB, index="Market", lazy=True)
res = df[df["TradeTime"].astype(ddb.DATE)==2023.02.01][["TradeTime", "SecurityID", "OrderQty", "Price"]].groupby(["SecurityID"]).apply(lambda x: volumeWeightedAvgPrice(x, 60))
```

示例代码解析：

* 通过 `rolling(lag).sum()` 的方式分别计算前 lag 笔委托单的总委托金额和总委托量
* `orderTB = loadTable("dfs://TL_Level2", "entrust")` 通过 `loadTable` 函数，将 "dfs://TL\_Level2" 数据库下的分布式表 "entrust" 的元数据取回到内存。此时变量 orderTB 只包含元数据，库内数据并未取到内存。
* `df = pd.DataFrame(orderTB, index="Market", lazy=True)` 通过 `pd.DataFrame()` 函数，将 DolphinDB 的表转化为数据框。对于分布式表而言，*index* 为必填参数，可以指定表中的任意一列，该列仅作为索引，后续可以不参与计算；*lazy* 参数指定计算是否立即执行，必须指定为 True，表示该 DataFrame 会存储所有函数调用，尽可能延迟计算，以减少计算带来的性能消耗。
* 可以通过 df[过滤条件] 的形式选出库内指定范围的数据。比如：`df[(df["TradeTime"].astype(ddb.DATE)==2023.02.01)&(df["SecurityID"]=="000001")]` 指定取库内 2023.02.01 的“000001”这一天一只股票的数据。
* 建议在 `groupby` 执行计算函数之前，先对数据列进行过滤，只取出计算需要的列。可以降低内存使用，减少数据读取与拷贝的开销。
* lazy 模式下不允许直接改变 DataFrame 的值。因为 `volumeWeightedAvgPrice` 函数里面有 `res["orderWeightPrice"] = totalAmount/totalVolume` 的操作，所以对直接过滤出来的 df 直接调用函数 `volumeWeightedAvgPrice(df, 60)` 会报错： `Lazy-model DataFrame does not support update value.` 需要使用 `df.compute()` 将 lazy 模式的 DataFrame 强制触发计算，转化为 no-lazy 模式的 DataFrame。
* 可以通过 .groupby(分组列).apply(函数) 的方式实现分组计算，Python Parser 内部对 `groupby.apply` 实现了并行计算。

#### 4. 性能测试

##### 4.1. 性能测试环境

| CPU 类型 | Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz |
| --- | --- |
| 逻辑 CPU 总数 | 24 |
| 内存 | 256 GB |
| OS | CentOS Linux release 7.9.2009 (Core) |

##### 4.2. 性能测试结果

**测试数据**

* 2023 年单个交易所某日的 level-2 全天数据
  + 快照数据：24,313,086 行 × 62 列 [约 20.6 GB]
  + 逐笔成交：108,307,125 行 × 19 列 [约 11.0 GB]
  + 逐笔委托：141,182,534 行 × 16 列 [约 11.6 GB]

| 数据源 | 因子 | Python Parser 运行耗时 | DolphinDB Scripts 运行耗时 | Python 运行耗时 | DolphinDB Scripts / python parser 性能对比 | Python / python parser 性能对比 |
| --- | --- | --- | --- | --- | --- | --- |
| 日频 K 线 | 双均线因子 (单只股票） | 10.88 ms | 9.07 ms | 30 ms | 0.836 | 2.757 |
| 日频 K 线 | 双均线因子 (全市场股票） | 1.1 s | 0.566 s | 14.01 s | 0.515 | 12.74 |
| 快照行情 | 十档净委买增额 | 4.3 s | 1.4 s | 49.4 s | 0.326 | 11.488 |
| 快照行情 | 价格变动与一档量差的回归系数 | 2.8 s | 0.34 s | 25.5 s | 0.019 | 9.107 |
| 逐笔成交 | 主动成交量占比 | 6.9 s | 1.2 s | 52.9 s | 0.174 | 7.667 |
| 逐笔成交 | 当日尾盘成交占比 | 4.1 s | 0.31 s | 19.6 s | 0.076 | 4.780 |
| 逐笔委托 | 早盘买卖单大小比 | 5.8 s | 0.64 s | 21.1 s | 0.110 | 3.638 |
| 逐笔委托 | 委托量加权平均委托价格 | 7.2 s | 1.4 s | 77.2 s | 0.194 | 10.722 |

#### 5. 总结

DolphinDB Python Parser 支持 Python 的常用语法，并兼容了 DolphinDB 部分独有语法。相比于 Python API，Python Parser 能够方便地访问 DolphinDB 库内的数据，减少了网络层面的开销；并且针对 groupby 等函数底层自动实现并行计算，提高计算性能。相比于 DolphinDB Scripts，Python Parser 兼容常用 Python 语法，学习难度更低，用户可以轻松上手 DolphinDB。

本教程针对量化金融中最常见的因子计算场景，提供了一种基于 Python Parser 开发因子的解决方案，包括不同频率因子库的存储方案和基于不同频率不同数据源的基础因子开发代码，并且因子计算性能和 Python 多进程框架相比能有 5 倍以上的提升。

#### 6. 附件

* 示例数据：[tradeData.zip](data/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/tradeData.zip)
* 因子实现 DolphinDB 版本：
  + [当日尾盘成交占比.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E5%BD%93%E6%97%A5%E5%B0%BE%E7%9B%98%E6%88%90%E4%BA%A4%E5%8D%A0%E6%AF%94.txt)
  + [价格变动与一档量差的回归系数.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E4%BB%B7%E6%A0%BC%E5%8F%98%E5%8A%A8%E4%B8%8E%E4%B8%80%E6%A1%A3%E9%87%8F%E5%B7%AE%E7%9A%84%E5%9B%9E%E5%BD%92%E7%B3%BB%E6%95%B0.txt)
  + [十档净委买增额.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E5%8D%81%E6%A1%A3%E5%87%80%E5%A7%94%E4%B9%B0%E5%A2%9E%E9%A2%9D.txt)
  + [双均线.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E5%8F%8C%E5%9D%87%E7%BA%BF.txt)
  + [委托量加权平均委托价格.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E5%A7%94%E6%89%98%E9%87%8F%E5%8A%A0%E6%9D%83%E5%B9%B3%E5%9D%87%E5%A7%94%E6%89%98%E4%BB%B7%E6%A0%BC.txt)
  + [早盘买卖单大小比.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E6%97%A9%E7%9B%98%E4%B9%B0%E5%8D%96%E5%8D%95%E5%A4%A7%E5%B0%8F%E6%AF%94.txt)
  + [主动成交量占比.txt](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_DolphinDB%E7%89%88%E6%9C%AC/%E4%B8%BB%E5%8A%A8%E6%88%90%E4%BA%A4%E9%87%8F%E5%8D%A0%E6%AF%94.txt)
* 因子实现 Python 版本：
  + [双均线](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E5%8F%8C%E5%9D%87%E7%BA%BF.zip)
  + [当日尾盘成交占比.ipynb](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E5%BD%93%E6%97%A5%E5%B0%BE%E7%9B%98%E6%88%90%E4%BA%A4%E5%8D%A0%E6%AF%94.ipynb)
  + [价格变动与一档量差的回归系数.ipynb](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E4%BB%B7%E6%A0%BC%E5%8F%98%E5%8A%A8%E4%B8%8E%E4%B8%80%E6%A1%A3%E9%87%8F%E5%B7%AE%E7%9A%84%E5%9B%9E%E5%BD%92%E7%B3%BB%E6%95%B0.ipynb)
  + [十档委买增额.ipynb](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E5%8D%81%E6%A1%A3%E5%A7%94%E4%B9%B0%E5%A2%9E%E9%A2%9D.ipynb)
  + [委托量加权平均委托价格.ipynb](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E5%A7%94%E6%89%98%E9%87%8F%E5%8A%A0%E6%9D%83%E5%B9%B3%E5%9D%87%E5%A7%94%E6%89%98%E4%BB%B7%E6%A0%BC.ipynb)
  + [早盘买卖单大小比.ipynb](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E6%97%A9%E7%9B%98%E4%B9%B0%E5%8D%96%E5%8D%95%E5%A4%A7%E5%B0%8F%E6%AF%94.ipynb)
  + [主动成交量占比.ipynb](script/DolphinDB_Python_Parser_Intro_for_Quantitative_Finance/%E5%9B%A0%E5%AD%90%E5%AE%9E%E7%8E%B0_Python%E7%89%88%E6%9C%AC/%E4%B8%BB%E5%8A%A8%E6%88%90%E4%BA%A4%E9%87%8F%E5%8D%A0%E6%AF%94.ipynb)

