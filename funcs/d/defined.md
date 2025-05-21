# defined

## 语法

`defined(names, [type=VAR])`

## 参数

**names** 可以是字符串标量或向量，表示对象名。

**type** 可为 VAR（本地变量），SHARED（共享变量）或 DEF（函数定义）。默认值为 VAR。

## 详情

返回一个标量/向量，表示 *names* 中的每个元素是否已被定义。

## 例子

```
x=10
y=20
def f(a){return a+1}
share table(1..3 as x, 4..6 as y) as t1;

defined(["x","y","f",`t1]);
// output
[1,1,0,0]

defined(["x","y","f",`t1], DEF);
// output
[0,0,1,0]

defined(["x","y","f",`t1], SHARED);
// output
[0,0,0,1]
```

