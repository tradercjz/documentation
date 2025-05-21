# cumnunique

## 语法

`cumnunique(X, [ignoreNull=false])`

参数说明和窗口计算规则请参考：[cumFunctions](../themes/cumFunctions.html)

## 参数

**ignoreNull** 是一个布尔值，表示是否忽略 *X* 中 NULL 值。若指定
*ignoreNull*=true，则统计唯一值时将不考虑 NULL 值；否则将会统计 NULL 值。默认值为 false。

## 详情

统计 *X* 元素的累计唯一值数量。若指定 *ignoreNull*=true，则统计唯一值时将不考虑 NULL
值；否则将会统计 NULL 值。

## 例子

```
v = [NULL, 1, 2, -6, 0, 1, 2]
cumnunique(v)
// output: [1,2,3,4,5,5,5]

cumnunique(v,true)
// output: [0,1,2,3,4,4,4]

t = table(`a`a`b`c`a`b as id, 20 20 10 40 30 20 as val)
select cumnunique(id) as cumVal from t
```

| cumVal |
| --- |
| 1 |
| 1 |
| 2 |
| 3 |
| 3 |
| 3 |

