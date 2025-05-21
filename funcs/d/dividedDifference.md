# dividedDifference

## 语法

`dividedDifference(X, Y, resampleRule, [closed='left'], [origin='start_day'],
[outputX=false])`

## 详情

该函数根据 *resampleRule*, *closed*, *origin* 确定的采样规则，对
*X* 进行重采样操作。并根据重采样后的 *X*，对 *Y* 进行均差插值（DividedDifference
Interpolation）。

若不指定 *outputX*，仅返回一个对 *Y* 插值后的向量。若指定 *outputX* =
true，则返回一个 tuple，其第一个元素为 *X* 重采样后的向量，第二个元素为对 *Y* 插值后的向量。

## 参数

**X** 严格递增的时间类型向量。

**Y** 同 *X* 等长的数值型向量。

**resampleRule** 一个字符串，可选值请参考 [resample](../r/resample.html) 的
*rule* 参数。

**closed** 和 **origin** 同 [resample](../r/resample.html) 的
*closed* 和 *origin* 参数。

**outputX** 布尔类型，表示是否输出 *X* 按照 *resampleRule*, *closed*,
*origin* 重采样后的向量。默认值为 false。

## 例子

```
dividedDifference([2016.02.14 00:00:00, 2016.02.15 00:00:00, 2016.02.16 00:00:00], [1.0, 2.0, 4.0], resampleRule=`60min);

// output
[1,1.0217,1.0451,1.0703,1.0972,1.1259,1.1562,1.1884,1.2222,1.2578,
1.2951,1.3342,1.375,1.4175,1.4618,1.5078,1.5556,1.605,1.6562,1.7092,
1.7639,1.8203,1.8785,1.9384,2,2.0634,2.1285,2.1953,2.2639,2.3342,
2.4062,2.48,2.5556,2.6328,2.7118,2.7925,2.875,2.9592,3.0451,3.1328,
3.2222,3.3134,3.4062,3.5009,3.5972,3.6953,3.7951,3.8967,4]
```

