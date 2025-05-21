# regexFindStr

## 语法

`regexFindStr(str, pattern, [onlyFirst=true],
[offset])`

## 详情

不同于 `regexFind` 返回满足条件的字符串位置，`regexFindStr` 从第
*offset* 个位置开始搜索，返回 *str* 中满足正则表达式 *pattern* 的字符串：

* 当*str*为标量，且 *onlyFirst* 为 true
  时，若存在满足条件的子字符串，则返回一个字符串标量，否则返回一个空的字符串。
* 当 *str* 为标量，且 *onlyFirst* 为 false
  时，若存在满足条件的子字符串，则返回一个字符串向量，其元素为所有满足条件的子串。
* 当 *str* 为向量，且 *onlyFirst* 为 true 时，返回一个字符串向量，其中每个元素都是 *str*中对应位置元素中第一个匹配正则表达式的子字符串。
* 当 *str* 为向量，且 *onlyFirst* 为 false 时，返回一个元组，其中每个元素都是 *str*对应位置元素中所有匹配正则表达式的子字符串的向量。

注： 该函数新增于 2.00.11.1版本。

## 参数

**str** 字符串或字符串向量，表示待搜索的对象。

**pattern** 字符串，表示搜索的模式字符串（正则表达式）。模式字符串可以包含字面量字符、元字符或两者的组合。

**onlyFirst** 布尔标量，表示是否只返回与正则表达式匹配的第一个子字符串：

* 默认值为 true，此时针对 str 中的每一个字符串，仅返回第一个满足正则表达式的子字符串；
* 设置为 false 时，针对 str 中的每一个字符串，返回所有满足正则表达式的非重叠匹配的子字符串。

**offset** 非负整数，表示从 *str* 的第 *offset* 个位置开始搜索。默认值为0，即 *str*
的第一个位置。

## 例子

*str* 为标量，且 *onlyFirst* 为 true 时：

```
regexFindStr('234AA(2)BBB S&P', '([A|B|C|+|-]*)', true)
```

返回：AA

*str* 为标量，且 *onlyFirst* 为 *false* 时：

```
regexFindStr('234AA(2)BBB S&P', '([A|B|C|+|-]*)', false)
```

返回：["AA","BBB"]

*str* 为向量，且 *onlyFirst* 为 true 时：

```
regexFindStr(['234AA(2)BBBS&P', '234AA(2)BBBS&P'], '([A|B|C|+|-]*)', true)
```

返回：["AA","AA"]

*str* 为向量，且 *onlyFirst* 为 false 时：

```
regexFindStr(['234AA(2)BBBS&P', '234AA(2)BBBS&P'], '([A|B|C|+|-]*)', false)
```

返回：(["AA","BBB"],["AA","BBB"])

**相关信息**

* [regexFind](regexFind.html "regexFind")

