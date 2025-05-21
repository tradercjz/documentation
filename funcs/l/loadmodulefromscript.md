# loadModuleFromScript

## 语法

`loadModuleFromScript(moduleNamespace, moduleScript,
[reload=false])`

## 参数

**moduleNamespace**：字符串标量或向量，表示模块的命名空间。如果模块之间存在依赖，则需要输入全部模块的命名空间。

**moduleScript**：字符串标量或向量，表示模块的脚本。

**reload**：布尔标量，表示是否重新加载模块,默认值为 false。如果之前已加载同名模块，要使更新的 *moduleScript*
生效，必须将此参数设置为 true。

## 详情

解析包含模块定义的字符串，并加载该模块。如果模块脚本中包含模块引用，则无需关注其依赖顺序，函数会自动解析。

## 例子

```
moduleName = "test"
moduleScript = "module test \n def testFunc(x,y){ return x+y }"
loadModuleFromScript(moduleName,moduleScript)
go
test::testFunc(2,3)
// output
5
```

如果模块脚本中包含模块引用：

```
moduleNames = ["test2","test1"]
moduleScripts = [
"module test2
use test1
def func4(x,y){
    return func1(x) + func2(y)
}
",
"module test1
def func1(x){
    return x+1
}
def func2(x){
    return x+2
}
def func3(x){
    print(func1(x)+func2(x))
}
"
]
loadModuleFromScript(moduleNames,moduleScripts)
go
test1::func3(2)
// output
7
test2::func4(2,3)
// output
8
```

