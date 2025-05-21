# autocorr

## 语法

`autocorr(X, lag)`

## 参数

**X** 是一个向量。

**lag** 是一个正整数。

## 详情

计算 *X* 的 *lag* 阶自相关系数。请注意，计算时两个时间序列所用的均值均为 *X*的均值，而非两个时间序列各自的均值。

## 例子

```
n=10000
x=array(DOUBLE, n, n, NULL)
x[0]=1
r=rand(0.05, n)-0.025
for(i in 0:(n-1)){
    x[i+1]=-0.8*x[i]+r[i]
}

autocorr(x, 1)
// output
-0.808343

autocorr(x, 2)
// output
0.661018
```

相关函数： [acf](acf.html)

