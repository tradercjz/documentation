# hmac

## 语法

`hmac(key, message, [digest='sha256'])`

## 参数

**key** LITERAL 类型标量，表示密钥。

**message** LITERAL 类型标量，表示需要加密的信息。

**digest** 可选参数，STRING 类型标量，表示加密使用的哈希算法。默认值为 sha256。可选值为 sha1, sha224, sha256, sha
384, sha512, md5。

## 详情

采用 HMAC（Hash-based Message Authentication
Code，基于哈希的消息认证码）机制，根据给定的密钥和加密信息，通过指定的加密算法生成并返回一个 STRING 类型的哈希值。

## 例子

```
hmac(key="myKey", message="myMessage", digest="sha256")
// output:'71e5f5ca5f64550ee4524909f7cead7b81d8674a657383aec1b003a8a3f05b04'

hmac(key="myKey", message="myMessage", digest="sha1")
// output:'5033197fa89dedf5088eed6100dfa5a0f67ef1ce'

hmac(key="myKey2", message="myMessage", digest="sha256")
// output:'40e2a700754cec30ace1e82abfe7fd233f8f6c299050cc21b0e0a4ea42428126'
```

