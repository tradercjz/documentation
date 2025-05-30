# 元编程

元编程（Metaprogramming）是一种高级的编程范式，其核心思想是将代码视为可处理的数据。使用元编程设计的程序具有读取、生成、分析或转换其他程序的功能，可以在运行时自行修改代码。这种范式打破了传统编程中程序运行动态而程序本身静态的界限，实现了两者的动态性，极大地增强了代码的灵活性和可控性。

元代码是由 “<” 和 “>” 包围的对象或表达式。在 DolphinDB 中，可以直接使用 “<” 和 “>” 包裹对象或表达式生成一个元代码。由
“<>” 包裹的对象不会立即执行，而是在需要时通过 `eval` 函数执行。例如：

```
a = <1 + 2 * 3>
typestr(a);
// output: CODE
// a 是元代码，它的数据类型是 CODE

eval(a);
// output: 7
// eval 函数用于执行元代码
```

DolphinDB 为不同的元代码使用场景，分别提供了不同的生成元代码的方法，方便用户灵活调用，包括函数元编程和 SQL 元编程。

## 函数元编程

函数元编程是指通过参数传递等手段动态获取函数定义和参数的方法。这种方式特别适合于复杂的数据分析任务，能够有效提高代码的灵活性和复用性。用户可以根据特定的数据结构和需求，动态调整函数的行为，从而实现更高效的分析和处理。

## SQL 元编程

SQL 元编程是指在代码执行时动态生成 SQL 语句的方法。这种方法方便用户通过程序脚本来生成 SQL 代码，达到动态生成和执行的目的。DolphinDB 提供了两种编写
SQL 元编程的方式：基于函数的元编程和基于宏变量的元编程。

* 基于函数的元编程：通过内置 SQL 元编程函数的组合调用生成元代码。DolphinDB 提供了一系列元编程函数，帮助生成元代码。
* 基于宏变量的元编程：通过定义宏变量，并在由 “<” 和 “>” 包裹的 SQL
  语句中直接引用宏变量的元编程方式。这种方式书写简单，且代码更直观、可读性强。

通过 SQL 元编程，用户可以根据需要动态地选择查询的列、表、过滤条件等，从而构建出符合特定需求的查询语句。元编程的应用场景包含但不限于以下几种：

* SQL 的字段名或过滤条件等需要通过函数参数或变量进行传递。例如，对表中每行数据动态应用计算规则、计算窗口大小各不相同的多个滑动窗口因子等。
* 查询列数非常多的表中的多个字段，或者对表中多个字段执行相同的操作，通过脚本书写 SQL 语句的脚步冗长且耗时。例如，同时对多个字段求和等。

接下来将分两个章节展开介绍 DolphinDB 函数元编程和 SQL 元编程。

