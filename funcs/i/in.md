# in

## 语法

`in(X, Y)`

## 参数

**X** 可以是标量、向量、元组、矩阵、数组向量、字典、表。

**Y** 可以是标量、向量、字典、单列内存表、键值内存表或索引内存表。

## 详情

* 若 *Y* 是非时间类型的标量，检查 *X* 和 *Y* 是否相等；若 *Y* 是时间类型的标量，则会检查
  *X* 中的每个元素是否在 *Y* 中。当 *Y* 是 NULL 值时，无论 *X* 为何值都返回
  false。
* 若 *Y* 是向量，检查 *X* 中的每一个元素是否在 *Y* 中。
* 若 *Y* 是字典，检查 *X* 中的每一个元素是否是 *Y* 中的键。
* 若 *Y* 是单列内存表，检查 *X* 中的每一个元素是否是 *Y*
  唯一列中的值。

  注： 表中单列的类型不能是数组向量。
* 若 *Y* 是键值表或索引内存表，检查 *X* 中的每一个元素是否为 *Y* 中的主键。*X* 中元素的个数必须与
  *Y* 中主键列的个数一致。

注： *X* 和 *Y* 的数据类型需保持一致。若类型不一致，但属于同一分类，系统会将 *X*
强制转换为与 *Y* 一致的类型。

## 例子

```
in(3 3 5 2, 2 3);
// output
[true,true,false,true]

x=dict(INT,DOUBLE);
x[1, 2, 3]=[4.5, 6.6, 3.2];
x;
// output
3->3.2
1->4.5
2->6.6

in(1..6, x);
// output
[true,true,true,false,false,false]

t = table(1 3 5 7 9 as id)
2 3 in t
// output
[false,true]

kt = keyedTable(`name`id,1000:0,`name`id`age`department,[STRING,INT,INT,STRING])
insert into kt values(`Tom`Sam`Cindy`Emma`Nick, 1 2 3 4 5, 30 35 32 25 30, `IT`Finance`HR`HR`IT)
in((`Tom`Cindy, 1 3), kt);
// output
[true,true]

t1 = indexedTable(`sym`side, 10000:0, `sym`side`price`qty, [SYMBOL,CHAR,DOUBLE,INT])
insert into t1 values(`IBM`MSFT`GOOG, ['B','S','B'], 10.01 10.02 10.03, 10 10 20)
in((`IBM`MSFT, ['S','S']), t1);
[false,true]

```

*X* 为浮点型，*Y* 为整型，数据类型不一致，会将 *X* 转换为与 *Y* 一致的类型进行比较。

```
in(10, NULL)
// output
false

in('a', 97)
// output
true

in(1, 1.1 1.2 1.3)
// output
false

in(float(1.1 2.2 3.3 4.4 5.5 6.6 7.7 8.8), 1..9)
// output
[true,true,true,true,true,true,true,true]
```

`in` 可以搭配 `select`
使用，用于限定条件的筛选的范围：

```
select * from kt where name in [`Tom, `Cindy];
```

| name | id | age | department |
| --- | --- | --- | --- |
| Tom | 1 | 30 | IT |
| Cindy | 3 | 32 | HR |

相关函数：[find](../f/find.md), [binsrch](../b/binsrch.md)。

