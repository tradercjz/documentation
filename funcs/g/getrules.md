# getRules

## 语法

`getRules([engineName])`

## 参数

**engineName** 字符串向量，代表要查询的规则引擎的名称。该参数省略时，返回当前节点所有规则引擎的规则信息。

## 详情

查询规则引擎的规则信息，包括规则集、规则检查策略和回调函数等。

返回一个字典，key 为引擎的名称， value 为字典，包含以下信息：

* ruleSets：该引擎的规则集。类型为一个字典，key 和 value 定义如下：

  + key：规则集的键值。key 为 “Default” 指默认规则。
  + value：规则集中该键值对应的规则。
* policy：指定引擎的规则检查策略。
* callback：指定引擎的回调函数的名称，未配置回调函数时为空字符串。

## 例子

```
// 设置规则集
x = [1, 2, NULL]
y = [ [ < value > 1 > ], [ < price < 2 >, < price > 6 > ], [ < value*price > 10 > ] ]
ruleSets = dict(x, y)

// 创建规则引擎
names = `sym`value`price`quantity
types = [INT, DOUBLE, DOUBLE, DOUBLE]
dummy = table(1:0, names, types)
outputNames = `sym`value`price`rule
outputTypes = [INT, DOUBLE, DOUBLE, BOOL[]]
outputTable = table(10:0, outputNames, outputTypes)
test = createRuleEngine(name="ruleEngineTest", ruleSets=ruleSets, dummyTable=dummy, outputColumns=["sym","value","price"], outputTable=outputTable, policy="all", ruleSetColumn="sym")
test2 = createRuleEngine(name="ruleEngineTest2", ruleSets=ruleSets, dummyTable=dummy, outputColumns=["sym","value","price"], outputTable=outputTable, policy="all", ruleSetColumn="sym")

// 查询规则
getRules(["ruleEngineTest"])
/*
ruleEngineTest->
    ruleSets->
        Default->(value * price > 10)
        1->(value > 1)
        2->(price < 2, price > 6)

    policy->all
    callback->
*/

// 更新规则
updateRule("ruleEngineTest", 1, [<value > 2>])

// 再次查询
getRules()
/*
ruleEngineTest->
    ruleSets->
        Default->(value * price > 10)
        1->(value > 2)
        2->(price < 2, price > 6)

    policy->all
    callback->
*/
```

相关函数：[createRuleEngine](../c/createRuleEngine.md), [updateRule](../u/updateRule.md), [deleteRule](../d/deleteRule.md)

