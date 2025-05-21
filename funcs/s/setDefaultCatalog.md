# setDefaultCatalog

## 语法

`setDefaultCatalog(catalog)`

## 参数

**catalog** 字符串标量，表示 catalog 的名称。若为空，则表示重置当前 catalog 空间为初始状态，即无默认 catalog。

## 详情

为当前 session 设置默认的 catalog。

## 例子

```
getCurrentCatalog()
// 返回为空

createCatalog("cat1")
setDefaultCatalog("cat1")
getCurrentCatalog()
// Output: cat1

setDefaultCatalog("")
getCurrentCatalog()
// 返回为空
```

