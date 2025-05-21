# 工具函数

## 元代码

支持通过以下函数生成类中定义的方法调用元代码：

* `objCall(obj, methodName, args...)`：
* `unifiedObjCall(obj, methodName, args)`
* `makeObjCall(obj, methodName, args...)`
* `makeUnifiedObjCall(obj, methodName, args)`

其中：

* *obj* 为 OOP 对象。
* *methodName* 是一个字符串，表示方法名称。
* 第1和第3个函数中的 *args...* 是传入的参数。
* 第2和第4个函数中的 *args* 是元组，表示传入的参数。

**示例**

利用 `makeObjCall` 函数创建 OOP
方法调用的元代码：

```
class Person {
  name :: STRING
  age :: INT

  def Person(name_, age_) {
    name = name_
    age = age_
  }

  def setName(newName) {
    name = newName
  }

  def getName(year, gender) {
  	if(year<2020)
  		return year
    else
    	return name
  }
}

a = Person("Harrison",20)
f = a.getName{2015}
f(true)

//使用 objCall 方法
objCall(a, "getName", "name1", 2022)
//使用 unifiedObjCall 方法
unifiedObjCall(a, "getName", ("name1", 2022))
//使用 makeObjCall 方法
makeObjCall(a, "getName", "name1", 2022).eval()
//使用 makeUnifiedObjCall 方法
makeUnifiedObjCall(a, "getName", ("name1", 2022)).eval()
```

## 其它工具函数

* `isInstanceOf(obj, cls)`：*obj* 为 OOP 对象，*cls*
  为类。

该函数用于检查对象是否为特定类或该类的子类实例，返回一个布尔值。

```
class B {
        def B() {}
}

class D : B {
        def D() {}
}
class A {
        def A() {}
}

d = D()

isInstanceOf(d, D)  // true
isInstanceOf(d, B)  // true
isInstanceOf(d, A)  // false
```

* `setAttr(obj, attrName, value)`：*obj* 为 OOP
  对象；*attrName* 为要设置的属性名称；*value* 为要设置的属性值。

该函数用于设置或修改对象的属性值。例如 `setAttr(obj, `alpha, 16)` 或者
`obj.setAttr(`alpha, 16)`。

