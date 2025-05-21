# memberModify!

## 语法

`memberModify!(obj, function, indices, parameters)`

## 详情

修改元组或 ANY 字典的成员对象，也可修改面向对象的编程（OOP）中的对象。

## 参数

**obj** 一个元组或值为 ANY 类型的字典，或者一个 OOP 对象。

**function**一个内置的系统函数，该函数的第一个参数是可修改的，例如 append!。

**indices** 标量、向量或元组，表示指向一个或多个成员对象的索引或键值。

* 若是一个元组，用于表示多维度索引。元组的长度表示索引的深度。
* 若是一个向量，表示对多个成员进行修改。

**parameters**
*function* 除第一个参数外的其它参数。*parameters* 的维度必须与 *indices*,
*function* 的参数个数匹配。

## 例子

### 例 1

创建元组 a，修改其中的一个元素，可见前后对比。

```
a = (1 2, 3 4 5)
memberModify!(a, append!, 0, 3 4)
a
//output: a = (1 2 3 4, 3 4 5)
```

创建字典
d，修改其中的两个元素，可见前后对比。

```
d = dict(`A`B`C, (1 2, 3 4, 5 6))
d
/*output:
A->[1,2]
B->[3,4]
C->[5,6]
*/

d.memberModify!(append!,`A`B, 3 4)
d
/*output:
A->[1,2,3]
B->[3,4,4]
C->[5,6]
 */
```

创建元组 c，其包含基于表 t，字典 d
和一个元组。

```
t = table(1 2 3 as val1, 4 5 6 as val2)
d = dict(`A`B`C, (1 2, 3 4, 5 6))
c = (t, d, [1 2 3, 4 5 6])
c
/*output:
(val1 val2
---- ----
1    4
2    5
3    6
,C->[5,6]
A->[1,2]
B->[3,4]
,([1,2,3],[4,5,6]))
*/
```

调用 `memberModify!` 对元组第 3 个元素 `[1 2 3, 4 5 6]` 的第 1
个元素 [1, 2, 3] 添加元素 4 和 5。要修改的对象需要用两个维度来指定，因此 indices 使用元组 (2, 0)
来表示。

```
c.memberModify!(append!, (2, 0), 4 5)
/*output:
(val1 val2
---- ----
1    4
2    5
3    6
,C->[5,6]
A->[1,2]
B->[3,4]
,([1,2,3,4,5],[4,5,6]))
*/
```

在该基础上，继续向元组的第 2 个元素（字典）的键值 B 指定的对象写入新数据 5 和 7。indices 仍然使用元组 （1，`B)
来表示。

```
c.memberModify!(append!, (1,`B), 5 7)
c
/*output:
(val1 val2
---- ----
1    4
2    5
3    6
,C->[5,6]
A->[1,2]
B->[3,4,5,7]
,([1,2,3,4,5],[4,5,6]))
*/
```

### 例 2

约定名为 A 的类并进行实例化，使用 `memberModify!` 进行写入操作，打印向量 a 的数据，可得预期结果。

```
class A {
	a :: INT VECTOR
	def A() {
		a = []
	}
}

v = A()
memberModify!(v, append!, "a", 1)
print v.a
//output: [1]

memberModify!(v, append!, "a", 11)
print v.a
//output: [1,11]
```

