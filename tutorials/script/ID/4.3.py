import pandas as pd
import dolphindb as ddb
import query

# 建立会话并登陆账号
s = ddb.session("192.198.1.38", 8200, 'testUser2', '123456')

# 访问全表数据
df = query.query(session=s, startDate='2015.01.01', endDate='2024.12.31')

# 访问2024年2月指定证券、指定列的数据
df = query.query(session=s, startDate='2024.02.01', endDate='2024.02.29', security='`000001', cols='`SecurityID`date`time`col1`col2`col3`col4`col5`col6`col7`col8`col9`col10')

# 访问近1年所有数据
df = query.queryRecentYear(session=s)

# 访问指定日期开始、指定列的数据
df = query.queryRecentYear(session=s, startDate='2024.07.01', cols='`SecurityID`date`time`col2`col3')

# 访问2023年指定证券、允许访问的所有列的数据
df = query.queryFirst10Col(session=s, startDate='2023.01.01', endDate='2023.12.31', security='`000008`000009`000010')

# 访问2022年12月指定列的数据
df = query.queryFirst10Col(session=s, startDate='2022.12.01', endDate='2022.12.31', cols='`SecurityID`date`time`col4`col5`col6')

# 访问2021年1月允许访问的所有列的数据
df = query.queryCond(session=s, startDate='2021.01.01', endDate='2021.01.31')

# 访问2021年指定列的数据
df = query.queryCond(session=s, startDate='2021.01.01', endDate='2021.12.31', cols='`SecurityID`date`time`col47`col48`col49')