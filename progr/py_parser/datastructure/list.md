# 列表

## 创建列表

```
s = [10, "math", 2022.01.01T09:10:01, [97c, 22l, 3.5f]]
type(s)
// output: list
```

## 访问列表中的值

1. 使用下标直接访问某个元素；

   ```
   s[3]
   // output: [a, 22, 3.5]

   s[-2]
   // output: 2022.01.01T09:10:01
   ```
2. 通过 slice 的方式访问列表中的元素。注意：暂不支持 step 参数。

   ```
   s[1:4]
   // output: ['math', 2022.01.01T09:10:01, [a, 22, 3.5]]

   s[2:]
   // output: [2022.01.01T09:10:01, [a, 22, 3.5]]
   ```

## 更新列表

1. 更新数据

   ```
   s[1]="english"
   // output: [10, 'english', 2022.01.01T09:10:01, [a, 22, 3.5]]

   # 嵌套 list 不支持直接通过多层索引更新内部的值
   s[3][1] = 21 # unsupported
   # 改写为：
   tmp = s[3]
   tmp[1] = 21
   s
   // output: [10, 'english', 2022.01.01T09:10:01, [a, 21, 3.5]]
   ```
2. 追加数据

   ```
   s.append(2020.01.01)
   // output: [10, 'english', 2022.01.01T09:10:01, [a, 21, 3.5], 2020.01.01]
   s.insert(0, 13:30m)
   // output: [13:30m, 10, 'english', 2022.01.01T09:10:01, [a, 21, 3.5], 2020.01.01]
   ```

## 删除列表元素

Python Parser 暂不支持 `del` 。

```
s.pop()  # 根据索引值删除元素，默认删除最后一个元素。也可通过指定索引删除对应位置的元素。
// output: 2020.01.01
s
// output: [13:30m, 10, 'english', 2022.01.01T09:10:01, [a, 21, 3.5]]

s.remove(13:30m) # 根据元素值进行删除
s
// output: [10, 'english', 2022.01.01T09:10:01, [a, 21, 3.5]]

s.clear()  # 删除列表所有元素
// output: []
```

## 列表可用的所有属性和方法

```
dir(s)
// output: ['__add__', '__dir__', '__eq__', '__getitem__', '__iadd__', '__imul__', '__init__', '__iter__', '__len__', '__mul__', '__ne__', '__repr__', '__req__', '__rne__', '__str__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort', 'toddb']
```

其中 `toddb` 是 Python Parser 中特有的方法，它支持将 Python Parser 的列表对象转换成 DolphinDB 的向量（常规向量、元组）。

```
s = [1, 2, 3]
type(s.toddb())
// output: dolphindb.VECTOR.INT

s = [[1, 2], `A, 3.2]
type(s.toddb())
// output: dolphindb.VECTOR.ANY
```

## 列表支持的操作符

| 操作符 | 含义 | 表达式 | 结果 |
| --- | --- | --- | --- |
| \* | 重复列表 | [1, 2, 3] \* 3 | [1, 2, 3, 1, 2, 3, 1, 2, 3] |
| + | 拼接列表 | [1, 2022.01M, 3] + [4, 5, "banana"] | [1, 2022.01M, 3, 4, 5, 'banana'] |

