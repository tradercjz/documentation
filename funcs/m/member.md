# member

## 语法

`member(X, Y)` 或 `X.Y`

## 参数

**X** 可以是表或字典。

**Y** 是 *X* 的一个成员或属性。若使用 member(X, Y) 方式，*Y*
必须是字符串。

## 详情

返回对象的指定成员/属性。

## 例子

```
x=1 2 3
y=4 5 6
t=table(x,y);

t.x;
// output
[1,2,3]
t.y;
// output
[4,5,6]

t.rows();
// output
3
t.cols();
// output
2
t.size();
// output
3
// 表的 size 定义为它的行数

d = dict(1 2 3, 4 5 6);
d;
// output
3->6
1->4
2->5

d.2;
// output
5
```

