# imr

## 语法

`imr(ds, initValue, mapFunc, [reduceFunc], [finalFunc], terminateFunc,
[carryover=false])`

## 参数

**ds**
数据源列表。它必须是每个元素作为数据源对象的元组。即使只有一个数据源，我们仍然需要一个元组来包装数据源。在迭代计算中，数据源自动缓存，缓存将在最后一次迭代后被清除。

**initValue** 模型参数估计的初始值。初始值的格式必须与最终函数的输出相同。

**mapFunc**
map函数。它有两个参数。第一个参数是由相应数据源表示的数据实体。第二个参数是前一次迭代中最终函数的输出，这是对模型参数的更新估算。对于第一次迭代，它是用户给出的初始值。

**reduceFunc** 二元 reduce 函数组合了两个 map 函数调用结果。如果有 M 个 map
调用，reduce 函数将被调用 M-1 次。在大多数情况下，reduce 功能是不重要的。一个例子是加法函数。reduce 函数是可选的。

**finalFunc**
每次迭代的最终函数。它接受两个参数。第一个参数是前一次迭代中最终函数的输出。对于第一次迭代，它是用户给出的初始值。第二个参数是 reduce
函数调用的输出。如果没有指定 reduce 函数，则各个 map 调用结果的集合的元组将是第二个参数。

**terminateFunc**
这是一个确定计算是否继续的函数，或是指定次数的迭代。终止函数接受两个参数。第一个是前一次迭代中 reduce 函数的输出，第二个是当前迭代中 reduce
函数的输出。如果函数返回 true，迭代将结束。

**carryover** 布尔值，表示 map 函数调用是否生成一个传递给下一次 map 函数调用的对象。默认值为
false。如果 *carryover* 为 true，那么 map 函数有3个参数并且最后一个参数为携带的对象，同时 map
函数的输出结果是一个元组，最后一个元素为携带的对象。在第一次迭代中，携带的对象为 NULL。

## 详情

DolphinDB 提供了基于 map-reduce 方法的迭代计算函数
`imr`。每次迭代使用上一次迭代的结果和输入数据集。每次迭代的输入数据集不变，因此可以被缓存。迭代计算需要模型参数的初始值和终止标准。

## 例子

现在我们使用分布式中位数计算的例子来说明函数
`imr`。假设数据分散在多个节点上，我们想计算所有节点之间的变量的中位数。首先，对于每个数据源，将数据放入桶中，并使用 map
函数对每个数据桶中的数据点数进行计数。然后使用 reduce
函数来合并来自多个数据源的计数。找到包含中位数的桶。在下一次迭代中，所选择的桶分为更小的桶。当所选择的桶的长度不超过指定的数量时，迭代就完成了。

```
def medMap(data, range, colName){
 return bucketCount(data[colName], double(range), 1024, true)
}

def medFinal(range, result){
   x= result.cumsum()
   index = x.asof(x[1025]/2.0)
   ranges = range[1] - range[0]
   if(index == -1)
      return (range[0] - ranges*32):range[1]
   else if(index == 1024)
      return range[0]:(range[1] + ranges*32)
   else{
      interval = ranges / 1024.0
      startValue = range[0] + (index - 1) * interval
      return startValue : (startValue + interval)
   }
}

def medEx(ds, colName, range, precision){
   termFunc = def(prev, cur): cur[1] - cur[0] <= precision
   return imr(ds, range, medMap{,,colName}, +, medFinal, termFunc).avg()
}
```

