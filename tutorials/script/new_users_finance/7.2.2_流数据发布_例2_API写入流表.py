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
try{dropStreamTable("st2")}catch(ex){writeLog(ex)}
dbName = "dfs://stock_lv2_snapshot"
tbName = "snapshot"

colName=loadTable(dbName, tbName).schema().colDefs.name
colType=loadTable(dbName, tbName).schema().colDefs.typeString
t = streamTable(100:0, colName, colType);
enableTableShareAndPersistence(table=t, tableName="st2", cacheSize=100000)
"""
s.run(spt)

data_path = "D:\\File2024\\入门教程\\data\\2022.01.04.csv"
df = pd.read_csv(data_path)
print(df.head(1))

# 字段类型转换
df["Securityid"] = df["Securityid"].astype('str').apply(lambda x: x.zfill(6))
df["TradeDate"] = pd.to_datetime(df["TradeDate"], format='%Y.%m.%d')
df["TradeTime"] = pd.to_datetime(df["TradeTime"] , format='%H:%M:%S.%f')
df["LocalTime"] = pd.to_datetime(df["LocalTime"] , format='%H:%M:%S.%f')
df["OfferPrice"] = df["OfferPrice"].apply(lambda str: [float(x) if x.strip() else np.NaN for x in str.split(',')])
df["BidPrice"] = df["BidPrice"].apply(lambda str: [float(x) if x.strip() else np.NaN for x in str.split(',')])
df["OfferOrderQty"] = df["OfferOrderQty"].apply(lambda str: [int(x) if x.strip() else None for x in str.split(',')])
df["BidOrderQty"] = df["BidOrderQty"].apply(lambda str: [int(x) if x.strip() else None for x in str.split(',')])
df["BidNumOrders"] = df["BidNumOrders"].apply(lambda str: [int(x) if x.strip() else None for x in str.split(',')])
df["OfferNumOrders"] = df["OfferNumOrders"].apply(lambda str: [int(x) if x.strip() else None for x in str.split(',')])
df["OfferOrder"] = df["OfferOrder"].apply(lambda str: [int(x) if x.strip() else None for x in str.split(',')])
df["BidOrder"] = df["BidOrder"].apply(lambda str: [int(x) if x.strip() else None for x in str.split(',')])

# print(df["TradeTime"].head(1))

writer = ddb.MultithreadedTableWriter(host="ecosystem", port=8440, userId="admin", password="123456", dbPath="", tableName="st2", threadCount=1)

# 通过循环模拟流数据写入
for row in df.itertuples(index=False):
    data = tuple(row)
    tmp = writer.insert(*data)
    if(tmp.hasError()):
        print(tmp.errorCode + ": " + tmp.errorInfo)

writer.waitForThreadCompletion()
res = writer.getStatus()
print(res)

if res.succeed():
    print("Data successfully written.")

