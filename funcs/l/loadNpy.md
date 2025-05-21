# loadNpy

## 语法

`loadNpy(fileName)`

## 参数

**filename** 是字符串，表示 npy 文件的路径。

## 详情

读取 Python Numpy 的 npy 格式二进制文件，并转化为 DolphinDB 的向量或矩阵。Numpy 对象中的 NaN 值会被转化为 DolphinDB 的
NULL 值。

## 例子

在 Python 中导出 npy 格式文件：

```
import numpy as np
np.save("intVec.npy", np.array([5,6,1,3,4,8]))
np.save("doubleMat.npy", np.array([[1.5,5.6,-7.87],[-1.0,3.4,4.5]]))
```

在 DolphinDB 中加载 npy 文件：

```
loadNpy("intVec.npy");
```

输出返回：[5,6,1,3,4,8]

```
loadNpy("doubleMat.npy");
```

输出返回：

| #0 | #1 | #2 |
| --- | --- | --- |
| 1.5 | 5.6 | -7.87 |
| -1 | 3.4 | 4.5 |

相关函数：[saveAsNpy](../s/saveAsNpy.html)

