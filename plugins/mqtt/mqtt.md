# mqtt

MQTT 插件基于 MQTT-C 库开发，用于与 MQTT 服务器建立连接并进行交互。该插件支持订阅消息，将收到的消息解析为 CSV 或 JSON 格式；亦支持发布消息，将待发送的消息按照 CSV 或 JSON 格式打包后发布 。

该插件利用 MQTT-C 库的高性能和稳定性，实现了高效的连接管理、消息发布与订阅、断线重连、安全通信等功能，使开发者能够专注于应用逻辑而无需担心底层通信细节。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10及更高版本。支持 Linux x64 ，Windows x64

### 安装步骤

1. 在DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("mqtt")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("mqtt")
   ```

## 接口说明

### connect

**语法**

```
mqtt::connect(host, port,[qos=0],[formatter],[batchSize=0],[username],[password],[sendBufSize=40960],[config])
```

**详情**

建立一个与 MQTT server/broker 的连接。返回一个 connection。可以显式的调用 `close` 函数去关闭，也可以在 reference count 为0时自动释放。

**参数**

**host** 是一个字符串，表示 MQTT server/broker 的 IP 地址。

**port** 是一个整数，表示 MQTT server/broker 的端口号。

**qos** 一个整数，表示消息发布服务质量。0：至多一次；1：至少一次；2：只有一次。它是可选参数，默认是0。

**formatter** 是一个函数，用于对发布的数据按 CSV 或 JSON 格式进行打包。目前仅支持由 `createJsonFormatter` 或 `createCsvFormatter` 创建的函数。

**batchSize** 是一个整数，表示每次发送的记录行数。当待发布内容是一个表时，可以分批发送。

**username** 是一个字符串，用于登录 MQTT server/broker 的用户名。

**password** 是一个字符串，用于登录 MQTT server/broker 的密码。

**sendBufSize** 是一个整数，用于指定发送缓冲区大小，单位为字节，默认是 40960。

**config** 是一个字典，用于指定一些额外的配置项。其键为 STRING 类型标量，值为 ANY。目前支持的键为：

* "recvBufSize" 一个正整数，用于指定接收缓冲区大小，单位为字节，默认是 40960。
* "clientID" 一个字符串标量，用于指定发布连接的 ID。若不指定则自动生成。

**例子**

```
f=mqtt::createJsonFormatter()
conn=connect("test.mosquitto.org",1883,0,f,50)
```

### publish

**语法**

```
mqtt::publish(conn,topic,obj)
```

**详情**

向 MQTT server/broker 发布消息。

**参数**

**conn** `connect` 函数返回的值。

**topic** STRING 类型标量，表示主题。

**obj** STRING 类型标量或向量/内存表，表示待发布的消息内容。

**例子**

```
mqtt::publish(conn,"dolphindb/topic1","welcome")
mqtt::publish(conn,"devStr/sensor001",["hello world","welcome"])
t=table(take(0..99,50) as hardwareId ,take(now(),
		50) as ts,rand(20..41,50) as temperature,
		rand(50,50) as humidity,rand(500..1000,
		50) as voltage)
mqtt::publish(conn,"dolphindb/device",t)
```

### createPublisher

**语法**

```
mqtt::createPublisher(conn,topic,colNames,colTypes)
```

**详情**

创建一个对象，可以通过向该对象写入数据来发布消息。

**参数**

**conn** 是 `connect` 函数返回的值。

**topic** STRING 类型标量，表示主题。

**colNames** STRING 类型向量，表示发布的表结构的列名。

**colTypes** 一个向量，表示发布的表结构的列类型。

**例子**

```
MyFormat = take("", 3)
MyFormat[2] = "0.000"
f = createCsvFormatter(MyFormat, ',', ';')
pubConn = connect("127.0.0.1",1883,0,f,100)

