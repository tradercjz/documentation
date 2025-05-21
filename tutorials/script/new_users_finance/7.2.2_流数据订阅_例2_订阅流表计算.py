import dolphindb as ddb
import numpy as np
import pandas as pd
import dolphindb.settings as keys
import csv
from threading import Event

# 建立 API 和 server 之间的连接
s = ddb.session()
conn = s.connect(host="ecosystem", port=8440, userid="admin", password="123456")
# 替换自己的 ip/port

if conn:
    print("successfully connected!")

s.enableStreaming(0)

def my_handler(msg):
    optPath = "D:/File2024/入门教程/streamOutput.csv"
    msg.to_csv(optPath, mode="a", header=False, index=False)

s.subscribe(host="ecosystem", port=8440, tableName="snap2", actionName="sub_snap2", offset=-1, handler=my_handler, msgAsTable=True, batchSize=10000, throttle=1, filter=np.array(["000001"]))

Event().wait()