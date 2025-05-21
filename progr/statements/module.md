# module

在DolphinDB中，模块是指只包含函数定义的脚本文件。当需要调用一个特定的函数时，可以通过调用含有该函数的模块来实现。通过module语句声明一个模块，该语句位于模块文件的第一行。

模块按层组织。命名结构必须与目录结构相一致。在下面模块声明的例子中，module语句放在了模块文件的首行。

```
module example::ch9
```

上述例子中，模块文件路径为<包的根目录>/example/ch9.dos，包的根目录位于<DolphinDB目录>/modules。

我们使用.dos作为模块文件的后缀，是"dolphin script"的缩写。

相关语句：[use](use.html)

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
