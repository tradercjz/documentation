# interpolate

## 语法

`interpolate(X, [method='linear'], [limit], [inplace=false],
[limitDirection='forward'], [limitArea], [index])`

## 参数

**X** 是一个数值型向量。

**method** 可选参数，是一个字符串，表示插值的方式。它的可取值为：

* 'linear'：线性插值
* 'pad'：使用已有的值填充
* 'nearest'：使用最接近 NULL 值的有效值填充
* 'krogh'：使用 krogh 多项式插值

如果没有指定，默认值为 'linear'。

**limit** 可选参数，是一个正整数，表示最多要填充的连续 NULL 值的个数。

**inplace** 可选参数， 是一个布尔值，表示是否使用结果覆盖输入的 *X*。默认值为
false，会返回一个新的向量。

**limitDirection** 可选参数， 是一个字符串，表示填充 NULL 的方向。它的可取值为：'forward',
'backward' 和 'both'。默认值为 'forward'。

**limitArea** 可选参数， 是一个字符串，表示填充的区域。它的可取值为：

* 空字符串： 填充的区域没有限制
* 'inside'： 只填充有效值包围的 NULL 值
* 'outside'： 只填充有效值之外的 NULL 值

**index** 可选参数，是一个时间类型或数值类型的索引向量，与 X 等长且不包含空值。当指定 *index* 时，函数将以该索引向量为横坐标，X
为纵坐标，对 X 中的缺失值进行插值。

## 详情

填充数值型向量中的缺失值。默认情况下，基于 X 中每个元素的下标索引（0, 1, 2, ...,
size(X)-1）进行插值计算。支持自定义横坐标的插值计算，详见参数 *index*。

## 返回值

返回填充后的数值型向量。

## 例子

```
a=[NULL,NULL,1,2,NULL,NULL,5,6,NULL,NULL];

interpolate(a);
// output: [,,1,2,3,4,5,6,6,6]

interpolate(X=a, method="pad");
// output: [,,1,2,2,2,5,6,6,6]

interpolate(X=a, limitDirection='both');
// output: [1,1,1,2,3,4,5,6,6,6]

interpolate(X=a, limit=1, limitDirection='both');
// output: [,1,1,2,3,4,5,6,6,]

interpolate(X=a, limitDirection='both', limitArea='outside');
// output: [1,1,1,2,,,5,6,6,6]

a;
// output: [,,1,2,,,5,6,,]

interpolate(X=a, limitDirection='backward', inplace=true);
// output: [1,1,1,2,3,4,5,6,,]

a;
// output: [1,1,1,2,3,4,5,6,,]

dates=[2023.10.01, 2023.10.03, 2023.10.08, 2023.10.13, 2023.10.31, 2023.11.02, 2023.11.07, 2023.11.08,2023.11.09,2023.11.14]

interpolate(X=a,index=dates)
// output
[,,1,2,4.160000000000001,4.400000000000001,5,6,6,6]

a=[10,NULL,30,NULL,50];
index=[0, 3, 4, 7, 8]
interpolate(X=a,method='linear',index=index)
// output
[10,25,30,45,50]
```

