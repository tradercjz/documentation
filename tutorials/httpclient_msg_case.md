# 利用 HttpClient 插件整合外部消息

DolphinDB 支持通过动态加载用 C++ 编写的插件程序，通过执行 DolphinDB 脚本函数，来调用插件程序的自定义函数，实现自定义功能扩展。

DolphinDB 的 httpClient插件提供以下 3 个函数，用于发送 HTTP 请求和发送邮件。

* `httpGet`: 发送http的Get方法请求。
* `httpPost`: 发送http的Post方法请求。
* `sendEmail`: 发送邮件。

本文介绍如何通过 httpClient 插件的 `httpGet` 与 `httpPost` 插件函数实现企业微信发送群聊消息、钉钉发送群聊消息，通过 `sendEmail` 插件函数发送文本邮件。

## 在 DolphinDB 中加载 httpClient 插件

### Linux

需要有 libPluginHttpClient.so 和 PluginHttpClient.txt 两个插件程序文件。

注：可以在[httpClient 插件项目](https://gitee.com/dolphindb/DolphinDBPlugin/tree/release200/httpClient)的 /bin/linux/ 目录下找到这两个文件，但需要注意分支版本号需要与所用的 DolphinDB server 版本相同。

确认 PluginHttpClient.txt 和 libPluginHttpClient.so 在同一目录下，执行以下脚本来加载插件：

```
loadPlugin("<PluginDir>/httpClient/bin/linux64/PluginHttpClient.txt");
```

## 三种外部消息平台的使用

### 企业微信消息通信的演示案例

以下我们演示一个企业微信发送群聊应用信息的案例。创建一个企业群聊，然后发送群聊信息。

**注意**：

* 如果已经有一个群聊并且有群聊标识id，则不需要创建群聊。群聊标识号一定需要通过创建群聊获取。
* 如果需要创建一个企业群聊，需要设置应用的可见范围为根部门。
* 在企业微信中，调用不同的http请求API都需要有不同的的请求地址(url)。

参考：[企业微信corpid、userid、部门id、tagid、agentid、secret、access\_token](https://work.weixin.qq.com/api/doc/90000/90135/90665)

#### 企业微信内自建新应用

[链接](https://work.weixin.qq.com/api/doc/90000/90135/90226)

* 首先,添加自建应用。管理员账号登录 [企业微信管理端](https://work.weixin.qq.com/wework_admin/loginpage_wx?from=myhome_baidu) -> 应用与小程序 -> 应用 -> 自建，点击“创建应用”，设置应用logo、应用名称等信息，创建应用。
* 创建完成后，在管理端的应用列表里进入该应用，可以看到 Agentid、Secret 等信息，这些信息在使用企业微信 API 时会用到。

#### 获取 access\_token

[链接](https://work.weixin.qq.com/api/doc/90000/90135/91039)

* access\_token 是应用调用 API 的凭证，由 corpid 和 corpsecret 换取。
  **注意**：access\_token 的时效为 7200 秒。需要缓存 access\_token，用于后续接口的调用（不能频繁调用 gettoken 接口，否则会受到频率拦截）。当 access\_token 失效或过期时，可通过查看返回正文的 errocode 来确定，需要重新获取，应实现 access\_token 失效时重新获取的逻辑。
* 每个企业都拥有唯一的 corpid。
* 每个应用都有相应的 corpsecret，用对应应用的 corpsecret 获取的 access\_token 就拥有该应用的权限。
* 请求方式： GET（HTTPS）

  请求地址： https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET

这里使用 httpClient 插件函数 `httpGet(url,params,timeout,headers)`。当前步骤不需要添加 http 请求头，只填写前面 3 个参数。

* url 只需要填写 'https://qyapi.weixin.qq.com/cgi-bin/gettoken', 后面的 corpid 和 corpsecret 参数通过 httpGet 方法中的 param 参数就可以补充完整。
* param 是一个键值对都是 string 的字典。 参数 corpid 的值 (ID) 为企业 ID，corpsecret 的值 (SECRET) 为对应应用的凭证密钥，两个值都需要以字符串的形式加入到 param中。
* timeout 为超时时间，单位为毫秒，数据类型为整型。达到超时时间后 `httpGet` 会直接返回，无论是否收到 HTTP 应答报文。因为这是一个远程网络请求，超时时间最好设置为 1000 毫秒或以上。

示例：

填写参数 url：

```
url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken';
```

填写参数 param，ID 和 SECRET 都需要更换为真实的 corpid 和 corpsecret。

```
param=dict(string,string);
ID='xxxxx';
SECRET='xxxxx';
param['corpid']=ID;
param['corpsecret']=SECRET;
```

使用 `httpGet` 函数向企业微信发送请求：

```
ret=httpClient::httpGet(url,param,1000);
print ret['text'];
```

返回值 ret 是一个 dictionary，ret['text'] 是响应正文。如果请求成功，返回的 json 格式的正文 ret['text'] 如下：

```
{
    "errcode" : 0,
    "errmsg" : "ok",
    "access_token" : "xxxxxx",
    "expires_in" : 7200
}
```

**注意**：errcode 是向企业微信请求信息的错误码，如果请求成功，返回值是 0。不同于 HTTP 协议的请求返回的响应码。如果出现其他 errcode 值，查看错误信息 errmsg。errcode 的值的含义可查看 [企业微信错误码表](https://work.weixin.qq.com/api/doc/90000/90139/90313)。

这里我们使用：

```
body = parseExpr(ret.text).eval();
ERRCODE=body.errcode;
ERRMSG=body.errmsg;
```

就可以便捷地把 errcode 和 errmsg 解析出来。

access\_token 的值在后续步骤中会用到。如果 errcode 的值为 0，则可以获取到 access\_token。

```
ACCESS_TOKEN=body.access_token;
```

#### 发送应用消息

[链接](https://work.weixin.qq.com/api/doc/90000/90135/90248)

通过这个步骤，可以在企业微信内发送应用消息。
需要一个 access\_token 和一个应用 id(AgentId)。

请注意，如果返回的 json 正文的 errcode 的值为 40014，则表明 access\_token 过期了，需要重新重新获取 access\_token。

* 请求方式： POST（HTTPS）

  请求地址：https://qyapi.weixin.qq.com/cgi-bin/message/send?access\_token=ACCESS\_TOKEN

使用 httpClient 中的函数 `httpPost(url,params,timeout,headers)`。这里不需要添加 http 请求头，只填写前面 3 个参数。

请注意，相较于 HTTP 协议的 get 方法，post 方法的参数都是放在请求正文中的，httpPost 方法的 param 参数是填写在 http 报文中的正文部分。在这里，需要补充完整 url。

* 完整的 url：

  ```
  https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
  ```

  其中 ACCESS\_TOKEN 应该替换为需要发送消息应用的 access\_token，由第二个步骤获取。
* 参数都是以json的格式放在post请求正文中。

  ```
  {
     "touser" : "@all",
     "agentid" : xxxx,
     "msgtype" : "text",
     "text" : {
         "content" : "This is a test message"
     }
  }
  ```

  + touser：指定接收消息的成员，成员ID列表。这里我们使用特殊值"@all",只需要设置好这个应用的可见范围即可向特定的部门、接受人发送消息。
  + msgtype：消息类型。
  + agentid：企业应用的id，整型。
  + text：消息正文。

示例：

* 需要把ACCESS\_TOKEN更换成由第二个步骤获得的access\_token。
* 作为示例，我们这里发送的消息类型仅是文本信息，还可以有图片信息、视频信息、语音信息等等。

填写参数 url：

```
url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?';
ACCESS_TOKEN='xxxxx';
url+='access_token='+ACCESS_TOKEN;
```

填写参数 param：

```
param='{"touser" : "@all","agentid" : xxxx,"msgtype" : "text","text" : {"content" : "这是一条测试信息"}';
```

调用 `httpPost` 在企业微信发送应用消息：

```
ret=httpClient::httpPost(url,param,1000);
print ret['text'];
```

如果请求成功，企业微信返回的 json 格式正文如下：

```
{
   "errcode" : 0,
   "errmsg" : "ok",
}
```

**注意**：errcode 是向企业微信请求信息的错误码，如果请求成功，返回值是 0。不同于 HTTP 协议的请求返回的响应码。如果出现其他 errcode 值，查看错误信息 errmsg。errcode 的值的含义可查看 [企业微信错误码表](https://work.weixin.qq.com/api/doc/90000/90139/90313)。

可以通过以下dolphindb脚本从json格式字符串中取出errcode。

```
body = parseExpr(ret.text).eval();
ERRCODE=body.errcode;
```

**注意**：如果部分接收人无权限或不存在，发送仍然执行，但会返回无效的部分（即 invaliduser、invalidparty、invalidtag字段），需要设置应用的可见范围。

#### 发送群聊消息

##### 创建企业群聊

[链接](https://work.weixin.qq.com/api/doc/90000/90135/90245)

* 通过这个步骤，我们创建了一个企业群聊，可以获得一个群聊 id(chatid)。
* 设置应用的可见范围是根目录，没有设置会返回 errcode(60011)。可以到应用管理找到这个自建应用，单击这个应用，会跳转到这个应用的详情页面，可以在这个页面编辑这个应用的可见范围。
* 首先需要有由第二个步骤获得的 access\_token。

请注意，如果返回的 json 正文的 errcode 的值为 40014，则表明 access\_token 过期了，需要重新到第二个步骤重新获取 access\_token。

* 请求方式： POST（HTTPS）

  请求地址： https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access\_token=ACCESS\_TOKEN

  请求参数：http正文json格式

  ```
      {"name" : "NAME","owner" : "userid1","userlist" : ["userid1", "userid2", "userid3"],"chatid" : "CHATID"}
  ```

  这里使用 httpClient 中的函数 `httpPost(url,params,timeout,headers)`。当前步骤不需要添加 http 请求头，只填写前面 3 个参数。

  请注意，相较于http协议的 get 方法，post 方法的参数都是放在请求正文中的，httpPost 方法的 param 参数是填写在 http 报文中的正文部分。在这里，我们需要自行补充完整 url。
* url 需要填写 'https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access\_token=ACCESS\_TOKEN'。access\_token的值(ACCESS\_TOKEN)由第二个步骤获得。
* param 填写上面的 json 格式，每一个参数值都需要更替为实际参数。

  + name：群聊名字。
  + owner：群主id。
  + userlist：群成员id(userid)列表。每个成员都有唯一的userid。在企业微信网页，管理后台->“通讯录”->点进某个成员的详情页，可以看到。
  + chatid：群聊标识id。可以指定，也可以不填让系统随机创建，允许字符0-9及字母a-z和A-Z。
* timeout为超时时间，单位为毫秒，数据类型为整型。达到超时时间后`httpPost`会直接返回，无论是否收到http应答报文。因为这是一个远程网络请求，超时时间最好设置为1000毫秒或以上。

示例：

填写参数 url：

其中，ACCESS\_TOKEN 由第二个步骤获得，param 中每个参数都需要实际的参数。

```
url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/create?';
url+='access_token='+ACCESS_TOKEN;
```

填写参数param。"NAME","userid1","userid2","userid3","CHATID"都需要填写为实际的值。

```
param='{"name" : "NAME","owner" : "userid1","userlist" : ["userid1", "userid2", "userid3"]，"chatid" : "CHATID"}';
```

调用httpPost向企业微信发送创建群聊的请求：

```
ret=httpClient::httpPost(url,param,1000);
print ret['text'];
```

返回值ret是一个dictionary，ret['text']是响应正文。如果请求成功，返回的json格式的正文text如下：

```
 {
     "errcode" : 0,
     "errmsg" : "ok",
     "chatid" : "CHATID"
}
```

请注意，errcode 是向企业微信请求信息的错误码，如果请求成功，返回值是 0。不同于 http 协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[企业微信错误码表](https://work.weixin.qq.com/api/doc/90000/90139/90313)。

chatid 的值后面步骤需要用到。这里我们使用：

```
body = parseExpr(ret.text).eval();
ERRCODE=body.errcode;
CHATID=body.access_token;
```

就可以便捷地把 chatid 和 errcode 的值解析出来。

##### 利用 post 请求发送群聊消息

[链接](https://work.weixin.qq.com/api/doc/90000/90135/90248)

通过这最后一个步骤，我们就可以成功地在企业微信内发送群聊信息。
首先，需要一个 access\_token 还有一个群聊 id(chatid)，可以通过上一个步骤获得。

请注意，如果返回的 json 正文的 errcode 的值为 40014，则表明 access\_token 过期了，需要重新到上一个步骤重新获取access\_token。

* 请求方式： POST（HTTPS）

  请求地址： https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access\_token=ACCESS\_TOKEN

  使用httpClient中的函数httpPost(url,params,timeout,headers)。这里不需要添加http请求头，只填写前面3个参数。

  请注意，相较于http协议的get方法，post方法的参数都是放在请求正文中的，httpPost方法的param参数是填写在http报文中的正文部分。在这里，需要补充完整url。
* 完整的url：

  ```
  https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=ACCESS_TOKEN,
  ```

  其中ACCESS\_TOKEN应该替换为需要发送消息应用的access\_token，由第二个步骤获取。
* 参数都是以json的格式放在post请求正文中。

  ```
  {"chatid" : "CHATID","msgtype" : "text","text" : {"content" : "这是一条测试信息"}}
  ```

  + chatid：群聊id，可由上一个步骤获得。
  + msgtype：消息类型。
  + text：消息正文。

示例：

* 需要把ACCESS\_TOKEN更换成由第二个步骤获得的access\_token，CHATID更换成第上一个步骤通过创建群聊获得的chatid。
* 作为示例，我们这里发送的消息类型仅是文本信息，还可以有图片信息、视频信息、语音信息等等。

填写参数 url：

```
url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?';
ACCESS_TOKEN='xxxxx';
url+='access_token='+ACCESS_TOKEN;
```

填写参数 param：

```
param='{"chatid" : "CHATID","msgtype" : "text","text" : {"content" : "这是一条测试信息"}}';
```

调用 `httpPost` 向企业微信群聊发送消息：

```
ret=httpClient::httpPost(url,param,1000);
print ret['text'];
```

如果请求成功，企业微信返回的json格式正文类似如下：

```
{
    "errcode" : 0,
    "errmsg" : "ok",
    "invaliduser" : "",
    "invalidparty" : "1"
}
```

请注意，errcode 是向企业微信请求信息的错误码，如果请求成功，返回值是 0。不同于 HTTP 协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[企业微信错误码表](https://work.weixin.qq.com/api/doc/90000/90139/90313)。

可以通过以下dolphindb脚本从json格式字符串中取出 errcode。

```
body = parseExpr(ret.text).eval();
ERRCODE=body.errcode;
```

### 钉钉消息通信的演示案例

以下演示一个钉钉发送群聊应用信息的案例。创建一个企业群聊，然后发送群聊信息。

**注意**：

* 如果已经有一个群聊并且有群聊标识id，则不需要创建群聊。群聊标识号一定需要通过创建群聊获取。
* 调用不同的http请求API都需要有不同的的请求地址(url)。

相比于企业微信，钉钉的进行http的API调用的时候都需要以下的更多的如下操作。

* 开通相关的权限。
* 设置服务器的出口公网ip地址。
* 需要在创建一个群聊时需要多步单次调用多个接口，无法直接到网页端查到每个成员的UserId。首先通过部门查询，然后通过查询该部门下的成员信息得到UserId，最后通过UserId列表创建一个群聊。

[钉钉CorpId, UserId, UnionId, AppKey, AppSecret, AccessToken, AgentId, AppId, AppSecret的介绍。](https://ding-doc.dingtalk.com/doc#/bgb96b/mzd9qg)

#### 创建企业内部开发应用，申请接口调用权限

[链接](https://ding-doc.dingtalk.com/doc#/serverapi2/eev437)

首先创建一个微应用。使用钉钉企业管理员账号登录[钉钉开发者后台网站](https://oa.dingtalk.com/?redirect=http%3A%2F%2Foa.dingtalk.com%2Fomp%2Fapi%2Fmicro_app%2Fadmin%2Flanding%3Fcorpid%3Dopen-dev.dingtalk.com%26redirect_url%3Dhttp%3A%2F%2Fopen-dev.dingtalk.com%2F#/login)，在应用开发页面，选择企业内部开发 > H5微应用，然后单击创建应用,填写应用名称、应用描述和补充应用图标，然后单击确定创建。创建应用可获得appkey，appsecret，在获取access\_token中需要用到。

还需要在这个应用的信息管理页面，设置服务器出口IP，为输入调用钉钉服务端API时使用的IP即企业服务器的公网IP，多个IP请以","隔开，支持带一个\*号通配符的IP格式。

需要用到的权限就需要在钉钉开发者平台网页上[开启权限](https://ding-doc.dingtalk.com/doc#/serverapi2/rnomdt)。

* 需要获取部门id，然后通过这个部门号去获取当前部门所有的人的详情--需要通讯录只读权限。
* 通过以上获取到的部门id，人员id，创建一个企业群聊--需要企业会话权限。
  然后就可以实现利用httpClient插件中的httpGet和httpPost方法向一个企业群聊中发送消息。

#### 获取access\_token

[链接](https://ding-doc.dingtalk.com/doc#/serverapi2/eev437)

* access\_token是应用调用API的凭证，由 appkey和appsecret换取。

> 请注意，access\_token的时效为7200秒。需要缓存access\_token，用于后续接口的调用（注意：不能频繁调用gettoken接口，否则会受到频率拦截）。当access\_token失效或过期时，需要重新获取，应实现access\_token失效时重新获取的逻辑。

* 不同应用都有相应的appkey和appsecret。
* 请求方式：GET（HTTPS）

  请求地址：https://oapi.dingtalk.com/gettoken?appkey=key&appsecret=secret

这里使用httpClient中的函数httpGet(url,params,timeout,headers)。不需要添加http请求头，只需要填写前3个参数。

* 参数appkey的值(key)为应用的标识号，appsecret的值(secret)为对应应用的凭证密钥。
* url在这里只需要填写'https://oapi.dingtalk.com/gettoken'，后面的appkey和appsecret参数通过httpGet方法中的param参数就可以填写。
* param是一个键值对都是string的字典。 参数appkey的值(key)为对应应用id，appsecret的值(secret)为对应应用的凭证密钥，两个值都需要以字符串的形式加入到param中。
* timeout为超时时间，单位为毫秒，数据类型为整型。达到超时时间后`httpGet`会直接返回，无论是否收到http应答报文。因为这是一个远程网络请求，超时时间最好设置为1000毫秒或以上。

示例：

填写参数url：

```
url = 'https://oapi.dingtalk.com/gettoken';
```

填写参数param：

```
param=dict(string,string);
key='xxxxx';
secret='xxxxx';
param['appkey']=key;
param['appsecret']=secret;
```

调用`httpGet`向钉钉发送申请access\_token的信息：

```
ret=httpClient::httpGet(url,param,1000);
print ret['text'];
```

返回值ret是一个dictionary，ret['text']是响应正文。如果请求成功，返回的json格式的正文ret['text']如下：

```
{
    "errcode" : 0,
    "errmsg" : "ok",
    "access_token" : "xxxxx"
}
```

请注意，errcode是向钉钉开发平台请求信息的错误码，如果请求成功，返回值是0。不同于http协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[钉钉开发错误码表](https://ding-doc.dingtalk.com/doc#/faquestions/rftpfg)。

access\_token的值后续步骤需要用到。这里我们使用：

```
body = parseExpr(ret.text).eval();
ACCESS_TOKEN=body.access_token;
ERRCODE=body.errcode;
```

就可以便捷地把access\_token和errcode解析出来。

#### 发送群聊消息

##### 获取部门列表

[链接](https://ding-doc.dingtalk.com/doc#/serverapi2/dubakq)

* 请求方式：GET（HTTPS）

  请求地址：https://oapi.dingtalk.com/department/list?access\_token=ACCESS\_TOKEN
* 需要有由第二个步骤获得的access\_token。
* 参数以json的格式放在请求正文中。

```
{"fetch_child" : true}
```

* fetch\_child: 是否递归部门的全部子部门

示例：

填写参数url：

```
url = 'https://oapi.dingtalk.com/department/list';
```

填写参数param,ACCESS\_TOKEN需要替换为由第二个步骤获得的access\_token。

```
param=dict(string,string);
ACCESS_TOKEN='xxxxx';
param['access_token']=ACCESS_TOKEN;
```

调用`httpGet`向钉钉发送查询部门信息的请求：

```
ret=httpClient::httpGet(url,param,1000);
print ret['text'];
```

返回值ret是一个dictionary，ret['text']是响应正文。
如果请求成功，返回的json格式的正文text类似：

```
{
    "errcode" : 0,"errmsg" : "ok","department" : [
        {
            "id" : 123,
            "name" : "服务端开发组",
            "parentid" : 2,
            "createDeptGroup" : false,
            "autoAddUser" : false,
            "ext" : "{\"deptNo\" : 2}"
        }
    ]
}
```

请注意，errcode是向钉钉开发平台请求信息的错误码，如果请求成功，返回值是0。不同于http协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[钉钉开发错误码表](https://ding-doc.dingtalk.com/doc#/faquestions/rftpfg)。

字段id的值就是部门id，后面的步骤需要用到。这里我们使用：

```
body = parseExpr(ret.text).eval();
DEPTID=string(body[0].id);
ERRCODE=body.errcode;
```

就可以便捷地把id和errcode解析出来。

##### 获取部门下成员详情

[链接](https://ding-doc.dingtalk.com/doc#/serverapi2/ege851)

请求方式：GET（HTTPS）

```
请求地址：https://oapi.dingtalk.com/user/getDeptMember?access_token=ACCESS_TOKEN&deptId=1
```

* 首先我们需要有由第二个步骤获得的access\_token。
* deptId是部门id，可以通过上一个步骤获得。

这里使用httpClient中的函数httpGet(url,params,timeout,headers)。不需要添加http请求头，只需要填写前3个参数。

* url只需要填写'https://oapi.dingtalk.com/user/getDeptMember'，后面的access\_token和deptId参数通过httpGet方法中的param参数就可以填写。
* param是一个键值对都是string的字典。 参数access\_token的值(ACCESS\_TOKEN)为请求接口凭证，deptId的值为部门id，两个值都需要以字符串的形式加入到param中。
* timeout为超时时间，单位为毫秒，数据类型为整型。达到超时时间后`httpGet`会直接返回，无论是否收到http应答报文。因为这是一个远程网络请求，超时时间最好设置为1000毫秒或以上。

示例：

填写参数url：

```
url = 'https://oapi.dingtalk.com/user/getDeptMember';
```

填写参数param,其中ACCESS\_TOKEN，DEPTID都需要替换为实际的值。

```
param=dict(string,string);
ACCESS_TOKEN='xxxxx';
DEPTID='xxxxx';
param['access_token']=ACCESS_TOKEN;
param['deptId']=DEPTID;
```

调用`httpGet`向钉钉发送查询部门人员信息的请求：

```
ret=httpClient::httpGet(url,param,1000);
print ret['text'];
```

返回值ret是一个dictionary，ret['text']是响应正文。如果请求成功，返回的json格式的正文ret['text']类似:

```
{
    "errcode" : 0,
    "errmsg" : "ok",
    "userIds" : ["1","2"]
}
```

列表userIds后面步骤需要用到。

请注意，errcode是向钉钉开发平台请求信息的错误码，如果请求成功，返回值是0。不同于http协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[钉钉开发错误码表](https://ding-doc.dingtalk.com/doc#/faquestions/rftpfg)。

字段id的值就是部门id，后面的步骤需要用到。这里我们使用：

```
body = parseExpr(ret.text).eval();
Userlds=body.userIds;
ERRCODE=body.errcode;
```

就可以便捷地把userIds和errcode解析出来。

##### 创建企业群聊

[链接](https://ding-doc.dingtalk.com/doc#/serverapi2/fg9dze)

请求方式：POST（HTTPS）

请求地址：https://oapi.dingtalk.com/chat/create?access\_token=ACCESS\_TOKEN

* 对于post请求，调用钉钉接口需要有一个http请求头(Content-Type:application/json)。
* url中的ACCESS\_TOKEN可以通过第二个步骤获取。
* 参数都是以json的格式放在post请求正文中。

```
{"name" : "groupName","owner" : "zhangsan","useridlist" : ["zxxxx","lxxxx"]}
```

* name：群名称。
* owner：群主userId，员工唯一标识ID；必须为该会话useridlist的成员之一。
* useridlist：群成员列表，每次最多支持40人。

这使用httpClient中的函数httpPost(url,params,timeout,headers)。需要添加一个http请求头`Content-Type : application/json`。

请注意，相较于http协议的get方法，post方法的参数都是放在请求正文中的，httpPost方法的param参数是填写在http报文中的正文部分。在这里，需要补充完整url。

示例:

填写参数url：

```
url = 'https://oapi.dingtalk.com/chat/create?';
ACCESS_TOKEN='xxxxx';
url+='access_token='+ACCESS_TOKEN;
```

填写参数param：

```
param='{"name" : "groupName","owner" : "zhangsan","useridlist" : ["zxxxx","lxxxx"]}';
```

填写参数header，冒号必须紧跟Content-Type，否则钉钉服务端不能识别这个http请求头。

```
header='Content-Type: application/json';
```

调用`httpPost`向钉钉发送创建群聊的请求：

```
ret=httpClient::httpPost(url,param,1000,header);
print ret['text'];
```

返回值ret是一个dictionary，ret['text']是响应正文。
如果请求成功，返回的json格式正文类似如下:

```
{   "errcode" : 0,
    "errmsg" : "ok",
    "chatid" : "chatxxxxxxxxxxxxxxxxxxx",
    "conversationTag" : 2
}
```

请注意，errcode是向钉钉开发平台请求信息的错误码，如果请求成功，返回值是0。不同于http协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[钉钉开发错误码表](https://ding-doc.dingtalk.com/doc#/faquestions/rftpfg)。

这里我们使用：

```
body = parseExpr(ret.text).eval();
ERRCODE=body.errcode;
```

就可以便捷地把errcode解析出来。

##### 向企业群聊发送消息

[链接](https://ding-doc.dingtalk.com/doc#/serverapi2/isu6nk)

* 请求方式：POST（HTTPS）

  请求地址：https://oapi.dingtalk.com/chat/send?access\_token=ACCESS\_TOKEN
* 对于post请求，调用钉钉接口需要有一个http请求头(`Content-Type:application/json`)。
* url中的ACCESS\_TOKEN可以通过第二个步骤获取。
* 参数都是以json的格式放在post请求正文中。

```
{"chatid" : "xxxxx","msg" : {"msgtype" : "text","text" : {"content" : "这是一条测试信息"}}}
```

* chatid:群会话的id。通过创建一个群聊会话获得。可以由上一个步骤获得。
* msg:消息内容。

这里使用httpClient中的函数httpPost(url,params,timeout,headers)。需要添加一个http请求头`Content-Type: application/json`。

请注意，相较于http协议的get方法，post方法的参数都是放在请求正文中的，httpPost方法的param参数是填写在http报文中的正文部分。在这里，需要补充完整url。

示例:

填写参数url：

```
url = "https://oapi.dingtalk.com/chat/send?";
ACCESS_TOKEN='xxxxx';
url+='access_token='+ACCESS_TOKEN;
```

填写参数headers：

```
headers=dict(string,string);
headers['Content-Type']='application/json';
```

填写参数param：

```
param='{"chatid" : "xxx","msg" : {"msgtype" : "text","text" : {"content" : "这是一条测试信息"}}}';
```

调用`httpPost`向钉钉发送群聊消息的请求：

```
ret=httpClient::httpPost(url,param,1000,headers);
print ret['text'];
```

* 如果请求成功，返回的json格式正文类似如下，errcode的值为0。

```
{"errcode" : 0,"errmsg" : "ok","messageId" : "abcd"}
```

> 请注意，errcode是向钉钉开发平台请求信息的错误码，如果请求成功，返回值是0。不同于http协议的请求返回的响应码。如果出现其他errcode值，查看错误信息errmsg。errcode的值的含义可查看[钉钉开发错误码表](https://ding-doc.dingtalk.com/doc#/faquestions/rftpfg)。

通过以下脚本就能把errcode从json格式正文中取出来。

```
body = parseExpr(ret.text).eval();
ERRCODE=body.errcode;
```

### 邮件发送示例

函数sendEmail支持单发邮件和群发邮件。

#### 前提

* 使用本插件的邮件发送函数通常需要在邮件服务商上面设置开启smtp协议。如果还需要获取邮箱授权码，参数psw为邮箱授权码的字符串，否则psw就是邮箱账号的密码。
* 在httpClient插件里面，默认设置了126, 163, yeah.net, sohu, dolphindb, qq邮箱的域名地址和端口。如果使用别的邮箱用户来发送邮件，需要通过emailSmtpConfig自行配置服务器地址和端口:

通过`httpClient::emailSmtpConfig(emailName,host,port)`配置邮箱服务器地址和端口。其中，emailName是邮箱名称，格式为邮箱'@'字符后的字符串；host是邮箱stmp服务器的地址；port是邮箱服务器端口。在httpClient插件里面，默认设置了126, 163, yeah.net, sohu, dolphindb, qq邮箱的域名地址和端口。如果使用别的邮箱用户来发送邮件，需要自行配置服务器地址和端口。配置方式如下：

```
emailName="yahoo.com";
host="smtp.yahoo.com";
port=25;
httpClient::emailSmtpConfig(emailName,host,port);
```

#### 发送邮件

通过`httpClient::sendEmail(user,psw,emailTo,subject,text)`发送邮件。其中，user需要填入实际的发送邮箱账号，psw填入实际的邮箱密码(邮箱授权码)。

示例：

* 单发邮件，recipient填入收件人邮箱。

```
user='MailFrom@xxx.com';
psw='xxxxx';
```

如果是单发邮件，recipient填写为一个目标邮箱的字符串。

```
recipient='Maildestination@xxx.com';
```

执行sendEmail函数，需要填写subject和text参数。

```
res=httpClient::sendEmail(user,psw,recipient,'This is a subject','It is a text');
assert  res[`responseCode]==250;
```

返回值是一个字典res，如果发送成功，res['responseCode']==250。

* 群发邮件，recipientCollection填入收件人邮箱列表。

```
user='MailFrom@xxx.com';
psw='xxxxx';
```

如果是群发邮件，recipient填写为目标邮箱的字符串集合。

```
recipientCollection='Maildestination@xxx.com''Maildestination2@xxx.com''Maildestination3@xxx.com';
```

执行sendEmail函数，需要填写subject和text参数。

```
res=httpClient::sendEmail(user,psw,recipientCollection,'This is a subject','It is a text');
assert  res[`responseCode]==250;
```

返回值是一个字典res，如果发送成功，res['responseCode']==250。

