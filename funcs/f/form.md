# form

## 语法

`form(X)`

## 参数

**X** 是一个任意的变量或常数。

## 详情

生成变量或常数的数据形式标识符（data form ID）。数据形式标识符和对应的数据形式为：0: 标量; 1: 向量; 2:
数据对; 3: 矩阵; 4: 集合; 5: 字典; 6: 表; 10: tensor。

## 例子

```
form(false);
// output
0

form(`TEST);
// output
0

form(`t1`t2`t3);
// output
1

form(1 2 3);
// output
1

x= 1 2 3
if(form(x) == VECTOR){y=1}
y;
// output
1

form(1..6$2:3);
// output
3
```

