# acf

## 语法

`acf(X, maxLag)`

## 参数

**X** 是一个向量。

## 详情

计算 *X* 的1阶至 *maxLag* 阶的自相关系数。

## 例子

```
n=10000
x=array(DOUBLE, n, n, NULL)
x[0]=1
r=rand(0.05, n)-0.025
for(i in 0:(n-1)){
   x[i+1]=-0.8*x[i]+r[i]
}

acf = acf(x, 20)
plot(acf,chartType=BAR)
```

相关函数： [autocorr](autocorr.md)

