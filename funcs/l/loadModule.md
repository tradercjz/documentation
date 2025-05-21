# loadModule

## 语法

`loadModule(name, [moduleDir])`

## 参数

**name** 是一个字符串，表示模块的名称。

**moduleDir** 是一个字符串，表示模块 dos 文件或 dom 文件所在的目录。

## 详情

将模块或插件中的函数加载成系统的内置函数。如果加载的模块依赖了其他模块，系统会一并加载其他模块。该函数必须要用户登录后才能执行。

系统启动时，根据配置项 *moduleDir* 的设置，寻找并决定模块所在目录：

* 配置项 *moduleDir* 设置为一个绝对目录，则该目录即为搜索模块所在的目录。
* 配置项 *moduleDir* 设置为一个相对目录，系统会依次在
  *HOMEDIR*，*WORKDIR* 和 *EXECDIR* 三个目录下搜索。如果找到了，就以该目录作为
  *moduleDir*；如果搜索不到，就以 *<HOMEDIR>* + “/” +
  *<moduleDir>* 作为 modules 的绝对目录
* 配置项 *moduleDir* 没有设置，搜索方式同相对目录。

如果 *modules* 目录中包含同名的 dos 文件和 dom 文件，系统仅会加载 dom 文件。

注： 该函数只能在系统的初始化脚本（默认为 *dolphindb.dos* 文件）中使用。

`loadModule` 函数与配置参数 *preloadModules*
的功能相同。

## 例子

例1. 加载模块

```
loadModule("ta");

loadModule("system::log::fileLog");
```

例2. 加载插件

```
loadModule("plugins::mysql");

loadModule("plugins::odbc");
```

**相关信息**

* [saveModule](../s/saveModule.html "saveModule")

