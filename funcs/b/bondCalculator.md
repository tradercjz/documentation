# bondCalculator

## 语法

`bondCalculator(start, maturity, issuePrice, coupon, frequency,
dayCountConvention, bondType, calendar, businessDayConvention, settlement,
price, priceType, [calcRisk=false], [benchmark='Qeubee'])`

## 详情

该函数用于实现债券到期收益率、净价和全价三者之间的互算，同时支持计算久期、凸度等风险指标。

**返回值：**字典或元组。

## 参数

注意：所有输入向量必须等长，输入标量将自动扩展以匹配其它向量的长度。

**start** DATE 类型标量或向量，表示债券的起息日。

**maturity** 与 *start* 等长的 DATE 类型标量或向量，表示债券的到期日。

**issuePrice** 与 *start*
等长的数值型标量或向量，表示债券的发行价格。贴现债需指定真实发行价（通常小于100）；其他债券通常为100。

**coupon** 数值型标量或向量，表示债券的票面利率。例如 0.03，表示票息为 3%。

**frequency** 整型或 STRING 类型的标量或向量，表示债券的付息频率。可选值为：

* 0/“Once”：到期一次还本付息
* 1/“Annual”：每年付息一次
* 2/“Semiannual：每半年付息一次
* 4/“Quarterly”：每季度付息一次
* 12/“Monthly”：每月付息一次

**dayCountConvention** STRING 类型的标量或向量，表示债券的计息日数惯例。可选值为：

* "Thirty360US"：US (NASD) 30/360
* "ActualActual"：实际/实际
* "Actual360"：实际/360
* "Actual365"：实际/365
* "Thirty360EU"：欧洲 30/360

**bondType** STRING 类型标量或向量，表示债券的类型。可选值为：

* "FixedRate"：固定利率债券，定期按息票利率支付利息。
* "Discount"：贴现债券，没有利息支付，以贴现方式发行的债券，期末FV=面值。
* "ZeroCoupon"：零息债券，期末一次性支付利息和面值，期末FV=面值+利息。

**calendar** STRING 类型标量，表示使用的交易日历。目前仅支持 “CFET”，表示中国人民银行债券交易日历（以 .IB 结尾的债券）。

**businessDayConvention** STRING 类型的标量，表示把非工作日调整到工作日的方法。目前仅支持
“Unadjusted”，表示不作调整。

**settlement** DATE 类型标量或向量，表示债券的结算日，即购买日期。

**price** 数值型标量或向量，具体含义取决于 priceType 的取值：

* 当 *priceType* 为 "YTM" 时，*price* 表示债券的到期收益率；
* 当 *priceType* 为 "CleanPrice" 时，*price* 表示债券的净价；
* 当 *priceType* 为 "DirtyPrice" 时，*price* 表示债券的全价。

**priceType** STRING 类型的标量或向量，用于指定债券价格类型，可选值为：

* "YTM"：到期收益率
* "CleanPrice"：净价
* "DirtyPrice"：全价

**calcRisk** 可选参数，布尔值，默认为 false，只计算输出全价、净价、应计利息和收益率。若设置为
true，除上述4项外，还会计算并输出麦考利久期、修正久期、凸度、基点价值。

**benchmark** 可选参数，STRING 类型标量，表示算法参考基准。目前仅支持 “Qeubee”（国内债券算法）。

## 例子

例1. 计算固定利率债券的价格、到期收益率、应计利息和风险指标。

