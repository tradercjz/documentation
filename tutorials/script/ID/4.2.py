import pandas as pd
import dolphindb as ddb

# 建立会话并登陆账号
s = ddb.session("192.198.1.38", 8200, 'testUser2', '123456')

# 访问全表数据
sqlStr = """
    query(startDate=2015.01.01, endDate=2024.12.31, cols="*", security=NULL)
"""
df = s.run(sqlStr)

# 访问近1年所有数据
sqlStr = """
    queryRecentYear(startDate=2024.07.01)
"""
df = s.run(sqlStr)

# 访问2023年指定证券、允许访问的所有列的数据
sqlStr = """
    queryFirst10Col(startDate=2023.01.01, endDate=2023.12.31, security=`000008`000009`000010)
"""
df = s.run(sqlStr)

# 访问2021年指定列的数据
sqlStr = """
    queryCond(startDate=2021.01.01, endDate=2021.12.31, cols=`SecurityID`date`time`col47`col48`col49)
"""
df = s.run(sqlStr)