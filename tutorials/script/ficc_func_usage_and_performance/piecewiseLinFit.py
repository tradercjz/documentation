import numpy as np
import pandas as pd
import pwlf
import time
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# Read the data
file_path =  '<YourDir>/curveOneday.csv'
data = pd.read_csv(file_path)

# Rename columns for convenience
data.rename(columns={'B_ANAL_CURVETERM': 'Maturity', 'B_ANAL_YIELD': 'Yield'}, inplace=True)

## 单个资产分段线性函数耗时测试
dataSingle = data[data['B_ANAL_CURVENUMBER'] == 4242]

## 定义一个函数来进行分段线性回归
def run_pwlf(dataTest):
    x = dataTest['Maturity']
    y = dataTest['Yield']
    get_model = pwlf.PiecewiseLinFit(x,y)
#     print(f"使用的fitnum为: {fitNum}")
    res = get_model.fit(fitNum)      #不同分段通过改变.fit()参数实现
    return res

# 分段数
fitNum = 5
start_time = time.time()
model = pwlf.PiecewiseLinFit(dataSingle['Maturity'] ,dataSingle['Yield'])
res = model.fit(fitNum)
end_time = time.time()
print("单个耗时: {:.3f} 秒".format(end_time - start_time))

## 使用groupby和apply进行分组分段线性回归耗时测试
start_time = time.time()
results_df = data.groupby('B_ANAL_CURVENUMBER').apply(run_pwlf).reset_index()
end_time = time.time()
print("所有标的耗时: {:.3f} 秒".format(end_time - start_time))