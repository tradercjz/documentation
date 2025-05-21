# objectChecksum

## 语法

`objectChecksum(vector, [prev])`

## 参数

**vector** 向量。用于进行校验和（checksum）计算。

**prev** 整数。当 *vector* 过长时，可以通过指定 *prev* 分段迭代求完整的校验和，*prev*
表示迭代时前一段数据的校验和。

## 详情

计算向量的校验和，返回一个整数。通常用于校验数据的完整性。

## 例子

```
print objectChecksum(take(`A`B`C, 10))
// output
-268298654

print objectChecksum(2.3 6.5 7.8)
// output
-430996932

// 分段计算校验和
print objectChecksum(1..15)
// output
-1877567753

t0 = objectChecksum(1..5)
t1 = objectChecksum(6..10, t0)
t2 = objectChecksum(11..15, t1)
print t2
// output
-1877567753
```

