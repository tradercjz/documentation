# convertExcelFormula

## 语法

`convertExcelFormula(formula, colStart, colEnd, rowStart,
rowEnd)`

## 参数

**formula** 是字符串标量或向量，表示 Excel 公式。

**colStart** 是字符串标量，表示数据在 Excel 中起始列。

**colEnd** 是字符串标量，表示数据在 Excel 中结束列。

**rowStart** 是整型标量，表示数据在 Excel 中起始行。*rowStart* 值应大于0。

**rowEnd** 是整型标量，表示数据在 Excel 中起始行。*rowEnd* 值应大于等于
*rowStart*。

## 详情

将 Excel 表达式转换为对应的 DolphinDB 表达式。

该函数目前只支持包含四则运算，逻辑运算，聚合函数的转换。

该函数目前不支持对行和列同时操作的表达式的转换。聚合函数对单列进行计算时，如果处理的行数与实际的行数相同，则将该列进行聚合操作；如果处理行数与实际行数不同，则进行移动聚合操作。

## 例子

```
convertExcelFormula("A2+B2", "A", "Z", 2, 10);
// output
col0+col1

convertExcelFormula("SUM(A2:C2)", "A", "Z", 2, 10);
// output
rowSum(col0, col1, col2)

convertExcelFormula("SUM(A2)", "A", "Z", 2, 10);
// output
cumsum(col0)

convertExcelFormula("SUM(A2:A5)", "A", "Z", 2, 10);
// output
msum(col0, 4)

convertExcelFormula("SUM(A2:A10)", "A", "Z", 2, 10);
// output
sum(col0)

convertExcelFormula(["=SUM(A1:A10)","IF(A1>0,B1,0"], "A", "D", 1, 10)
// output
["sum(col0)","iif(col0>0,col1,0)"]
```

