# randF

## 语法

`randF(numeratorDF, denominatorDF, count)`

## 参数

**numeratorDF** 和 **denominatorDF** 都是正数，表示 F 分布的自由度。

**count** 是正整数，表示生成的随机数个数。

## 详情

生成指定个数的 F 分布随机数。

## 例子

```
randF(2.31, 0.671, 2);
// output
[0.41508, 0.642609]
```