colNames = [`ts, `hardwareId, `val]
colTypes = [TIMESTAMP, SYMBOL, INT]
publisher = createPublisher(pubConn, "sensor/s001", colNames, colTypes)

// 使用举例1：直接将要 push 的数据 append 到 publisher 中即可发布，这里的 tb 参数必须是一个表
append!(publisher, tb)

// 使用举例2：通过 insert SQL 语句
insert into publisher values([2023.08.25 10:57:47.961, 2023.08.25 10:57:47.961], symbol([`bb,`cc]), [22,33])

// 使用举例3：订阅流数据表时直接设置 handler=append!{publisher} 即可完成实时数据发布
share streamTable(1000:0, `time`sym`val, [TIMESTAMP, SYMBOL, INT]) as trades
subscribeTable(tableName="trades", actionName="engine1", offset=0, handler=append!{publisher}, msgAsTable=true);

insert into trades values(2018.10.08T01:01:01.785,`dd,44)
insert into trades values(2018.10.08T01:01:02.125,`ee,55)
insert into trades values(2018.10.08T01:01:10.263,`ff,66)
```

### close

**语法**

```
mqtt::close(conn)
```

**详情**

断开与 MQTT server/broker 的连接。

**参数**

**conn** 是 `connect` 函数返回的值。

**例子**

```
mqtt::close(conn)
```

### subscribe

**语法**

```
mqtt::subscribe(host, port, topic, parser, handler, [username], [password], [recvbufSize=20480],[config])
```

**详情**

向 MQTT server/broker 订阅消息。返回一个连接。

**参数**

**host** 是一个字符串，表示 MQTT server/broker 的 IP 地址。

**port** 是一个整数，表示 MQTT server/broker 的端口号。

**topic** 是一个字符串，表示订阅主题。

**parser** 是一个函数，用于对订阅的消息按 CSV 或 JSON 格式进行解析。目前仅支持由 createJsonParser 或 createCsvParser 创建的函数。

**handler** 是一个函数或表，用于处理从 MQTT server/broker 接收的消息。

**username** 是一个字符串，用于登录 MQTT server/broker 的用户名。

**password** 是一个字符串，用于登录 MQTT server/broker 的密码。

**recvbufSize** 是一个整数，用于指定接收缓冲区大小，单位为字节，默认是 20480。

**config** 是一个字典，用于指定一些额外的配置项。其键为 STRING 类型标量，值为 ANY。目前支持的键为：

* "sendBufSize" 一个正整数，用于指定发送缓冲区大小，单位为字节，默认是 40960。
* "subscribeID" 一个字符串标量，用于指定订阅连接的 ID，若不指定则自动生成。
* "asyncFlag" 一个布尔类型，用于指定是否开启异步订阅模式，默认为 false。

**例子**

```
p = createCsvParser([INT, TIMESTAMP, DOUBLE, DOUBLE,DOUBLE], ',', ';' )
sensorInfoTable = table( 10000:0,`deviceID`send_time`temperature`humidity`voltage ,[INT, TIMESTAMP, DOUBLE, DOUBLE,DOUBLE])
conn = mqtt::subscribe("192.168.1.201",1883,"sensor/#",p,sensorInfoTable)
```

### getSubscriberStat

**语法**

```
mqtt::getSubscriberStat()
```

**详情**

查询所有订阅信息。返回一个包含7列的表，分别是："subscriptionId" 表示订阅标识符；"user" 表示建立订阅的会话用户; "host" 表示 MQTT server/broker 的 IP； "port" 表示 MQTT server/broker 的端口号；"topic" 表示订阅主题；"createTimestamp" 表示可以订阅建立时间；"receivedPackets" 表示订阅收到的消息报文数。

**参数**

无。

**例子**

```
mqtt::getSubscriberStat()
```

### unsubscribe

**语法**

```
mqtt::unsubscribe(subscription)
```

**详情**

取消订阅MQTT server/broker。

**参数**

**subscription** 是 `subscribe` 函数返回的值或 `getSubscriberStat` 返回的订阅标识符。

**例子**

```
mqtt::unsubscribe(sub1)
mqtt::unsubscribe("350555232l")
```

### createCsvFormatter

**语法**

```
mqtt::createCsvFormatter([format], [delimiter], [rowDelimiter])
```

**详情**

创建一个 CSV 格式的 Formatter 函数。

**参数**

**format** STRING 类型向量。

**delimiter** STRING 类型标量，表示列之间的分隔符，默认是 ','。

**rowDelimiter** STRING 类型标量，表示行之间的分隔符，默认是 ';'。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
MyFormat = take("", 18)
MyFormat[2] = "0.000"
MyFormat[5] = "yyyy.MM.dd"
f = mqtt::createCsvFormatter(MyFormat)
f(t)
```

