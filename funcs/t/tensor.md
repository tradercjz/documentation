# tensor

## 语法

`tensor(X)`

## 参数

**X** 可以是标量、向量、元组、列式元组、矩阵或表。目前仅支持以下数据类型：BOOL, CHAR, SHORT, INT, LONG, FLOAT,
DOUBLE。

## 详情

将 *X* 转换为一个 tensor。转换规则如下：

| **X** | **转换结果** |
| --- | --- |
| 标量 | 1 维 tensor |
| 常规向量 | 1 维 tensor |
| 列式元组 | 2 维 tensor |
| 矩阵 | 2 维 tensor |
| 表（每一列具有相同类型） | 2 维 tensor |
| tuple（每个元素都是具有相同类型的向量，tuple of vector） | 2 维 tensor |
| tuple（每个元素都是维度和类型都相同的矩阵，tuple of matrix） | 3 维 tensor |
| tuple（每个元素都是 tuple，且子 tuple 的每个元素都是类型相同的向量，tuple of tuple） | 3 维 tensor |
| 多个 tuple 嵌套 | n 维 tensor，n<=10 |

目前 tensor 主要应用于 DolphinDB 插件（如 LibTorch 等），与深度学习框架进行数据交换。DolphinDB 中的 tensor
目前暂不支持直接存储和计算，并且不支持直接访问和修改其元素。

## 例子

```
// 标量转为 tensor
tensor(3)
/* 输出一个长度为 1 的 1 维 tensor<int[1]>:
0: int 3
*/

// 向量转为 tensor
tensor(1 2 3)
/* 输出一个长度为 3 的 1 维 tensor<int[3]>：
0: int 1
1: int 2
2: int 3
*/

//列式元组转为 tensor
tp = [[1.3,2.5,2.3], [4.1,5.3,5], [4.1,5.3,5]]
tp.setColumnarTuple!()
tensor(tp)

/* 输出一个 2 维 tensor<double[3][3]>：
0: double[3] [1.3, 2.5, 2.3]
1: double[3] [4.1, 5.3, 5]
2: double[3] [4.1, 5.3, 5]
 */

//矩阵转为 tensor
m= 1..6$2:3
tensor(m)

/* 输出一个 2 维 tensor<int[2][3]>：
0: int[3] [1, 3, 5]
1: int[3] [2, 4, 6]
*/

// 表转为 tensor
t=table(1..5 as id1, 6..10 as id2)
tensor(t)

/* 输出一个 2 维 tensor<int[5][2]>：
0: int[2] [1, 6]
1: int[2] [2, 7]
2: int[2] [3, 8]
3: int[2] [4, 9]
4: int[2] [5, 10]
*/

// 元组转为 tensor
tp1 = [[1.3,2.5,2.3], [4.1,5.3,5], [4.1,5.3,5]]
tensor(tp1)

/* 输出一个 2 维 tensor<double[3][3]>：
0: double[3] [1.3, 4.1, 4.1]
1: double[3] [2.5, 5.3, 5.3]
2: double[3] [2.3, 5, 5]
*/

// tuple of matrix 转为 tensor
m1= 1..6$2:3
m2=4..9$2:3
tensor([m1,m2])

/* 输出一个 3 维 tensor<int[2][2][3]>:
0: int[2][3]
1: int[2][3]
*/

// tuple of tuple 转为 tensor
tp1 = [[1.3,2.5,2.3], [4.1,5.3,5], [4.1,5.3,5]]
tp2 = [[1.1,1.2,1.4], [1.5,1.2,1.6], [1.3,1.5,1.8]]
tensor([tp1, tp2])

/* 输出一个 3 维 tensor<double[2][3][3]>:
0: double[3][3]
1: double[3][3]
*/

// tuple 嵌套转为 tensor
tp1 = [[1.3,2.5,2.3], [4.1,5.3,5], [4.1,5.3,5]]
tp2 = [[1.1,1.2,1.4], [1.5,1.2,1.6], [1.3,1.5,1.8]]
tp3 = [[2.1,6.2,4.4], [3.5,1.9,3.6], [1.8,3.5,9.8]]
tensor([[tp1, tp2],[tp1, tp3]])

/* 输出一个 4 维 tensor<double[2][2][3][3]>:
0: double[2][3][3]
1: double[2][3][3]
*/
```

