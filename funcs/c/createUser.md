# createUser

## 语法

`createUser(userId, password, [groupIds], [isAdmin=false],
[authMode])`

## 详情

创建用户。

*groupIds* 表示的组必须是已经创建了的组。

注： 该函数只能由管理员运行。

## 参数

**userId**
是表示用户名的字符串。它只能包含字母、下划线或数字，并且它不能以数字或下划线开头。长度不能超过30个字符。

**password** 是表示用户密码的字符串。它不能包含空格或控制字符。

从 2.00.10.10 开始，用户可以通过配置项 *enhancedSecurityVerification*
控制是否对 password 进行复杂性校验。若不设置 *enhancedSecurityVerification*，则不校验；若设置
*enhancedSecurityVerification*=true，则要求密码必须满足以下条件：

* 字符个数为8~20
* 至少包含一个大写字母
* 至少包含以下字符之一：!"#$%&'()\*+,-./:;<=>?@[]^\_`{|}~。

**groupIds** 可选参数，是表示用户所属组的字符串标量或向量。

**isAdmin** 可选参数，是表示用户是否为管理员的布尔值。

**authMode** 可选参数，指定该用户的登录认证方式。默认为”sha256”，即用户通过 `login` 函数登录，使用
SHA-256 算法认证。另支持指定为”scram”，使用 SCRAM (Salted Challenge Response Authentication
Mechanism) 协议登录。

注：

* SCRAM 基于 [IETF's RFC 5802
  标准](https://datatracker.ietf.org/doc/html/rfc5802)实现，通过高强度的哈希算法，双向验证等措施，为用户通过密码登录的方式提供更高的安全性。
* DolphinDB 的 API 已支持 SCRAM 认证方式：
  + 通过 API 的原生方法连接 DolphinDB 服务器时， API 端将优先采用 SCRAM 方式登录。
  + 如该用户未启用 SCRAM 认证，则自动回退至默认登录方式。
* 若不使用 API 提供的封装好的接口，自行使用 SCRAM 登录时，需调用 DolphinDB 服务端函数 scramClientFirst
  和 scramClientFinal。具体流程与配置要求请见对应函数文档。
* 启用 SCRAM 认证后，`login`, `resetPwd`,
  `changePwd` 等密码相关函数仍然有效。

## 例子

创建一个名称为 "JohnSmith"，密码为 'Qb0507#$' 的非管理员用户，登录时默认使用 SHA-256
算法进行认证。该用户属于组 "research" 和组 "production"。

```
createUser(`JohnSmith, "Qb0507#$", `research`production);
```

