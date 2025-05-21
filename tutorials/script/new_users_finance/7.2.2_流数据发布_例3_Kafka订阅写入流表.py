from kafka import KafkaConsumer, TopicPartition
import json
from json import JSONDecodeError
import dolphindb as ddb
import numpy as np
import pandas as pd
import dolphindb.settings as keys

# 建立 API 和 server 之间的连接
s = ddb.session()
conn = s.connect(host="ecosystem", port=8440, userid="admin", password="123456")
# 替换自己的 ip/port

if conn:
    print("successfully connected!")

# 定义用于写入的持久化流表
spt = """
try{dropStreamTable("st3")}catch(ex){writeLog(ex)}

dbName = "dfs://stock_lv2_snapshot"
tbName = "snapshot"

colName=loadTable(dbName, tbName).schema().colDefs.name
colType=loadTable(dbName, tbName).schema().colDefs.typeString
t = streamTable(100:0, colName, colType);
enableTableShareAndPersistence(table=t, tableName="st3", cacheSize=100000)
"""
s.run(spt)

##### 上述脚本可在 DolphinDB 端实现 #####


# 定义Kafka集群的地址和topic名称
bootstrap_servers = ['183.134.101.143:9092']
topic = 'snapshot'

# 创建一个KafkaConsumer对象，并指定要消费的topicY
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         value_deserializer=lambda m: json.loads(m) if m else None
                        )

# 创建 MTW 对象用于实时写入流数据
writer = ddb.MultithreadedTableWriter(host="ecosystem", port=8440, userId="admin", password="123456", dbPath="", tableName="st3", threadCount=1, batchSize=100)

# 消费 kafka 中的数据写入流表
for message in consumer:
    try:
        msg = message.value
        msg['TradeDate']=pd.to_datetime(msg["TradeDate"], format='%Y.%m.%d')
        msg["TradeTime"] = pd.to_datetime(msg["TradeTime"] , format='%H:%M:%S.%f')
        msg["LocalTime"] = pd.to_datetime(msg["LocalTime"] , format='%H:%M:%S.%f')
        data = tuple(msg.values())
        tmp = writer.insert(*data)
        if(tmp.hasError()):
            print(tmp.errorCode + ": " + tmp.errorInfo)
    except Exception:
        print("Received invalid JSON message:", message)


