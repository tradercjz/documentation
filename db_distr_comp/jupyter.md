# Jupyter Notebook 客户端

Jupyter Notebook
是基于网页的用于交互计算的应用程序，可被应用于全过程计算：开发、文档编写、运行代码和展示结果。用户可以直接通过浏览器编辑和交互式运行代码。DolphinDB database
提供了Jupyter Notebook 的插件。

DolphinDB Jupyter Notebook 扩展插件提供以下功能：

* 为用户提供 Jupyter Notebook 连接DolphinDB Server 的配置界面。
* 使 Jupyter Notebook 支持 DolphinDB 脚本语言的执行。

## 下载安装

* 在命令行中，首先使用pip安装 DolphinDB Jupyter Notebook 插件：

  ```
  pip install dolphindb_notebook
  ```

* 安装完成后启用插件：

  ```
  jupyter nbextension enable dolphindb/main
  ```

## 插件配置

Jupyter Notebook内核（kernels）是编程语言特定的进程，它们独立运行并与Jupyter应用程序及其用户界面进行交互。DolphinDB Jupyter
Notebook 扩展插件提供了运行DolphinDB脚本的内核。用户需要通过以下步骤配置Jupyter
Notebook的工作路径，以便在程序运行时DolphinDB内核能够顺利导入。

* 通过命令行`jupyter kernelspec list`查看Jupyter
  Notebook Kernel的工作路径
  + Linux系统

    ```
    >jupyter kernelspec list
    Available kernels:
        dolphindb   /home/admin/.local/share/jupyter/kernels/dolphindb
        python3       /home/admin/.local/share/jupyter/kernels/python3
    ```

  将/home/admin/.local/share/jupyter/kernels复制下来，方便下一步配置时粘贴。

  + Windows系统

    ```
    >jupyter kernelspec list
    Available kernels:
        dolphindb   C:\Users\admin\appdata\local\programs\python3\python37\share\jupyter\kernels\dolphindb
        python3       C:\Users\admin\appdata\local\programs\python3\python37\share\jupyter\kernels\python3
    ```

  将
  C:\Users\admin\appdata\local\programs\python3\python37\share\jupyter\kernels复制下来，方便下一步配置时粘贴。
* 通过命令行 `jupyter notebook
  --generate-config`生成一个配置文件jupyter\_notebook\_config.py，打开这个配置文件，找到c.NotebookApp.notebook\_dir选项，设为上一步复制下来的工作路径，并去掉注释#。

  注： Windows系统中，需要将路径中的一个反斜杠\都替换成两个反斜杠\\，因为一个反斜杠\会被系统误认为是转义字符。

## 连接服务器

* 在命令行输入 `jupyter notebook`，启动Jupyter Notebook。
* 在Jupyter Notebook的页面右侧点击新建，选择DolphinDB，新建一个DolphinDB notebook。
* 点击notebook工具栏的 Connect to DolphinDB Server
  按钮。选择相应的server，然后点击右下角Connect按钮，即与DolphinDB
  server建立连接（如果不需要该server，可以点击Delete按钮删除）。
* 也可以通过New按钮，输入新的server信息，然后点击Save & Connect按钮即与DolphinDB
  server建立连接，并保存该信息以便下次使用。

## 编辑和运行脚本

连接DolphinDB
Server后，在代码块区域编写DolphinDB脚本，点击运行即可运行相应代码块。每次运行DolphinDB脚本后，运行结果都会在相应的代码块下方展示。对于DolphinDB的绘图功能，以PNG展示结果。

注：

* 对于一些数据量较大的结果，可能会出现IOPub数据率超出限制的问题，可以启用Jupyter
  Notebook配置文件中的c.NotebookApp.iopub\_data\_rate\_limit一项，去掉注释符号后，按需调高数值。
* 对于超出60行的表格，只显示前五行与后五行。

