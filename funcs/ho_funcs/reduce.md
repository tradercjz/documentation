# reduce

## 语法

`reduce(func, X, [init], [assembleRule|consistent=false])`

`reduce:T(X, [init])` 或 `[init] <operator>:T X`
表示不指定 *assembleRule*，使用默认值

`reduce:TC(X, [init])` 或 `[init] <operator>:TC X`
表示指定 *assembleRule*，此例中指定为 C（Consistent）

## 参数

* **func** 函数。
  + 当 *func* 是一元函数时，*X*
    可以是非负整数、一元函数或空值。*init* 表示 *func* 的参数，必须指定。
  + *func* 是二元函数时，*X* 是向量、矩阵或表。*init*
    表示初始值。
  + *func* 是三元函数时，*X* 必须是一个
    Tuple，包含2个元素，分别表示 *func* 的后两个参数。
* **assembleRule** 可选参数，表示如何将子任务的结果合并为函数最终结果。接受一个整数或字符串作为输入，可选值如下：
  + 0 （或 "D"）：默认值，表示 DolphinDB
    规则，即根据所有子任务的结果来决定最终输出的数据类型和形式。当所有子结果具有相同的数据类型和形式时，多个标量合并为一个向量、多个向量合并为一个矩阵、多个矩阵合并为一个元组、多个字典合并为一张表；否则将所有子结果合并为一个元组输出。
  + 1（或 "C"）：表示 Consistent
    规则，即认为所有子结果的数据类型和形式都与第一个子结果相同，根据第一个子结果来选择最终结果的数据类型和形式。如果后续子任务返回的结果与第一个子任务的结果类型不一致，系统会尝试对后续结果进行类型转换。如果转换失败则抛出异常。因此，此规则只可在已知子结果的数据类型及形式一致时指定。此规则可使系统免于逐一缓存并检查每个子任务的计算结果，从而提升性能。
  + 2（或 "U"）：表示 Tuple 规则，系统不再对各子结果的类型和形式一致性进行检查，而是直接将子结果组装成一个元组输出。
  + 3（或 "K"）：表示 kdb+ 规则。与 DolphinDB 规则类似，都会根据所有子结果来决定最终结果形式。主要区别在于，kdb+
    规则下，只要有任一子任务返回向量，则最终结果必为一个元组；而在 DolphinDB
    规则下，子任务结果若均为长度相同的向量，则最终结果为一个矩阵。其他情况下，kdb+ 规则的输出与 DolphinDB 规则相同。

  注：
  + 自 2.00.15/3.00.3 版本起，新增了
    *assembleRule* 参数。该参数不仅实现了原 *consistent*
    参数的功能，还提供了更多的结果合并选项。*consistent* 是一个布尔值，默认值为 false，相当于
    *assembleRule*="D"；若为 true，则相当于
    *assembleRule*="C"。为保持兼容性，用户仍可使用 *consistent* 参数。如果同时指定
    *assemble* 和 *consistent*，将以 *consistent*
    的值为准。
  + *assembleRule* 也可在高阶函数对应的函数模式符号后指定，通过字符 D/C/U/K 表示。以
    `eachPre (:P)` 为例，形如
    `sub:PU(X)`。不指定则使用默认值 D。

## 详情

该函数与 `accumulate`
的功能相同，唯一区别是返回值不同。`reduce` 返回最后一个结果，而 `accumulate`
输出所有中间结果。关于函数功能描述，参见  [accumulate](accumulate.html)。

`reduce` 等同于以下伪代码的执行过程：

```
result=<function>(init,X[0]);

for(i:1~size(X)){

result=<function>(result, X[i]);

}

return result;
```

## 例子

*func* 是一元函数时：

通过以下方式定义一个一元函数：

```
def func1(x){
  if(x<5){
          return x*3
  }
  else{
          return x+3
  }
}
```

当 X 为整数时，迭代 X 次，输出最后一个结果：

```
reduce(func1, 5, 1)
```

返回：18

当 X 为一元函数 condition 时，第3次迭代时因 condition 返回false，停止迭代2次后停止，并输出最后一个结果。

```
def condition(x){
  return x<9
}
reduce(func1, condition, 1)
```

返回：9

当 X 为 NULL（或不指定）时，自定义函数 func2 作为进行迭代的函数。

```
def func2(x){
  if(x<5){
          return x*3
  }
  else{
          return 6
  }
}

//因第4次迭代结果和第3次相同，停止迭代并输出最后一个结果。
reduce(func2,NULL,1)
```

返回：6

*func* 是二元函数时，在一个向量上执行 `reduce`：

```
reduce(mul, 1..10);
```

返回：3628800，即 10 的阶乘。上例如果由 `accumulate` 高阶函数实现，则是：

```
*:A 1..10;
```

返回：[1,2,6,24,120,720,5040,40320,362880,3628800]

```
2 *:T 1..10;
```

返回：7257600

```
def f1(a,b):a+log(b);
reduce(f1, 1..5, 0);
```

返回：4.787492

对一个矩阵执行 `reduce`：

```
x=1..12$3:4;
x;
```

得到：

| col1 | col2 | col3 | col4 |
| --- | --- | --- | --- |
| 1 | 4 | 7 | 10 |
| 2 | 5 | 8 | 11 |
| 3 | 6 | 9 | 12 |

```
+ :T x;
```

返回：[22,26,30]

*func* 是三元函数时：

```
def fun3(x,y,z){
  return x+y+z
}
reduce(fun3,[[1,2,3],[10,10,10]],5)
```

返回：41

