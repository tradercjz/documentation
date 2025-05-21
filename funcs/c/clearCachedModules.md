# clearCachedModules

## 语法

`clearCachedModules()`

## 参数

无

## 详情

清除缓存的 module。更新 module 文件后，通过该命令清除 module 缓存，执行 use 语句时，会重新从文件加载
module，无需重启节点。

注： 只有管理员（admin）才能执行该命令。

## 例子

定义并导入一个 module

```
module printLog
def printLog(){
print "hello"
}
```

加载模块

```
use printLog
printLog()
// output
hello
```

修改 module

```
module printLog
def printLog(){
print "hello new"
}
```

再次加载模块前，需要调用 `clearCachedModules` 以清除之前缓存的
module。

```
login("admin", "123456")

clearCachedModules();

use printLog
printLog()
// output
hello new
```

