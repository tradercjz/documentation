# parseExpr

## 语法

`parseExpr(X, [varDict], [modules], [overloadedOperators])`

## 参数

**X** 是一个字符串标量或向量。

**varDict** 为可选参数，是一个字典。如果指定了该参数，使用 [eval](../e/eval.html) 函数解析时，表达式中的变量会被解析成字典的 key，其值即为字典中该 key 所对应的 value。

**modules** 为可选参数，是字符串或字符串数组，表示需要加载的模块名称。

**overloadedOperators** 为可选参数，是一个字典。将运算符号映射为一个函数。key 必须是一个字符串标量，value
必须是一个二元函数。

## 详情

把字符串转换为元代码。使用 [eval](../e/eval.html) 函数可以执行
`parseExpr` 函数生成的元代码。

## 例子

```
a=parseExpr("1+2")
a;
// output
< 1 + 2 >

typestr(a);
// output
CODE

a.eval();
// output
3
```

将 JSON
字符串解析为字典

```
json1 = '{"f2":10.71,"f12":"000001"},{"f2":7.24,"f12":"000002"}'
parseExpr(json1).eval()

/*
output:
f2->10.71
f12->000001
*/
```

```
t=table(1 2 3 4 as id, 5 6 7 8 as value, `IBM`MSFT`IBM`GOOG as name);
parseExpr("select * from t where name='IBM'").eval();
```

| id | value | name |
| --- | --- | --- |
| 1 | 3 | IBM |
| 3 | 7 | IBM |

`parseExpr`
函数解析变量时，首先搜索会话中的局部变量，再搜索共享变量，但不会搜索函数体内定义的局部变量。

如下例所示，用户自定义函数 myfunc 后欲取得数据表 t3 中 ID 列1到5对应的行：

```
def myfunc(){
  t3 = table(1..100 as id)
  return parseExpr("select * from t3 where id in 1..5").eval()
}

myfunc()
```

产生如下错误信息：

```
myfunc() => myfunc: return ::evaluate(parseExpr("select * from t3 where id in 1..5")) => Can't find the object with name t3
```

解决此问题可以使用 [sql](../s/sql.html) 函数动态生成 SQL
语句，如下所示：

```
def myfunc(){
t3 = table(1..100 as id)
return sql(sqlCol("*"), t3, <id in 1..5>).eval()
}
myfunc();
```

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |

表达式中的变量和值通过字典形式传入，为 dict 的 key 赋值等价于为变量赋值。

```
d = dict(`a`b`c, (1, 2, 3))
parseExpr("a + b*c", d).eval()
// output
7
d[`a] = 5;
parseExpr("a + b*c", d).eval()
// output
11
```

下例解释表达式中使用函数的处理方式，因 dict 中未存储变量 first，first 解析时直接当作函数来处理。

```
index = [2000.01.01, 2000.01.31, 2000.02.15, 2000.02.20, 2000.03.12, 2000.04.16, 2000.05.06, 2000.08.30]
s = indexedSeries(index, 1..8)
d1 =  dict(STRING, ANY)
d1["S"] = s
parseExpr("resample(S, `M, first)", d1).eval()
```

在 modules 目录下的 test 模块内定义了一个 add 函数，调用模块中的函数，同时通过
overloadedOperators 参数，将二元运算符”+”映射为一个新的函数。代码执行时，运算符”+”将按照新函数进行计算。

```
parseExpr("test::add(1,2)+2", modules="test", overloadedOperators={"+": def(a, b){return a - b}}).eval()
// output
1
```

相关函数：[expr](../e/expr.html), [eval](../e/eval.html)

