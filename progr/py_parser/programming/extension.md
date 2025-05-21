# SQL 脚本语言的语法和 DolphinDB 的语法保持一致，可以直接使用 "a:b"。
select top 0:5 * from pt where sym like "A%"

// output：
id	sym	qty
7cd8359b-e1f4-b8b0-a0e5-6f0c6e971132	A3	84
b3aafacc-525e-3459-252d-4a3b63bfc994	A9	82
96252fcb-80ec-4272-5113-205eb02dee87	A9	96
3816fa58-94a7-97c0-170a-9f9e79594567	A9	85
a12e999c-5c5b-a392-3865-3384b823f583	A3	45
114cd225-2ff5-25f5-98ce-84e4253215e5	A2	77
```

## 元编程

DolphinDB 元代码用于生成动态的表达式，其由一对尖括号 “<>” 来包裹对象或表达式。

Python Parser 中的元代码编写规则和 DolphinDB 保持一致，但部分语法存在差异，例如：Python Parser 暂不支持 DolphinDB 特有的语法，如 "1 2 3", "a:b", "a..b", "func [1,2,3]"等。

```
eval(<1 + 3>)
// output：4

sqlColAlias(<avg(PRC)>, `avgPRC)
// output: < avg(PRC) as avgPRC >

n=20
id=symbol(string(rand(uuid(), n)))
sym=rand(flatten(("A"+string(seq(1,10)), "B"+string(seq(1,10)), "C"+string(seq(1,10))).toddb()), n)
qty=rand(100, n)
t=table(id, sym, qty)
sql(select=sqlCol("*"), from=t, groupBy=sqlCol(`sym), groupFlag=0, limit=1)
// output: < select top 1 * from tf0746a0500000000 context by sym >
```

参考：[元编程](../../objs/meta_progr.html)

## `timer` 语句

支持使用 `timer(n):` 计算 Python Parser 代码运行时间，其中 n 代表执行次数。

```
def fib(n):
    xs = []
    a, b = 0, 1
    while a < n:
        xs.append(a)
        a, b = b, a + b
	return xs
timer(1000): fib(2000)
// output: Time elapsed: 108.709 ms
```

参考：[timer 语句](../../statements/timer.html)

## 字符串创建方式扩展

在 Python Parser 中，可以通过 Python 的方式创建字符串，也可以通过使用 DolphinDB  ```  字符串标识符的创建方式字符串。

