# prefix join

## 语法

```
pj(leftTable, rightTable, matchingCols, [rightMatchingCols])
```

## 参数

* **leftTable** 和 **rightTable** 是连接的表。
* **matchingCols** 是一个字符串，表示连接列的名称。
* **rightMatchingCols** 是一个字符串，表示右表连接列的名称。当 *leftTable* 和
  *rightTable* 的连接列不同时，必须指定
  *rightMatchingCols*。返回结果中的连接列与左表的连接列名称相同。

## 详情

将左表连接列中以右表连接列内容开头的记录与相应的右表记录连接。如果左表中有多条匹配记录，pj会取所有匹配的记录。因此，pj返回结果的行数可能比右表的行数多。

注： 当左右表均为分布式表时，`pj` 仅在分布式表的分区内部匹配数据。

pj和ej类似，它们的区别如下：

* pj只能有一个连接列，且连接列必须是STRING或SYMBOL类型。
* pj返回左表连接列中以右表连接列内容开头的记录。

## 例子

例1：两个表的连接列名称相同。

```
t1=table(["DT_1","DT2","BC.1","GB7T","AC/8","ACA9","DEF"] as id, 20.5 12.3 26.8 15.2 24.7 56.8 33.6 as price)
t2=table(["DT","BC","GB","AC", "TD"] as id,12 45 78 26 89 as qty);
t1;
```

| id | price |
| --- | --- |
| DT\_1 | 20.5 |
| DT2 | 12.3 |
| BC.1 | 26.8 |
| GB7T | 15.2 |
| AC/8 | 24.7 |
| ACA9 | 56.8 |
| DEF | 33.6 |

```

t2;
```

| id | qty |
| --- | --- |
| DT | 12 |
| BC | 45 |
| GB | 78 |
| AC | 26 |
| TD | 89 |

```
select * from pj(t1,t2,`id);
```

| id | price | t2\_id | qty |
| --- | --- | --- | --- |
| DT\_1 | 20.5 | DT | 12 |
| DT2 | 12.3 | DT | 12 |
| BC.1 | 26.8 | BC | 45 |
| GB7T | 15.2 | GB | 78 |
| AC/8 | 24.7 | AC | 26 |
| ACA9 | 56.8 | AC | 26 |

例2：两个表的连接列名称不同。

```
t1=table(["DT_1","DT2","BC.1","GB7T","AC/8","ACA9","DEF"] as id, 20.5 12.3 26.8 15.2 24.7 56.8 33.6 as price)
t2=table(["DT","BC","GB","AC", "TD"] as prefix,12 45 78 26 89 as qty);
select * from pj(t1,t2,`id,`prefix);
```

| id | price | prefix | qty |
| --- | --- | --- | --- |
| DT\_1 | 20.5 | DT | 12 |
| DT2 | 12.3 | DT | 12 |
| BC.1 | 26.8 | BC | 45 |
| GB7T | 15.2 | GB | 78 |
| AC/8 | 24.7 | AC | 26 |
| ACA9 | 56.8 | AC | 26 |

