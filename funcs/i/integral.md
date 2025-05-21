# integral

## 语法

`integral(func, start, end, [start2], [end2])`

## 参数

**func** 是一元或二元函数。

**start** 是一个数值标量或向量，表示开始值。*start* 用 NULL 值表示负无穷。

**end** 是一个数值标量或向量，表示结束值。*end* 用 NULL 值表示正无穷。

**start2** 是一个数值标量，向量或一元函数，表示二重积分第二维度的开始值。*start2* 用 NULL 值表示负无穷。

**end2** 是一个数值标量，向量或一元函数，表示二重积分第二维度的结束值。*end2* 用 NULL 值表示正无穷。

如果 *start* 和 *end* 都是向量，或需要计算二重积分时，*start*, *end* , *start2*
和 *end2* 为向量，则它们的长度必须相同。如果部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。

## 详情

返回 *func* 在 *start* 和 *end* 范围内的积分，或在平面区域
*start* ≤ x ≤ *end* 和 *start2* ≤ y ≤ *end2* 上 *func*
的积分。

当结果中出现无穷值或者计算过程中出现有关复数的计算时会返回 NULL。

## 例子

```
integral(abs, -10, 10);
// output
100

integral(acos, [0.1, -0.10], [0.3, 0.10]);
// output
[0.273816,0.314159]

integral(acosh, [1, 2, 9, 9], 10);
// output
[19.982354,19.080489,2.941187,2.941187]

integral(pow{,3}, 5, 9);
// output
1484

integral(abs, NULL, NULL);
// output
00F

def f(x1,x2){
   fx=100*(x2-x1*2)+square(1-x1)
   return fx
}

integral(f,0,1,7,1)
// output
-1802

integral(f,[0,1,2,3],7,2,[0,1,2,3])
// output
[8255.333333, 8256, 7856.666667, 7061.333333]
```

