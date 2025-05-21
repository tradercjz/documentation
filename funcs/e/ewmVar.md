# ewmVar

## 语法

`ewmVar(X, [com], [span], [halfLife], [alpha], [minPeriods=0], [adjust=true],
[ignoreNA=false], [bias=false])`

## 参数

**X** 是一个数值型向量、矩阵或表。若 *X* 是表，只对其内数值型和布尔型的列进行计算。

**com** 是一个大于等于0的数值型标量，表示质心。

**span** 是一个大于等于1的数值型标量，表示跨度。

**halfLife** 是一个大于0的数值型标量，表示半衰期。

**alpha** 是一个(0,1]之间的浮点数，表示平滑系数。

**minPeriods** 是一个整数，表示窗口中的最小观察数。默认值为0。

**adjust** 是一个布尔值，表示是否除以开始阶段的衰减调整因子。默认值为 true。

**ignoreNA** 是一个布尔值，表示计算权重时是否忽略 NULL 值。默认值为 false。

**bias** 是一个布尔值，表示是否校正系统偏差。默认值为 false。

## 详情

返回 *X* 的指数加权移动方差。该函数必须指定 *com*, *span*, *halfLife*, *alpha*
四个参数中的一个。

## 例子

```
a=[0,1,2,int(),4]
ewmVar(X=a,com=0.5);
// output
[,0.5,0.846154,0.846154,2.960165]

ewmVar(X=a,com=0.5,ignoreNA=true);
// output
[,0.5,0.846154,0.846154,2.819231]

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
ewmVar(X=t1,com=0.5);
```

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | AAPL |  |  |
| 09:30:00.001 | AAPL | 4999.9999 | 337.9999 |
| 09:30:00.001 | DELL | 1538.4615 | 85.5384 |
| 09:30:00.001 | DELL | 541.5384 | 297.2807 |
| 09:30:00.001 | DELL | 754.3801 | 161.1487 |

相关函数：[ewmCorr](ewmCorr.md), [ewmCov](ewmCov.md), [ewmMean](ewmMean.md), [ewmStd](ewmStd.md)

