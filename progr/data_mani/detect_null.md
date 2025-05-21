# 空值检查

我们可以使用 [isNull](../../funcs/i/isNull.html) 函数或 [hasNull](../../funcs/h/hasNull.html) 函数来检查是否包含空值。`isNull`
函数返回结果的数据结构与输入数据的数据结构一致。`hasNull` 函数的返回结果是0或1，表示输入数据中是否包含空值。

```
isNull(00i);
// output
1

isNull(-128c);
// output
1
// 最小的 char 值表示空值

isNull(1 NULL 2);
// output
[0,1,0]

hasNull(1 NULL 2);
// output
1
```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
