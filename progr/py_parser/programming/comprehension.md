# 推导式

Python Parser 暂时仅支持列表推导式。

## 列表推导式语法

```
[表达式 for 变量 in 列表]
[out_exp_res for out_exp in input_list]

或者

[表达式 for 变量 in 列表 if 条件]
[out_exp_res for out_exp in input_list if condition]
```

## 例子

```
multiples = [i for i in range(30) if i % 3 == 0]
print(multiples)

// output: [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
```

