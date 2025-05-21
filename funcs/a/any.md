# any

## 语法

`any(X)`

## 参数

**X** 可以是标量、数据对、向量或矩阵。

## 详情

如果 *X* 中有至少一个元素为 true 或非0，则返回 1；否则返回 0。NULL 值不参与计算。

## 例子

```
any(1 0 2)
// output
1
any(0 0 0)
// output
0
any(0 0 NULL)
// output
0

any(true false)
// output
1
any(false false)
// output
0

any(0..9$2:5)
// output
1
```

相关函数：[all](all.html)

