# This is a comment
print("Hello, World!")
```

多行注释用三个单引号 ''' 或者三个双引号 """ 将注释括起来，例如:

```
'''
This is the first comment
This is the second comment
This is the third comment
'''
print("Hello, World!")
```

## 模块

DolphinDB 的模块文件以 .dos 作为后缀，位于“<DolphinDB目录>/modules”下。DolphinDB Session 使用 use 引用模块文件。

Python Parser 的模块文件以 .py 作为后缀，位于“<DolphinDB目录>/python”或用户自定义的路径（需使用 sys.path 设置路径）下。若使用自定义路径，则需要重启 server 后，才可在 Python Session 中通过 import 引用这些模块。

首先，在 "<DolphinDB目录>/python" 下创建一个 mod\_test.py 的模块文件；

```
def f():
  a = 10
  b = 15
  return a + b
```

通过 `import` 导入模块：

```
import mod_test
mod_test.f()

// output: 16
```

或通过 `from..import..` 导入模块内的某个函数：

```
from mod_test f
f()
// output: 16
```

若模块放在其它路径，则需通过 sys 设置模块的搜索路径：

```
import sys
sys.path.append("/path/to/module")
```

清除模块：

```
undef("mod_test")
```

