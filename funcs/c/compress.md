# compress

## 语法

`compress(X, [method='lz4'])`

## 参数

**X** 是一个向量或数据表。

**method** 是一个字符串，为压缩算法，可取值为 "lz4", "delta" (delta-of-delta encoding), "zstd" 或
"chimp"，默认值为 "lz4"。其中，

* lz4 适用于几乎所有数据类型，它侧重于压缩和解压速度，虽然压缩比不是最高的，但解压速度快，适用于需要快速解压的场景。
* zstd 同样适用于几乎所有数据类型，其压缩比高于 lz4，但解压缩速度较 lz4 慢约1倍。它适用于对压缩比有较高要求的场景。
* delta 使用 delta of delta 算法，适用于 SHORT, INT, LONG 与时间或日期类型数据。
* chimp 适用于小数部分长度在三位以内的 DOUBLE 类型的数据。

## 详情

使用指定压缩算法对向量或数据表进行压缩。压缩某个变量后，需要使用函数 [decompress](../d/decompress.html) 将其解压缩后方可使用该变量。

## 例子

```
x=1..100000000
y=compress(x, "delta");

y.typestr();
// output: HUGE COMPRESSED VECTOR

z=compress(x, "zstd");
z.typestr();
// output: HUGE COMPRESSED VECTOR

select name, bytes from objs() where name in `x`y;
```

| name | bytes |
| --- | --- |
| x | 402653952 |
| y | 13634544 |

注： 对向量 x 压缩后的结果（y ）使用 `size` 函数，结果为 y 的长度，而不是 x
的长度。若要从 y 中获取 x 的长度或其它信息，需先将 y 解压缩：

```
y.size();
// output: 12670932

z=decompress(y);
z.size();
// output: 100000000
```

相关函数：[decompress](../d/decompress.html)

