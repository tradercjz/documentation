# nunique

## 语法

`nunique(X, [ignoreNull=false])`

## 参数

**X** 是一个向量/数组向量，或包含多个等长向量的元组。

**ignoreNull** 是一个布尔值，表示是否忽略 *X* 中 NULL 值。若指定
*ignoreNull*=true，则统计唯一值时将不考虑 NULL 值；否则将会统计 NULL 值。默认值为 false。请注意，当 *X*
是元组或数组向量时，不可指定 *ignoreNull*=true。

## 详情

*X* 是向量/数组向量时，计算 *X* 中唯一值的数量。

*X* 是元组时，其内每个向量位于相同位置的元素组成一个 key，计算唯一 key 的数量。

## 例子

```
v = [1,3,1,-6,NULL,2,NULL,1];
nunique(v);
// output: 5

//指定 ignorNull = true，统计唯一值时将不考虑 NULL 值
nunique(v,true);
// output: 4

a = array(INT[], 0, 10).append!([1 2 3, 3 5, 6 8 8, 9 10])
nunique(a)
// output: 8
```

```
t=table(1 2 4 8 4 2 7 1 as id, 10 20 40 80 40 20 70 10 as val);
select nunique([id,val]) from t;
```

| nunique |
| --- |
| 5 |

```
dbName = "dfs://testdb"
if(existsDatabase(dbName)){
   dropDatabase(dbName)
}

db=database("dfs://testdb", VALUE, 2012.01.11..2012.01.29)

n=100
t=table(take(2012.01.11..2012.01.29, n) as date, symbol(take("A"+string(21..60), n)) as sym, take(100, n) as val)

pt=db.createPartitionedTable(t, `pt, `date).append!(t)
select nunique(date) from pt group by sym
```

