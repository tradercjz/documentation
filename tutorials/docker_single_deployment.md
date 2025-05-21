# 基于 Docker 部署 DolphinDB

Docker 只是轻量化的资源隔离，DolphinDB 部署在 Docker 环境和非 Docker 环境下的运行性能差异不明显，可根据业务需求选择合适的运行环境。本文介绍如何使用 Docker 部署一个社区版/企业版 DolphinDB 单机服务。

## 环境准备

* 安装 Docker

  Docker 可以方便地在 Linux /MAC/Windows 平台安装，安装方法请参考 [Docker 官方文档](https://www.docker.com/products/docker)。
* 拉取 DolphinDB 的 Docker 镜像

  最新 Docker 镜像可以通过 [Docker 官方镜像仓库](https://hub.docker.com/u/dolphindb) 获取，以 tag 为 v2.00.5 为例：

  ```
  docker pull dolphindb/dolphindb:v2.00.5
  ```

  注意：本文基于 v2.00.5 版本编写，文中涉及的版本号请根据实际使用的版本进行相应调整。
* 主机信息

  | 主机名 | IP | 部署服务 | 数据盘挂载 |
  | --- | --- | --- | --- |
  | host1 | xxx.xxx.xx.xx | dolphindb | /ddbdocker |

## 快速体验

### Docker（X86 架构版）

* 登录机器执行以下脚本，创建一个 Docker 容器：

  ```
  docker run -itd --name dolphindb \
    --hostname host1 \
    -p 8848:8848 \
    -v /etc:/dolphindb/etc \
    dolphindb/dolphindb:v2.00.5 \
    sh
  ```
* 参数解释:

  + `--hostname`: 容器的主机名称（用于采集指纹制作企业版 Licence）

    > 可通过 `hostname` shell 命令查看主机名称。
  + `-p`：其中前一个 8848 端口为宿主机端口，后一个 8848 端口为映射到 DolphinDB 容器中的端口（DolphinDB 单机版默认端口）。启动后可通过本机 8848 端口访问 DolphinDB。
  + `-v`：表示使用映射宿主机的 `/etc`目录到容器中的 /dolphindb/etc 路径，用于采集指纹制作企业版 License。
  + `--name`：为容器名。指定容器名以便对该容器进行相关操作，例如，通过容器名查看容器相关信息等。若不指定，Docker 会随机分配一个容器名。
  + `dolphindb/dolphindb:v2.00.5`：必填参数，用于指定构建容器的镜像。镜像名称必须完整（包含dolphindb仓库及版本信息），例如：dolphindb/dolphindb:v2.00.5
* 检测容器是否成功构建

  执行如下命令

  ```
  docker ps|grep dolphindb
  ```

  期望输出

  ```
  347bfa54df86   dolphindb/dolphindb:v2.00.5   "sh -c 'cd /data/ddb…"   20 seconds ago   Up 19 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   dolphindb
  ```
* 客户端连接 DolphinDB 进行测试。

  详细教程参考[使用客户端](../db_distr_comp/clients.html)

### Docker(ARM架构)

登录机器执行以下脚本，创建一个 Docker 容器：

```
docker run -itd --name dolphindb \
  --hostname cnserver10 \
  -p 8848:8848 \
  -v /etc:/dolphindb/etc \
  dolphindb/dolphindb-arm64:v2.00.7 \
  sh
```

参数解释:

* `--hostname`：容器的主机名称（用于采集指纹制作企业版 License）
* `-p`：其中前一个 8848 端口为宿主机端口，后一个8848端口为映射到 DolphinDB容器中的端口（DolphinDB 单机版默认端口）。启动后可通过本机 8848 端口访问 DolphinDB。
* `-v`：表示使用映射宿主机的 `/etc`目录到容器中的 /dolphindb/etc 路径，用于采集指纹制作企业版 License。
* `--name`：为容器名。指定容器名以便对该容器进行相关操作，例如，通过容器名查看容器相关信息等。若不指定，Docker 会随机分配一个容器名。
* `dolphindb/dolphindb-arm64:v2.00.7`：必填参数，用于指定构建容器的镜像。镜像名称必须完整（包含dolphindb仓库及版本信息），例如：dolphindb/dolphindb-arm64:v2.00.7

检测容器是否成功构建

执行如下命令

```
docker ps|grep dolphindb
```

期望输出

```
347bfa54df86   dolphindb/dolphindb-arm64:v2.00.7   "sh -c 'cd /data/ddb…"   20 seconds ago   Up 19 seconds   0.0.0.0:8848->8848/tcp, :::8848->8848/tcp   dolphindb
```

客户端连接 DolphinDB 进行测试。

详细教程参考[使用客户端](../db_distr_comp/clients.html)

## 生产环境部署建议

以下内容以 X86 架构版为例。

### 在线部署

* 登录机器执行 shell 脚本，下载安装包并配置容器映射文件，以 v2.00.5 为例

  ```
  git clone --depth=1 https://github.com/dolphindb/dolphindb-k8s && \
  cd dolphindb_k8s/docker-single && \
  sh map_dir.sh
  ```

**注意**：由于新建的目录是 `/ddbdocker`，可能遇到用户新建权限问题，需自行修改可以用户可以创建权限的文件夹 -->

执行下面命令：

```
tree /ddbdocker
```

期望输出：

```
├── ddbdocker
│   ├── data
│   ├── ddb_related
│   │   ├── dolphindb.cfg
│   │   └── dolphindb.lic
│   └── plugins
│       ├── hdf5
│       │   ├── libPluginHdf5.so
│       │   └── PluginHdf5.txt
│       ├── mysql
│       │   ├── libPluginMySQL.so
│       │   └── PluginMySQL.txt
│       ├── odbc
│       │   ├── libPluginODBC.so
│       │   └── PluginODBC.txt
│       └── parquet
│           ├── libPluginParquet.so
│           └── PluginParquet.tx
```

文件夹说明如下：

| 文件（夹）名 | 文件（夹）用途 | 宿主机映射路径 | 容器映射路径 |
| --- | --- | --- | --- |
| dolphindb.cfg | 单节点模式下的 DolphinDB 配置文件 | /ddbdocker/ddb\_related/dolphindb.cfg | /data/ddb/server/dolphindb.cfg |
| dolphindb.lic | DolphinDB 的证书文件（企业版的需要联系工程师） | /ddbdocker/ ddb\_related/dolphindb.lic | /data/ddb/server/dolphindb.lic |
| plugins | 存储 DolphinDB 插件 | /ddbdocker/plugins | /data/ddb/server/plugins |
| data | 用来存储 DolphinDB 数据节点相关文件（例如元数据，流数据，数据表等） | /ddbdocker/data | /data/ddb/server/data |

执行下面命令启动容器：

```
docker run -itd --name dolphindb \
-p 8848:8848 \
--ulimit nofile=1000000:1000000 \
  -v /etc:/dolphindb/etc \
  -v /ddbdocker/ddb_related/dolphindb.cfg:/data/ddb/server/dolphindb.cfg \
  -v /ddbdocker/ddb_related/dolphindb.lic:/data/ddb/server/dolphindb.lic \
  -v /ddbdocker/plugins:/data/ddb/server/plugins \
  -v /ddbdocker/data:/data/ddb/server/data \
  dolphindb/dolphindb:v2.00.5 \
  sh \
  -stdoutLog 1
```

预期输出容器 id`3cdfbab788d0054a80c450e67d5273fb155e30b26a6ec6ef8821b832522474f5`。

* 使用 DolphinDB 客户端连接 DolphinDB 进行测试

  详细教程参考[使用客户端](../db_distr_comp/clients.html)

### 离线部署

* 在DolphinDB官网下载并安装对应版本的 DolphinDB server 安装镜像包。
* 在下载的 zip 压缩包的同目录添加 shell 脚本 `map_dir.sh`，内容如下：

  ```
  #!/bin/bash
  set -e
  clear
  #创建用于存储相应文件（夹）的空白目录
  dir1=/ddbdocker
  dir2=/ddbdocker/ddb_related

  if [ ! -e "$dir1" ];
  then
      mkdir $dir1
  fi

  if [ ! -e "$dir2" ];
  then
      mkdir $dir2
  fi

  #获取安装包
  ddb_zip=$(ls ./DolphinDB_Linux64_V*.zip)
  ddb_name=$(basename $ddb_zip .zip)

  if [ -e $ddb_zip ];
  then
      echo -e "上传软件安装包成功" "\033[32m UpLoadSuccess\033[0m"
  else
      echo -e "无法找到安装包，请上传至该目录" "\033[31m UpLoadFailure\033[0m"
      echo ""
      sleep 1
      exit
  fi
  #解压安装包
  unzip "${ddb_zip}" -d "${ddb_name}"
  if [ -d ./$ddb_name ];then
      echo -e "解压软件安装包成功" "\033[32m UnzipSuccess\033[0m"
  else
      echo -e "解压安装包失败，请检查安装包是否下载完整" "\033[31m UnzipFailure\033[0m"
      echo ""
      sleep 1
      exit
  fi

  #获取相应路径下的源和目标文件（夹）
  source_f1=./${ddb_name}/server/dolphindb.cfg
  source_f2=./${ddb_name}/server/dolphindb.lic
  source_dir4=./${ddb_name}/server/plugins

  f1=/ddbdocker/ddb_related/dolphindb.cfg
  f2=/ddbdocker/ddb_related/dolphindb.lic
  dir3=/ddbdocker/data
  dir4=/ddbdocker/plugins

  #编写函数对各目标路径进行遍历并通过设置条件语句来判断是否要对已有的文件进行覆盖
  function isCovered() {

  for i in $*;
  do
      if [ -e $i ];
      then
          #echo $i
          read -p "The $i has already existed, would you want to recover or clean it and other similar ones?(y/n)" answer
          if [ $answer=="y" ];
          then
              break
          else
              echo ""
              sleep 1
              exit
          fi
      fi
  done
  }

  isCovered $f1 $f2 $dir3 $dir4

  #进行相应文件（夹）的拷贝
  cp -rpf $source_f1 $f1
  cp -rpf $source_f2 $f2

  if [ -e "$dir3" ];
  then
      rm -rf $dir3
  fi

  mkdir $dir3
  cp -rpf $source_dir4 $dir4

  #删除解压的安装包
  rm -rf ./${ddb_name}

  ```
* 执行 shell 脚本，构建数据映射目录

  ```
  sh map_dir.sh && tree /ddbdocker
  ```

期望输出：

```
├── ddbdocker
│   ├── data
│   ├── ddb_related
│   │   ├── dolphindb.cfg
│   │   └── dolphindb.lic
│   └── plugins
│       ├── hdf5
│       │   ├── libPluginHdf5.so
│       │   └── PluginHdf5.txt
│       ├── mysql
│       │   ├── libPluginMySQL.so
│       │   └── PluginMySQL.txt
│       ├── odbc
│       │   ├── libPluginODBC.so
│       │   └── PluginODBC.txt
│       └── parquet
│           ├── libPluginParquet.so
│           └── PluginParquet.tx
```

文件夹说明如下：

| 文件（夹）名 | 文件（夹）用途 | 宿主机映射路径 | 容器映射路径 |
| --- | --- | --- | --- |
| dolphindb.cfg | 单节点模式下的 DolphinDB 配置文件 | /ddbdocker/ddb\_related/dolphindb.cfg | /data/ddb/server/dolphindb.cfg |
| dolphindb.lic | DolphinDB 的证书文件（企业版的需要联系工程师） | /ddbdocker/ ddb\_related/dolphindb.lic | /data/ddb/server/dolphindb.lic |
| plugins | 存储 DolphinDB 插件 | /ddbdocker/plugins | /data/ddb/server/plugins |
| data | 用来存储 DolphinDB 数据节点相关文件（例如元数据，流数据，数据表等） | /ddbdocker/data | /data/ddb/server/data |

执行下面命令启动容器：

```
docker run -itd --name dolphindb \
  -p 8848:8848 \
  --ulimit nofile=1000000:1000000 \
  -v /etc:/dolphindb/etc \
  -v /ddbdocker/ddb_related/dolphindb.cfg:/data/ddb/server/dolphindb.cfg \
  -v /ddbdocker/ddb_related/dolphindb.lic:/data/ddb/server/dolphindb.lic \
  -v /ddbdocker/plugins:/data/ddb/server/plugins \
  -v /ddbdocker/data:/data/ddb/server/data \
  dolphindb/dolphindb:v2.00.5 \
  sh \
  -stdoutLog 1
```

预期输出容器 id`3cdfbab788d0054a80c450e67d5273fb155e30b26a6ec6ef8821b832522474f5`。

* 使用 DolphinDB 客户端连接 DolphinDB 进行测试

  详细教程参考[使用客户端](../db_distr_comp/clients.html)

## 常见问题

### 如何自定义配置文件

在宿主机上找到映射的 DolphinDB 配置文件 dolphindb.cfg，此处的路径为/ddbdocker/ddb\_related/dolphindb.cfg，其文件内容如下：

```
localSite=localhost:8848:local8848
mode=single
maxMemSize=32
maxConnections=512
workerNum=4
localExecutors=3
dataSync=1
chunkCacheEngineMemSize=2
newValuePartitionPolicy=add
maxPubConnections=64
subExecutors=4
subPort=8849
lanCluster=0
```

* 重要参数解释:

  + `localSite`: 节点的局域网信息，格式为 host:port:alias。单实例中默认值为 localhost:8848:local8848。其中8848为 DolphinDB 运行的端口号，必须填写。
  + `workerNum`: 常规作业的工作线程的数量，决定了节点最大并发前台作业数。默认值是 CPU 的内核数。
  + `localExecutors`: 本地执行线程的数量，决定了节点最大并发子任务数。默认值是 CPU 的内核数-1。
  + `maxMemSize`：分配给 DolphinDB 的最大内存空间（以 GB 为单位）。如果该参数设为0，表明 DolphinDB 的内存使用没有限制。建议设置为比机器内存容量低的一个值。

### 如何升级版本

执行如下命令拉取新版本的 DolphinDB 镜像，下例拉取的镜像为 2.00.6 版本：

```
  docker pull dolphindb/dolphindb:v2.00.6
```

执行下列命令，进行升级:

```
  docker run -itd --name dolphindb \
    -p 8848:8848 \
    --ulimit nofile=1000000:1000000 \
    -v /etc:/dolphindb/etc \
    -v /ddbdocker/ddb_related/dolphindb.cfg:/data/ddb/server/dolphindb.cfg \
    -v /ddbdocker/ddb_related/dolphindb.lic:/data/ddb/server/dolphindb.lic \
    -v /ddbdocker/plugins:/data/ddb/server/plugins \
    -v /ddbdocker/data:/data/ddb/server/data \
    dolphindb/dolphindb:v2.00.6 \
    sh \
    -stdoutLog 1
```

DolphinDB 升级只是替换二进制安装包，需要保留之前版本的 `dolphindb.cfg`（DolphinDB 的配置）, `dolphindb.lic`（DolphinDB 的证书文件）, `plugins`（DolphinDB 内置的插件）, `data`（DolphinDB 内置的数据文件等）目录，以保证配置不更改和数据不丢失。

**注意**：

1. 由于 Docker 容器名要求唯一，如果之前的容器依旧保留，则新容器名必须要和之前的容器名不同；
2. 需要注意端口号不被占用。

通过 GUI 连接该节点，执行以下命令查看版本信息，检查升级是否成功。

```
  version()
```

期望输出:

```
  2.00.6
```

### 报错及解决方案

* 报错信息如下

  ```
  Can't find time zone database. Please use parameter tzdb to set the root directory of time zone database.
  ```

  解决方案：
  若 Docker 镜像中不包含 `tzdata` 包，比如 `ubuntu:latest`，会导致 DolphinDB 启动报如上错误，执行下述命令安装 `tzdata` 包：

  ```
  apt-get install tzdata
  ```
* 报错信息如下

  ```
  <ERROR> : Failed to retrieve machine fingerprint
  ```

  解决方案：
  由于正式 License 需要校验服务器硬件信息，而 Docker 没有权限获取此信息，启动时日志中会报告上述异常。需在 `docker run` 添加如下启动参数：

  ```
  -v /etc:/dolphindb/etc
  ```
* 报错信息如下

  ```
  docker: Error response from daemon: driver failed programming external connectivity on endpoint dolphindb (178a842284d64fbe128ff3f1188ead76ef4072c9149226f8bf62dc7795a58603): Error starting userland proxy: listen tcp4 0.0.0.0:8848: bind: address already in use.
  ```

  解决方案：更换宿主机的端口号，或用如下命令查看端口号占用情况：

  ```
  lsof -i:8848
  COMMAND     PID USER   FD   TYPE    DEVICE SIZE/OFF NODE NAME
  dolphindb 17238 root    6u  IPv4 231927135      0t0  TCP *:8848 (LISTEN)
  ```

