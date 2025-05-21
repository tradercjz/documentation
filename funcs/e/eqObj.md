# eqObj

## 语法

`eqObj(obj1, obj2, [precision])`

## 参数

**obj1** 和 **obj2** 可以是标量、数据对、向量或矩阵。

**precision** 是一个非负整数，表示对 FLOAT 或 DOUBLE 类型，比较精度为小数点后几位。

## 详情

检验两个对象的类型和值是否相同。只有当类型和值都相同时，此函数才会返回 true。 如果值相同但类型不同，则此函数仍返回
false，这与函数 [eq](eq.md) 不同。

注： 使用
`eqObj` 比较浮点数时，根据 abs(obj1-obj2)<=pow(10,-precision)
的结果来判断 obj1 和 obj2 的值是否相等。

## 例子

```
eqObj(2, 2.0);
// output: false

eq(2, 2.0);
// output: true

eqObj(1.1, 1.2, 0);
// output: true

eqObj(1.1, 1.2, 1);
// output: true

eqObj(1 2 3, 1 2 3);
// output: true

eq(1 2 3, 1 2 3);
// output: [true,true,true]
```

`eqObj` 不能直接用于比较两个表是否相同。但是，可以使用高阶函数 [each](../ho_funcs/each.md) 来逐列对比两个表的值。

```
t1=table(1 2 3 as x, 4 5 6 as y);
t2=table(1 2 3 as x, 4 5 6 as y);

t1.values();
// output: ([1,2,3],[4,5,6])

each(eqObj, t1.values(), t2.values());
// output: [true,true]
```

