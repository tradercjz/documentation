# all

## 语法

`all(X)`

## 参数

**X** 可以是标量、数据对、向量或矩阵。

## 详情

如果 *X* 中包含 false 或0，返回 false；反之返回 true。NULL 值不参与计算。

## 例子

```
all(1 2 3)
// output
1

all(0 1 2)
// output
0

all(true false)
// output
0

all(true true true)
// output
1

all(1..10$2:5)
// output
1

all(0..9$2:5);
// output
0
```

相关函数：[any](any.html)

