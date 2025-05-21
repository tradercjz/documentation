# getEnv

## 语法

`getEnv(name, [default])`

## 参数

**name** 是字符串标量，表示环境变量名称。

**default** 是字符串标量，表示不存在对应的环境变量时返回的默认值。如果没有指定 default，默认值为空字符串。

## 详情

返回指定环境变量的值。如果环境变量不存在，则返回 default 参数。

## 例子

```
getEnv("path")
```

返回：C:\ProgramData\DockerDesktop\version-bin;C:\Program
Files\Docker\Docker\Resources\bin;

```
getEnv("JAVA_HOME");
```

返回：C:\Program Files\Java\jdk1.8.0\_191

```
getEnv("not_exist","not exist")
```

返回：`not exist`

