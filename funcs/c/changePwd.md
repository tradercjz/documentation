# changePwd

## 语法

`changePwd(oldPwd, newPwd)`

## 参数

**oldPwd** 表示用户旧密码的字符串。

**newPwd** 表示用户新密码的字符串。它不能包含空格或控制字符。

从 2.00.10.10 开始，用户可以通过配置项 *enhancedSecurityVerification*
控制是否对 newPwd 进行复杂性校验。若不设置 *enhancedSecurityVerification*，则不校验；若设置
*enhancedSecurityVerification*=true，则要求新密码必须满足以下条件：

* 字符个数为8~20
* 至少包含一个大写字母
* 至少包含以下字符之一：!"#$%&'()\*+,-./:;<=>?@[]^\_`{|}~。

注： 该函数只能在控制节点、数据节点和计算节点运行。

## 详情

修改用户密码。

## 例子

```
changePwd("LTmp4389.", "T5139pm.");
```

