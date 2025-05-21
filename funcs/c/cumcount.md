# cumcount

## 语法

`cumcount(X)`

参数说明和窗口计算规则请参考: [累计窗口系列（cum 系列）](../themes/cumFunctions.md)

## 详情

计算 *X* 中累积非 NULL 的元素数量。

## 例子

```
x=[1,2,NULL,3,4,NULL,5,6]
cumcount(x);
// output
[1,2,2,3,4,4,5,6]

m=matrix(1 2 3 NULL 4, 5 6 NULL NULL 8);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 5 |
| 2 | 6 |
| 3 |  |
|  |  |
| 4 | 8 |

```
cumcount(m);
```

| #0 | #1 |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 3 | 2 |
| 4 | 3 |

相关函数：[count](count.md)

