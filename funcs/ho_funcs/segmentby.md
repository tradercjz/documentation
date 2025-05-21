# segmentby

## 语法

`segmentby(func, funcArgs, segment)`

## 详情

根据 *segment* 参数确定分组方案，把 *funcArgs* 分组，并把函数 *func*
应用到每个分组中。返回的结果与 *segment* 参数的长度相同。

## 参数

* **func** 是一个函数。
* **funcArgs** 是函数的参数。
* **segment** 是分组向量。segment参数中连续相同的元素为一组。segment的长度必须和funcArgs相同。

## 例子

下面的例子中，y确定了3个分组：1 1 1、-1 -1 -1和1 1
1。第一个分组的index是0-2，第二个分组的index是3-5，第三个分组的index是6-9。按照这个规则把x分成3组，1 2 3、0 3 2和1 4 5，并把
[cumsum](../c/cumsum.md) 函数应用到x的每个分组，计算每个分组的累计和。

```
x=1 2 3 0 3 2 1 4 5
y=1 1 1 -1 -1 -1 1 1 1
segmentby(cumsum,x,y);
// output
[1,3,6,0,3,5,1,5,10]
```

*segmentby*
可用于止损回测。下面的例子把回报率ret分为两组，分别判断position=1和position=-1这两种情况下，是否需要止损。

```
def stoploss(ret, threshold){
     cumret = cumprod(1+ret)
     drawDown = cumret.cummax() / cumret - 1
     firstCutIndex = at(drawDown >= threshold).first() + 1
     indicator = take(false, ret.size())
     if(isValid(firstCutIndex) and firstCutIndex < ret.size())
         indicator[firstCutIndex:] = true
     return indicator
}
position = 1 1 1 1 1 -1 -1 -1 -1
ret = 0.01 0.02 -0.04 -0.02 -0.01 -0.005 -0.015 0.005 0.025
segmentby(stoploss{,0.05}, ret, position);
// output
[false,false,false,false,true,false,false,false,false]
```

