# decimalFormat

## 语法

`decimalFormat(X, format)`

## 参数

**X** 可以是整型或浮点型的标量或向量。

**format** 是表示格式的字符串。

## 详情

把数字转换成指定格式的字符串。

| 标志 | 含义 | 备注 |
| --- | --- | --- |
| 0 | 强制数字位数 | 备注1 |
| # | 可选数字位数 | 备注2 |
| . | 小数点 |  |
| % | 百分号 | 备注3 |
| E | 科学计数法的符号 | 备注4 |
| , | 分隔符 | 备注5 |
| ; | 表示正数和负数的符号 | 备注6 |

* 备注1：小数点之前0的个数表示整数部分的位数。与之对比，小数点之后0的个数表示小数部分的位数。

  ```
  decimalFormat(123,"0");
  // output: 123

  decimalFormat(123,"00000");
  // output: 00123

  decimalFormat(123.45,"0");
  // output: 123

  decimalFormat(123.45,"0.0");
  // output: 123.5

  decimalFormat(123.45,"0.000");
  // output: 123.450

  decimalFormat(123.45, ".0");
  // output: 123.5

  decimalFormat(0.45, ".0");
  // output: .5
  ```
* 备注2：如果0与#同时在小数点后使用，0必须在#前面。

  ```
  decimalFormat(123.45,"0.#");
  // output: 123.5

  decimalFormat(123.45,"0.###");
  // output: 123.45

  decimalFormat(123.456,"0.000###");
  // output: 123.456

  decimalFormat(123.456789110,"0.000###");
  // output: 123.456789

  decimalFormat(0.345, ".##");
  // output: .35
  ```
* 备注3：%用于格式字符串的结尾。%和 E 在一个格式字符串中不能同时出现。

  ```
  decimalFormat(0.125,"0.00%");
  // output: 12.50%

  decimalFormat(0.125, "#.##%");
  // output: 12.5%

  decimalFormat(0.12567,"#.##%");
  // output: 12.57%
  ```
* 备注4：E 后面只能紧跟0，并且至少紧跟一个0。

  ```
  decimalFormat(1234567.89,"0.##E00");
  // output: 1.23E06

  decimalFormat(0.0000000000123456789,"0.000E0");
  // output: 1.235E-11
  ```
* 备注5：分隔符在一个格式字符串中只能出现一次。分隔符与小数点之间的位数或分隔符到结尾的位数即为分隔的间距。

  ```
  decimalFormat(123456789,"#,###");
  // output: 123,456,789

  decimalFormat(123456789.166,"#,###.##");
  // output: 123,456,789.17

  decimalFormat(123456789.166,"0,000.00");
  // output: 123,456,789.17
  ```
* 备注6：我们可以使用";"来选择数字对象的正负。

  ```
  decimalFormat(123.456,"0.00#E00;(0.00#E00)");
  // output: 1.235E02

  decimalFormat(-123.456,"0.00#E00;(0.00#E00)");
  // output: (1.235E02)
  ```

