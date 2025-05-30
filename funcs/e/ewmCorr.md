# ewmCorr

## 语法

`ewmCorr(X, [com], [span], [halfLife], [alpha], [minPeriods=0],
[adjust=true], [ignoreNA=false], [other], [bias=false])`

## 参数

**X** 是一个数值型向量、矩阵或表。若 *X* 是表，只对其内数值型和布尔型的列进行计算。

**com** 是一个大于等于0的数值型标量，表示质心。

**span** 是一个大于等于1的数值型标量，表示跨度。

**halfLife** 是一个大于0的数值型标量，表示半衰期。

**alpha** 是一个(0,1]之间的浮点数，表示平滑系数。

**minPeriods** 是一个整数，表示窗口中的最小观察数。默认值为0。

**adjust** 是一个布尔值，表示是否除以开始阶段的衰减调整因子。默认值为 true。

**ignoreNA** 是一个布尔值，表示计算权重时是否忽略NULL值。默认值为 false。

**other** 当 *X* 是向量时，*other* 只能是一个与 *X* 长度相同的数值型向量；当 *X*
是矩阵时，*other* 是一个长度与 *X* 行数相同的数值型向量，或维度与 *X* 相同的矩阵；当 *X*
是表时，*other* 是一个长度与 *X* 行数相同的数值型向量，或维度与 *X* 相同的表。

**bias** 是一个布尔值，表示是否校正系统偏差。默认值为 false。

## 详情

返回 *X* 和 *other* 的指数加权移动相关系数。该函数必须指定 *com*, *span*,
*halfLife*, *alpha* 四个参数中的一个。

## 例子

```
a=[0,1,2,int(),4]
b=[2,4,3,6,5]
ewmCorr(X=a,other=b,com=0.5);
// output
[,1.0000,-0.0533,-0.0533,0.9146]

ewmCorr(X=a,other=b,com=0.5,ignoreNA=true);
// output
[,1.0000,-0.0533,-0.0533,0.8934]

n = 20
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
t1 = table(n:0, colNames, colTypes)
insert into t1 values(09:30:00.001,`AAPL,100,56.5)
insert into t1 values(09:30:00.001,`AAPL,200,30.5)
insert into t1 values(09:30:00.001,`DELL,150,35.5)
insert into t1 values(09:30:00.001,`DELL,170,60.5)
insert into t1 values(09:30:00.001,`DELL,130,40.5)
b=[2,4,3,6,5]
ewmCorr(X=t1,other=b,com=0.5);
```

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | AAPL |  |  |
| 09:30:00.001 | AAPL | 1.0000 | -1.0000 |
| 09:30:00.001 | DELL | 1.0000 | -0.8481 |
| 09:30:00.001 | DELL | 0.5536 | 0.8747 |
| 09:30:00.001 | DELL | 0.3064 | 0.7050 |

相关函数：[ewmCov](ewmCov.md), [ewmMean](ewmMean.md), [ewmStd](ewmStd.md), [ewmVar](ewmVar.md)

