# method2: dict(iterable, **kwarg)
d1 = dict([('one', 1), ('two', 2), ('three', 3)])
type(d1)
// output: dict
```

## 访问字典里的值

通过键（key）来访问字典里的值。

```
d['C']
// output: [1,2,3]

d.values()
```

## 更新字典

1. 更新数据

   ```
   d['B'] = 2022.01.01
   d
   // output: {'A': 12, 'B': 2022.01.01, 'C': [1, 2, 3]}

   d2 = {'A':15, 'D':`YES}
   d.update(d2)
   d
   // output: {'A': 15, 'B': 2022.01.01, 'C': [1, 2, 3], 'D': 'YES'}
   ```
2. 追加数据

   ```
   d = {'A':12, 'B':`halo, 'C': [1,2,3]}
   d['D'] = ("math", "chinese", [90, 80])
   d
   // output: {'A': 12, 'B': 'halo', 'C': [1, 2, 3], 'D': ('math', 'chinese', [90, 80])}
   ```
3. 删除数据

   ```
   d = {'A':12, 'B':`halo, 'C': [1,2,3]}
   d.pop('A')  # 通过键，删除指定键值对
   // output: 12
   d
   // output: {'B': 'halo', 'C': [1, 2, 3]}

   d.clear()
   d
   // output: {}
   ```

## 字典可用的所有属性和方法

```
dir(d)
// output: ['__dir__', '__eq__', '__getitem__', '__init__', '__iter__', '__len__', '__ne__', '__repr__', '__req__', '__rne__', '__str__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'setdefault', 'toddb', 'update', 'values']
```

其中 `toddb` 是 Python Parser 中特有的方法。当一个字典对象的 key 满足以下条件时：所有 key 的类型相同，且不能是 DOUBLE 或 FLOAT 类型，可以通过 `toddb` 将其转换成 DolphinDB 的字典。

```
d = {'A': 12, 'B': 2022.01.01, 'C': [1, 2, 3]}
type(d.toddb())
// output: dolphindb.DICTIONARY.STRING

d = {1: 12, 2: 2022.01.01, 3: [1, 2, 3]}
type(d.toddb())
// output: dolphindb.DICTIONARY.INT
```