```
bondCalculator(start=2022.07.15, maturity=2072.07.15, issuePrice=100, coupon=0.034, frequency="Semiannual", dayCountConvention="ActualActual", bondType="FixedRate", calendar="CFET", businessDayConvention="Unadjusted", settlement=2025.04.10, price=0.02, priceType="YTM", calcRisk=true);

/* Output:
pvbp->0.3902
ytm->0.0200
macaulayDuration->27.4761
dirtyPrice->143.4689
accruedInterest->0.7983
cleanPrice->142.6705
modifiedDuration->27.2041
convexity->1025.4003
*/

bondCalculator(start=2022.07.15, maturity=2072.07.15, issuePrice=100, coupon=0.034, frequency="Semiannual", dayCountConvention="ActualActual", bondType="FixedRate", calendar="CFET", businessDayConvention="Unadjusted", settlement=2072.04.18, price=100.2143, priceType="CleanPrice", calcRisk=false);

/* Output:
accruedInterest->0.8780
cleanPrice->100.2143
ytm->0.0250
dirtyPrice->101.0923
*/
```

例2. 计算零息债券的价格、到期收益率、应计利息和风险指标。

```
bondCalculator(start=2025.01.09, maturity=2026.02.05, issuePrice=100, coupon=0.0119, frequency="Annual", dayCountConvention="ActualActual", bondType="ZeroCoupon", calendar="CFET", businessDayConvention="Unadjusted", settlement=2025.04.10, price=0.025, priceType="YTM", calcRisk=true);

/* Output:
pvbp->0.0080
ytm->0.0250
macaulayDuration->0.8246
dirtyPrice->99.2322
accruedInterest->0.2966
cleanPrice->98.9355
modifiedDuration->0.8079
convexity->1.3057
*/
```

例3. 计算贴现债券的价格、到期收益率、应计利息和风险指标。

```
bondCalculator(start=2025.02.13, maturity=2025.05.15, issuePrice=99.663, coupon=0.0, frequency="Once", dayCountConvention="ActualActual", bondType="Discount", calendar="CFET", businessDayConvention="Unadjusted", settlement=2025.04.10, price=0.02, priceType="YTM", calcRisk=true);

/* Output:
pvbp->0.0009
ytm->0.0200
macaulayDuration->0.0958
dirtyPrice->99.8085
accruedInterest->0.2073
cleanPrice->99.6012
modifiedDuration->0.0957
convexity->0.0183
*/
```

例4. 同时计算多种债券的价格、到期收益率、应计利息和风险指标。

```
result = bondCalculator(start=[2025.02.13, 2025.01.09, 2022.07.15], maturity=[2025.05.15, 2026.02.05, 2072.07.15], issuePrice=[99.663, 100, 100], coupon=[0.0, 0.0119, 0.034], frequency=["Once", "Annual", "Semiannual"], dayCountConvention=["ActualActual", "ActualActual", "ActualActual"], bondType=["Discount", "ZeroCoupon", "FixedRate"], calendar=["CFET", "CFET", "CFET"], businessDayConvention=["Unadjusted", "Unadjusted", "Unadjusted"], settlement=[2025.04.10, 2025.04.10, 2072.04.18], price=[0.02, 0.025, 100.2143], priceType=["YTM", "YTM", "CleanPrice"], calcRisk=true);

print result

/* Output:
(dirtyPrice->99.808586272901294
cleanPrice->99.601201657516682
ytm->0.02
accruedInterest->0.207384615384617
macaulayDuration->0.095890410958904
modifiedDuration->0.095706863549357
convexity->0.018319607460911
pvbp->0.000955236674747
,dirtyPrice->99.232212603180983
cleanPrice->98.935527671674137
ytm->0.025
accruedInterest->0.296684931506849
macaulayDuration->0.824657534246575
modifiedDuration->0.80799946312328
convexity->1.305726264815019
pvbp->0.008017957450791
,dirtyPrice->101.092321978021971
cleanPrice->100.214299999999994
ytm->0.025000792220527
accruedInterest->0.878021978021978
macaulayDuration->0.240437158469945
modifiedDuration->0.239000497930427
convexity->0.114242476021984
pvbp->0.002416111528969
)
*/
```

相关函数：[bondAccrInt](bondaccrint.html)、[bondConvexity](bondconvexity.html)、[bondDirtyPrice](bondDirtyPrice.html)、[bondDuration](bondDuration.html)、[bondYield](bondyield.html)