### createCsvParser

**语法**

```
mqtt::createCsvParser(colTypes, [delimiter], [rowDelimiter])
```

**详情**

创建一个 CSV 格式的 Parser 函数。

**参数**

**colTypes** 一个向量，表示列的数据类型。

**delimiter** STRING 类型标量，表示列之间的分隔符，默认是','。

**rowDelimiter** STRING 类型标量，表示行之间的分隔符，默认是';'。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
MyFormat = take("", 18)
MyFormat[2] = "0.000"
MyFormat[5] = "yyyy.MM.dd"
f = mqtt::createCsvFormatter(MyFormat)
s=f(t)
p = mqtt::createCsvParser([BOOL,CHAR,SHORT,INT,LONG,DATE,MONTH,TIME,MINUTE,SECOND,DATETIME,TIMESTAMP,NANOTIME,NANOTIMESTAMP,FLOAT,DOUBLE,STRING,SYMBOL])
p(s)
```

### createJsonFormatter

**语法**

```
mqtt::createJsonFormatter()
```

**详情**

创建一个 JSON 格式的 Formatter 函数。

**参数**

无。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
f = mqtt::createJsonFormatter()
f(t)
```

### createJsonParser

**语法**

```
mqtt::createJsonParser(colTypes, colNames)
```

**详情**

创建一个 JSON 格式的 Parser 函数。

**参数**

**colTypes** 一个向量，表示列的数据类型。

**colNames** STRING 类型标量，表示列名。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
f = mqtt::createJsonFormatter()
p = createJsonParser([BOOL,CHAR,SHORT,INT,LONG,DATE,MONTH,TIME,MINUTE,SECOND,DATETIME,TIMESTAMP,NANOTIME,NANOTIMESTAMP,FLOAT,DOUBLE,STRING,SYMBOL],
`bool`char`short`int`long`date`month`time`minute`second`datetime`timestamp`nanotime`nanotimestamp`float`double`string`symbol)
s=f(t)
x=p(s)

```

## 完整示例

```
loadPlugin("mqtt")
use mqtt;

//***************************publish a table****************************************//
MyFormat = take("", 5)
MyFormat[2] = "0.000"
f = createCsvFormatter(MyFormat, ',', ';')

//create a record for every device
def writeData(hardwareVector){
	hardwareNumber = size(hardwareVector)
	return table(take(hardwareVector,hardwareNumber) as hardwareId ,take(now(),
		hardwareNumber) as ts,rand(20..41,hardwareNumber) as temperature,
		rand(50,hardwareNumber) as humidity,rand(500..1000,
		hardwareNumber) as voltage)
}
def publishTableData(server,topic,iterations,hardwareVector,interval,f){
    conn=connect(server,1883,0,f,100)
    for(i in 0:iterations){
	   t=writeData(hardwareVector)
	   publish(conn,topic,t)
	   sleep(interval)
    }
    close(conn)

}
host="192.168.1.201"
submitJob("submit_pub1", "submit_p1", publishTableData{host,"sensor/s001",10,100..149,100,f})
publishTableData(host,"sensor/s001",100,0..99,100,f)

//*******************************subscribe : handler is a table************************************************//
p = createCsvParser([INT, TIMESTAMP, DOUBLE, DOUBLE,DOUBLE], ',', ';' )
sensorInfoTable = table( 10000:0,`deviceID`send_time`temperature`humidity`voltage ,[INT, TIMESTAMP, DOUBLE, DOUBLE,DOUBLE])
conn = mqtt::subscribe("192.168.1.201",1883,"sensor/#",p,sensorInfoTable)
```

