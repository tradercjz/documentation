# crmwCBond

## 语法

`crmwCBond(settlement, maturity, fv, ys, yd)`

## 详情

本函数使用中债估值方法，对标的债务为到期一次还本付息的短期债券的信用风险缓释凭证（Credit Risk Mitigation Warrant,
CRMW）进行估值。成功执行后将返回 CRMW 的估值价格，是一个 DOUBLE 类型的标量或向量。

## 语法

**settlement** DATE 类型标量或向量，表示 CRMW 的估值日。

**maturity** DATE 类型标量或向量，表示标的债券的到期日。

注意：*settlement* 应早于对应的 *maturity*。

**fv** 数值型标量或向量，非负数，表示标的债券到期时还本付息总金额。

**ys** 数值型标量或向量，非负数，表示 CRMW 创设机构估价收益率。

**yd** 数值型标量或向量，非负数，表示标的债券的估价收益率。

注意：如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同、所有元素值等于该标量的向量；且所有向量的长度必须一致。

## 例子

假设 CRMW 的标的债券到期日为 2024 年 9 月 1 日，到期时还本付息总金额为 105，CRMW 创设机构估价收益率为 5.3%，标的债券的估价收益率
5.8%。估值日为 2024 年 3 月 1
日。

```
crmwCBond(settlement=2024.03.01, maturity=2024.09.01, fv=105, ys=0.053, yd=0.058)
// Output: 0.249800655
```

