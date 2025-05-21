# method2: set([iterable])
st1 = set(['e', 'o', 'g', 'l'])
type(st1)
// output: set
```

## 访问集合中的元素

集合中的元素是无序的，因此不能够通过索引进行访问。

## 更新集合

1. 追加不可变元素

   ```
   st.add("0")
   st
   // output: {1, 2, '3', '4', '5', '0'}
   st.add([1,3,5])
   // output: 'TypeError: unhashable type: 'list''
   ```
2. 更新集合

   ```
   st.update({'0', 1, 2, '4', '5', '6'})
   st
   // output: {1, 2, '3', '4', '5', '0', '6'}
   ```
3. 删除数据

   remove：删除指定元素。删除的元素必须在集合中，如果不存在，则会报错。

   ```
   st.remove('3')
   st
   // output: {1, 2, '4', '5', '0', '6'}

   st.remove('7')
   // output: 'KeyError: "7"'
   ```

   discard：删除指定元素。删除的元素如果不存在，不会报错。

   ```
   st = {1,2,"3","4","5"}
   st.discard('4')
   st
   // output: {1, 2, '3', '5'}

   st.discard('4')   # 再次删除 '4'，即使不存在该元素，也不会报错
   st
   // output: {1, 2, '3', '5'}
   ```

   pop：随机删除一个元素，并返回被删除的元素。

   ```
   st = {1,2,"3","4","5"}
   st.pop()
   // output: 1
   ```

   clear：清空集合

   ```
   st = {1,2,"3","4","5"}
   st.clear()
   st
   // output: {}
   ```

## 集合可用的所有属性和方法

```
dir(st)
// output: ['__bitAnd__', '__bitOr__', '__bitXor__', '__dir__', '__eq__', '__ge__', '__gt__', '__ibitAnd__', '__ibitOr__', '__ibitXor__', '__init__', '__isub__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__repr__', '__req__', '__rne__', '__str__', '__sub__', 'add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update', 'toddb', 'union', 'update']
```

其中 `toddb` 是 Python Parser 中特有的方法，它支持将 Python Parser 的集合对象转换成 DolphinDB 的集合。DolphinDB 的集合是强类型的，若 Python Parser 的集合中元素类型不一致，则无法通过 `toddb` 进行转换。

```
st = {1,2,"3","4","5"}
type(st.toddb())
// output: TypeError: keyType can't be BOOL or ANY

st = {1, 2, 3, 4, 5}
type(st.toddb())
// output: dolphindb.SET.INT
```

