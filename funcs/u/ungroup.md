# ungroup

## 语法

`ungroup(X)`

## 参数

**X** 必须是一个表对象。

## 详情

若表 *X*
的某列中包含数组向量或列式元组，则将其展开后整体做为一列；同时保留原同行中其余列的数据，按照对应数组向量或列式元组的元素数量进行复制填充；最后返回一个表。

若 *X* 的行数为0或不包含数组向量或列式元组，则直接返回 *X*。

## 例子

```
x = array(INT[], 0).append!([1 2 3, 4 5, 6 7 8, 9 10])
t = table(1 2 3 4 as id, x as vol)
ungroup(t)
// output
id vol
-- -------
1  1
1  2
1  3
2  4
2  5
3  6
3  7
3  8
4  9
4  10

//创建一个表，其中 price 列为列式元组。
sym = `st1`st2`st3
price = [[3.1,2.5,2.8], [3.1,3.3], [3.2,2.9,3.3]]
t = table(sym, price)
t;
```

| sym | price |
| --- | --- |
| st1 | [3.1000,2.5000,2.8000] |
| st2 | [3.1000,3.3000] |
| st3 | [3.2000,2.9000,3.3000] |

```

ungroup(t)
```

| sym | price |
| --- | --- |
| st1 | 3.1 |
| st1 | 2.5 |
| st1 | 2.8 |
| st2 | 3.1 |
| st2 | 3.3 |
| st3 | 3.2 |
| st3 | 2.9 |
| st3 | 3.3 |

```

sym = `st1`st2`st2`st1`st3`st1`st3`st2`st3
volume = 106 115 121 90 130 150 145 123 155;
t = table(sym, volume);
t;

t1 = select toArray(volume) as volume_all from t group by sym;
t1;
```

| sym | volume\_all |
| --- | --- |
| st1 | [106,90,150] |
| st2 | [115,121,123] |
| st3 | [130,145,155] |

```

ungroup(t1)
```

| sym | volume\_all |
| --- | --- |
| st1 | 106 |
| st1 | 90 |
| st1 | 150 |
| st2 | 115 |
| st2 | 121 |
| st2 | 123 |
| st3 | 130 |
| st3 | 145 |
| st3 | 155 |

