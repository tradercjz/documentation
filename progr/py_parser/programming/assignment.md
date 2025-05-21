# 将单层索引赋值给一个变量，再修改该变量的元素值的方式进行修改：
tmp=a[1]
tmp[1]=19
a
// output: [2, [3, 19], 10]
```

## 释放变量

通过 `undef` 函数从内存中释放变量。

```
x=1;
undef(`x)
def max(a, b):
    if a > b:
        return a
    else:
        return b
undef(`max)
```

