# temporalParse

## 语法

`temporalParse(X, format)`

别名：datetimeParse

## 参数

**X** 是一个字符串。

**format** 是表示时间序列对象格式的字符串。

## 详情

把字符串转换成 DolphinDB 中的时序类型数据。如果系统不能识别时序格式，将返回 NULL。

DolphinDB 具有以下时序格式：

| 格式 | 含义 | 范围 |
| --- | --- | --- |
| yyyy | 年份（4个数字） | 1000-9999 |
| yy | 年份（2个数字） | 00-99. (00-39: 2000-2039; 40-99: 1940-1999) |
| MM | 月份 | 1月12日 |
| MMM | 月份 | JAN, FEB, ... DEC （不区分大小写） |
| dd | 日期 | 1月31日 |
| HH | 时（24小时制） | 0-23 |
| hh | 时（12小时制） | 0-11 |
| mm | 分钟 | 0-59 |
| ss | 秒 | 0-59 |
| aa | 上午/下午 | AM, PM. （不区分大小写） |
| SSS | 毫秒 | 0-999 |
| nnnnnn | 微秒 | 0-999999 |
| nnnnnnnnn | 纳秒 | 0-999999999 |

`temporalParse` 函数中的 *format* 参数有以下两种表示方式：

* 使用分隔符

  对于 *format* 参数 ，除了 y, M, d, H, h, m, s, a, S, n
  以外的符号的字符都可以作为分隔符。*format* 参数中的分隔符需要与输入字符串中的分隔符一致。

  ```
  temporalParse("14-02-2018","dd-MM-yyyy");
  // output
  2018.02.14

  temporalParse("14-02-2018","dd/MM/yyyy");
  // output
  00d

  temporalParse("14//02//2018","dd//MM//yyyy");
  // output
  2018.02.14

  temporalParse("14//02//2018","dd/MM/yyyy");
  // output
  00d

  temporalParse("14//02//2018","dd..MM..yyyy");
  // output
  00d
  ```

  我们可以使用单个字母来简化格式。例如，使用 "y/M/d" 代替 "yyyy/MM/dd"。因为 "y" 可以表示
  "yyyy" 和 "yy", 系统会根据数字的个数采用 "yyyy" 或 "yy"。

  ```
  temporalParse("14-02-18","d-M-y");
  // output
  2018.02.14

  temporalParse("2018/2/6 02:33:01 PM","y/M/d h:m:s a");
  // output
  2018.02.06T14:33:01
  ```

  "MMM","SSS", "nnnnnn" , "nnnnnnnnn" 不能使用单个字母。

  ```
  temporalParse("02-FEB-2018","d-MMM-y");
  // output
  2018.02.02

  temporalParse("02-FEB-2018","d-M-y");
  // output
  00d

  temporalParse("13:30:10.001","H:m:s.SSS");
  // output
  13:30:10.001

  temporalParse("13:30:10.001","H:m:s.S");
  // output
  Invalid temporal format: 'H:m:s.S'. Millisecond (S) must have three digits.

  temporalParse("13:30:10.008001","H:m:s.nnnnnn");
  // output
  13:30:10.008001000

  temporalParse("13:30:10.008001","H:m:s.n");
  // output
  Invalid temporal format: 'H:m:s.n'. Nanosecond (n) must have six or nine digits.
  ```

  `temporalParse`
  函数解释输入字符串中数字个数的方式是非常灵活的。

  ```
  temporalParse("2-4-18","d-M-yy");
  // output
  2018.04.02

  temporalParse("2-19-6","H-m-s");
  // output
  02:19:06

  temporalParse("002-019-006","H-m-s");
  // output
  02:19:06
  ```

  对于毫秒，微秒和纳秒，对应的数字位个数必须是3, 6, 9。

  ```
  temporalParse("2018/2/6 13:30:10.001","y/M/d H:m:s.SSS");
  // output
  2018.02.06T13:30:10.001

  temporalParse("2018/2/6 13:30:10.01","y/M/d H:m:s.SSS");
  // output
  00T

  temporalParse("2018/2/6 13:30:10.000001","y/M/d H:m:s.nnnnnn");
  // output
  2018.02.06T13:30:10.000001000

  temporalParse("2018/2/6 13:30:10.0000010","y/M/d H:m:s.nnnnnn");
  // output
  00N
  ```
* 不使用分隔符

  对于这种表示方式，*format* 参数必须与上述表格中的格式对应，不能使用单个字母来表示格式。

  ```
  temporalParse("20180214","yyyyMMdd");
  // output
  2018.02.14

  temporalParse("122506","MMddyy");
  // output
  2006.12.25

  temporalParse("155950","HHmmss");
  // output
  15:59:50

  temporalParse("035901PM","hhmmssaa");
  // output
  15:59:01

  temporalParse("02062018155956001000001","MMddyyyyHHmmssnnnnnnnnn");
  // output
  2018.02.06T15:59:56.001000001
  ```

