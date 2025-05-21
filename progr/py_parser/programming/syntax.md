# 语法

本章主要介绍 DolphinDB Python Parser 中的变量赋值、语句和函数定义等相关内容。与标准的 Python 相比，Python Parser 在标识符、保留字、行与缩进、多行语句、数字类型、字符串、空行、同一行显示多条语句以及 print 输出等方面保持了相同的语法。然而，在某些方面可能存在细微的差异，这些差异将在后续各个章节中进行详细的说明。

需要注意的是：

* Python Parser 对推导式的支持不够完善，目前仅支持列表推导式（list comprehension）。
* Python Parser 暂不支持生成器表达式（generator expression）。
* Python Parser 只支持 print 输出到标准输出，不支持其它输出形式和输入。
* Python Parser 将 DolphinDB 中与 Python 内置函数同名的函数以及 DolphinDB 的常量对象封装在 dolphindb 库中，需要引入 dolphindb 库后进行调用。
* Python Parser 的函数暂不支持位置参数（/）、星号参数（\* 和 \*\*）、函数里面定义类、函数里面使用 import。

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
