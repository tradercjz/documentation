# digitize

## 语法

`digitize(x, bins, [right=false])`

## 参数

**x**  一个浮点型、整型或 DECIMAL 类型的标量或向量。

**bins** 一个单调递增或递减的浮点型、整型或 DECIMAL 类型向量。

**right** 一个布尔值，为可选参数，设置区间包含右边界还是左边界，默认为 false（包含左边界）。

## 详情

返回 *x* 所属的 *bins* 的索引，返回值的数据形式与 *x* 一致。

| right | bins 顺序 | 返回的索引满足 |
| --- | --- | --- |
| false | 升序 | *bins* 里第一个大于 *x* 的元素的索引 |
| true | 升序 | *bins* 里第一个大于等于 *x* 的元素的索引 |
| false | 降序 | *bins* 里第一个小于等于 *x* 的元素的索引 |
| true | 降序 | *bins* 里第一个小于 *x* 的元素的索引 |

如果 *x* 中的值超出 *bins* 的左或右边界，则返回 0 或 *bins* 的长度。

该函数的功能和使用方法同 numpy.digitize。

## 例子

```
bins = [1,3,3,5,5]
// 返回 bins 里第一个大于 x 的元素的索引
digitize(3, bins=bins, right=false)
// output: 3
//返回 bins 里第一个大于 x 的元素的索引，由于 bins 里不存在这样的元素，返回 size(bins)
digitize(5, bins=bins, right=false)
//output: 5
// 返回 bins 里第一个大于等于 x 的元素的索引
digitize(5, bins=bins, right=true)
//output: 3
bins = reverse(bins)
digitize(5, bins=bins, right=false)
//output: 0
digitize(5, bins=bins, right=true)
//output: 2

x = [-1,0,1,2,3,4,5,6]
bins = [1,3,5]
digitize(x=x, bins=bins, right=false)
//output: [0,0,1,1,2,2,3,3]
digitize(x=x, bins=bins, right=true)
//output: [0,0,0,1,1,2,2,3]
bins = reverse(bins)
digitize(x=x, bins=bins, right=false)
//output: [3,3,2,2,1,1,0,0]
digitize(x=x, bins=bins, right=true)
//output: [3,3,3,2,2,1,1,0]
```

`digitize` 函数相较于 `bucket` 函数更灵活，可以自定义 *bins*
。以下为示例：

```
bucket(9 23 54 36 46 12, 12:53, 2) //报错：dataRange must be the mutltiplier of bucketNum.
```

因为 [12, 53) 中元素个数不能被2整除，所以不能使用 `bucket` 来分桶。

```
digitize(9 23 54 36 46 12 , 12 40 53)
// output: [0,1,3,1,2,1]
```

`digitize` 函数中，函数按照自定义的 *bins* 给数据分桶。

