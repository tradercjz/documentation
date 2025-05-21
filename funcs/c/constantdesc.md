# constantDesc

## 语法

`constantDesc(obj)`

## 参数

**obj** 一个对象。

## 详情

返回一个字典，描述对象 *obj* 的相关属性。字典可能包含的 key 及说明如下：

| key | 说明 |
| --- | --- |
| form | 数据形式 |
| vectorType | 向量类型，仅当 *obj* 是向量时才有此 key |
| isIndexedMatrix | 是否是索引矩阵，仅当 obj 是矩阵时才有此 key |
| isIndexedSeries | 是否是索引序列，仅当 obj 是矩阵时才有此 key |
| nullFlag | 是否存在 NULL 值，仅当 *obj* 是向量、数据对或矩阵时才有此 key |
| isView | 是否是视图，仅当 *obj* 是向量、数据对或矩阵时才有此 key |
| tableType | 表的类型，仅当 obj 是表时才有此 key |
| type | 数据类型 |
| codeType | 元代码的类型，仅当 obj 是元代码时才有此 key |
| functionDefType | 函数类型，仅当 obj 是函数是才有此 key |
| scale | 保留的小数位数，仅当 obj 是 DECIMAL 类型数据时才有此 key |
| isColumnarTuple | 是否是列式元组，仅当 obj 是元组且不是视图时才有此 key |
| category | 数据类型分类 |
| isTemporary | 是否是临时对象 |
| isIndependent | 是否独立对象 |
| isReadonly | 是否只读对象 |
| isReadonlyArgument | 是否是只读参数 |
| isStatic | 是否是静态对象 |
| isTransient | 是否是瞬态对象 |
| copyOnWrite | 是否写时拷贝 |
| refCount | 被引用的次数 |
| address | 地址的十六进制表示 |
| rows | 包含行数 |
| columns | 包含列数 |
| memoryAllocated | 已分配的内存 |

## 例子

```
t = table(1..3 as id, 4..6 as val)
constantDesc(t)
/*
form->TABLE
tableType->BASIC
type->DICTIONARY
category->MIXED
isTemporary->false
isIndependent->true
isReadonly->false
isReadonlyArgument->false
isStatic->false
isTransient->false
copyOnWrite->false
refCount->1
address->0000000028d2d1e0
rows->3
columns->2
memoryAllocated->208
*/

constantDesc(lj)
/*
form->SCALAR
type->FUNCTIONDEF
functionDefType->SYSTEM FUNCTION
category->SYSTEM
isTemporary->true
isIndependent->true
isReadonly->false
isReadonlyArgument->false
isStatic->false
isTransient->false
copyOnWrite->false
refCount->6
address->000000000cabce00
rows->1
columns->1
memoryAllocated->10
*/
```

