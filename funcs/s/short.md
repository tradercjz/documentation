# short

## 语法

`short(X)`

## 详情

将输入的数据类型转换为 SHORT。

## 参数

**x** 可以是任意数据类型。

## 例子

```
x=short();
x;
```

返回：null

```
typestr x;
```

返回：SHORT

```
short(`12.3);
```

返回：12

```
short(`120.9c);
```

返回：120

```
short(32767);
```

返回：32,767

注： SHORT 数据类型的范围是[ -215+1, 215 -1] =
[-32767, 32767]。如果 *X* 超出了该范围，将会发生[溢出](../../progr/data_types.html#chap4_sect_data_type_description__section_oxj_hty_jxb)。

```
short(32768);
//Output
null

short(65578);
//Output
42

short(32789)
//Output
-32747
```

