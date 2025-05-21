# find

## 语法

`find(X, Y)`

## 参数

**X** 可以是向量、字典、单列内存表、键值表或者索引内存表。

**Y** 可以是标量、向量、数组向量、元组、字典、矩阵、表。

## 详情

* 若 *X* 是向量，对 *Y* 中每一个元素，返回其第一次出现在 *X*
  中的位置；如果没有在X中出现，返回 -1。若要查找所有出现的位置，可使用 [at](../a/at.md) 函数
  。
* 若 *X* 是字典，对 *Y* 中每一个元素，若其为 *X* 的键，返回
  *X* 中对应的值；若不是 *X* 的键，返回 NULL。
* 若 *X* 是单列内存表，对 *Y* 中每一个元素，返回其第一次出现在 *X*
  的唯一列中的位置；如果没有在 *X* 的唯一列中出现，返回-1。注意：表中单列的类型不能是
  Array Vector。
* 若 *X* 是键值内存表或索引内存表，对 *Y* 中每一个元素，返回其第一次出现在
  *X* 的主键中的位置； 如果没有在 *X* 的主键中出现，返回 -1。

通过 `find`
函数，用一个大向量搜索另一个大向量时，系统将建立一个字典，用以优化性能。但如果只是用几个值搜索一个向量，系统可能不会为了优化性能建立字典。是否建立字典是动态决定的。如果需要在已经排序的向量中搜索少量数据，我们推荐使用
[binsrch](../b/binsrch.md) 函数。

## 例子

*X* 是向量：

```
find(7 3 3 5, 3);
// output
1

at(7 3 3 5 == 3);
// output
[1,2]

(7 3 3 5 6).find(2 4 5);
// output
[-1,-1,3]
```

*X* 是字典：

```
z=dict(1 2 3,4.5 6.6 3.2);
z;
// output
3->3.2
1->4.5
2->6.6

find(z,3);
// output
3.2

find(z,5);
// output
00F
```

*X* 是单列内存表：

```
t = table(1 3 5 7 9 as id)
find(t, 2 3)
// output
[-1,1]
```

*X* 是键值表或者索引内存表：

```
kt = keyedTable(`name`id,1000:0,`name`id`age`department,[STRING,INT,INT,STRING])
insert into kt values(`Tom`Sam`Cindy`Emma`Nick, 1 2 3 4 5, 30 35 32 25 30, `IT`Finance`HR`HR`IT)
find(kt,(`Emma`Sam, 4 1));
// output
[3,-1]

t1 = indexedTable(`sym`side, 10000:0, `sym`side`price`qty, [SYMBOL,CHAR,DOUBLE,INT])
insert into t1 values(`IBM`MSFT`GOOG, ['B','S','B'], 10.01 10.02 10.03, 10 10 20)
find(t1, (`GOOG`MSFT, ['B','S']))
// output
[2,1]
```

