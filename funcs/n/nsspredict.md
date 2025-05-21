# nssPredict

## 语法

`nssPredict(model, maturity)`

## 参数

**model** 字典类型，表示 Nelson-Siegel（NS） 模型或 Nelson-Siegel-Svensson（NSS）模型。字典中应至少包含
*modelName* 和 *params* 两个成员：

* modelName 字符串类型，必须为 “ns” 或 “nss” 。
* params 数值型向量，表示模型的参数：

  + 对于 NS 模型，向量长度为 4，依次为 β0, β1,
    β2, λ 。
  + 对于 NSS 模型，向量长度为 6，依次为 β0, β1,
    β2, β3,
    λ0, λ1。

**maturity** 值大于 0 的数值型向量，表示历史债券的到期时间，单位是年。

## 详情

根据指定的 NS 模型或 NSS 模型，预测债券的收益率。

## 例子

```
model = dict(STRING, ANY)
model[`modelName] = `nss
model[`params] = [0.038184469794996,-0.048575389082029,-0.022287414169806,0.047523360012739,1.873046195772644,0.161159907274023]
maturity = [3,1]
nssPredict(model, maturity)
//output: [0.009904201306,0.003891991292041]
```

相关函数：[nss](nss.md)

