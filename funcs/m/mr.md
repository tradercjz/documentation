# mr

## 语法

`mr(ds, mapFunc, [reduceFunc], [finalFunc], [parallel=true])`

## 参数

**ds** 数据源列表。该参数必选，且必须是元组，元组的每个元素都是数据源对象。即使只有一个数据源，我们仍然需要一个元组来包装数据源。

**mapFunc** map 函数。它只接受一个参数，即相应数据源的物化数据实体。如果希望 map
函数接受除了物化数据源之外更多的参数，可以使用 [部分应用](../../progr/partial_app.md)
将多参数函数转换为一个参数的函数。map 函数调用的次数是数据源的数量。map
函数返回一个常规对象（标量，对，数组，矩阵，表，集合或字典）或一个元组（包含多个常规对象）。

**reduceFunc** 二元 reduce 函数组合了两个 map 函数调用结果。在大多数情况下，reduce
函数是不重要的。一个例子是加法函数，reduce 函数是可选的。如果没有指定 reduce 函数，则系统将所有单独的 map 调用结果返回到最终函数。

**finalFunc** final 函数，只接受一个参数。该函数的输入是最后一个 reduce
函数的输出。如果未指定，系统将返回所有 map 函数调用结果。

**parallel** 指示是否在本地并行执行 map 函数的可选布尔标志。默认值为
true，即启用并行计算。当可用内存有限和每个 map
调用需要大量的内存时，我们可以禁用并行计算以防止内存不足问题。我们也可能要禁用并行选项以确保线程安全。例如，如果多个线程同时写入同一个文件，则可能会发生错误。

## 详情

Map-Reduce 函数是 DolphinDB 通用分布式计算框架的核心功能。

## 例子

以下是分布式线性回归的示例。X 是自变量的矩阵，y 是因变量。X 和 y 存储在多个数据源中。为了估计最小二乘参数，我们需要计算 X
T X 和 X T y 。我们可以从每个数据源计算 (X T X, X
T y) 的元组，然后将所有数据源的结果相加，以获得整个数据集的 X T X 和 X
<sup>T</sup> y。

```
def myOLSMap(table, yColName, xColNames, intercept){
  if(intercept)
      x = matrix(take(1.0, table.rows()), table[xColNames])
  else
      x = matrix(table[xColNames])
  xt = x.transpose();
  return xt.dot(x), xt.dot(table[yColName])
}

def myOLSFinal(result){
  xtx = result[0]
  xty = result[1]
  return xtx.inv().dot(xty)[0]
}

def myOLSEx(ds, yColName, xColNames, intercept){
  return mr(ds, myOLSMap{, yColName, xColNames, intercept}, +, myOLSFinal)
}
```

在上面的例子中，我们定义了 map 函数和 final
函数。实践中，我们也可为数据源定义转换函数。这些功能仅需在本地实例中定义，用户不需要编译它们或将其部署到远程实例。DolphinDB
的分布式计算框架可以为最终用户快速处理这些复杂的问题。

作为经常使用的分析工具，分布式最小二乘线性回归已经在我们的核心库中实现。内置版本([olsEx](../o/olsEx.md))提供更多功能。

