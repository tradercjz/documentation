# 类

Python Parser 中引入了类机制，目前支持函数封装、运算符重载等简单功能，暂不支持继承、在函数中定义类等功能。

## 例 1：函数封装

```
class student:
    def __init__(self, name, gender, score_list):
        self.name = name
        self.gender = gender
        self.score = score_list

    def get_avgScore(self):
        return avg(self.score.toddb())

    def get_Info(self):
        print("name:", self.name)
        print("gender:", self.gender)
        print("avgScore:", self.get_avgScore())

x = student("pl", "male", [100, 99, 98, 92])
x.get_Info()

// output:
name:
  pl
gender:
  male
avgScore:
  97.25
```

## 例 2：重载运算符

以下例子定义一个类 Complex，实现了 `__add__` 方法重载加号，以及实现了 `__repr__` 方法用于显示对象。

```
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
    def __add__(self, other):
        return Complex(self.r + other.r, self.i + other.i)
    def __repr__(self):
        sign = "+" if self.i >= 0 else ""
        return str(self.r) + sign + str(self.i) + "i"

x = Complex(3, 4)
y = Complex(0, -1)
x
// output: 3+4i
y
// output: 0-1i
x + y
// output: 3+3i
```

