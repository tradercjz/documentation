# isort!

## 语法

`isort!(X, [ascending=true], indices)`

## 参数

**X** 是一个向量或一个由多个等长向量组成的元组。

**ascending** 是布尔值，表示按升序排序还是按降序排序。默认值为 true（按升序排序）。

**indices** 是一个向量，它的长度与 *X* 中每个向量的长度相同。

## 详情

isort!(x, ascending, y) 相当于 y[isort(x, ascending)]，结果会赋给 y。

## 例子

```
x=3 1 NULL 2
y=5 7 8 3
isort!(x, false, y);
// output
[5, 3, 7, 8]
// 排序后的x为[3, 2, 1, NULL]，第一个元素3与y中的5对应，第二个元素与2与y中的3对应，第三个元素1与y中的7对应，...以此类推。

x=2 2 1 1
y=2 1 1 2
isort!([x,y],[1,0],5 4 3 2);
// output
[2,3,5,4]
```

