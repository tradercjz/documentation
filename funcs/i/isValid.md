# isValid

## 语法

`isValid(X)`

## 参数

**X** 可以是标量、数据对、向量或矩阵。

## 详情

检查每个元素是否为有效数（非 NULL 值）。如果是，返回 true；否则返回 false。

## 例子

```
isValid(00i);
// output
false

isValid(1 NULL NULL 6 NULL 7);
// output
[true,false,false,true,false,true]

isValid(1/0);
// output
false
```

