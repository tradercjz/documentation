# attributeValues

## 语法

`attributeValues(obj)`

## 参数

**obj** 类实例。

## 详情

获取类实例的所有属性及其对应的属性值。

**返回值：**一个字典，key 是属性名称，value 是属性值。

## 例子

```
class Person {
	name :: STRING
	age :: INT
	def Person(name_, age_) {
		name = name_
		age = age_
	}
}
p1 = Person("Sam", 12)
attributeValues(p1)

/* output:
name->Sam
age->12
*/

p2 = Person("Andy", 16)
attributeValues(p2)

/* output:
name->Andy
age->16
*/
```

