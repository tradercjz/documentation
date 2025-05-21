import pandas as pd
import numpy as np
from scipy.interpolate import KroghInterpolator
from datetime import datetime, timedelta
import time

file_path = '<YourDir>/curveOneday.csv'
curveOneday = pd.read_csv(file_path)
# 基础数据，性能测试
grouped = curveOneday.groupby(['TRADE_DT', 'B_ANAL_CURVENUMBER'])
# 循环处理每个组
results = []
start_time = time.time()
for name, group in grouped:
    try:
        if group['B_ANAL_CURVETERM'].nunique() < 2:
            results.append((name, np.nan))  # 如果不足两个不同点，返回NaN
            continue
        interpolator = KroghInterpolator(group['B_ANAL_CURVETERM'].values, group['B_ANAL_YIELD'].values)
        interpolated_value = interpolator(1.3)
        results.append((name, interpolated_value))
    except Exception as e:
        print(f"插值失败，组 {name}，错误信息：{e}")
        results.append((name, np.nan))  # 捕捉到任何异常，简单处理为返回 NaN
# 插值完成时间
interpolation_time = time.time()
# 将结果转换为 DataFrame
result_df = pd.DataFrame(results, columns=['Group', 'InterpolatedValue'])
# 输出结果和计时
interpolation_duration = interpolation_time - start_time
print(interpolation_duration)

# 扩展成1个月数据的性能测试
# 生成日期
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 1, 31)
date_range = pd.date_range(start=start_date, end=end_date)

# 扩展数据到一个月
full_month_data = pd.concat([curveOneday]*len(date_range), ignore_index=True)
full_month_data['TRADE_DT'] = np.repeat(date_range, len(curveOneday))

full_month_data

grouped = full_month_data.groupby(['TRADE_DT', 'B_ANAL_CURVENUMBER'])
# 循环处理每个组
results = []
start_time = time.time()

for name, group in grouped:
    try:
        if group['B_ANAL_CURVETERM'].nunique() < 2:
            results.append((name, np.nan))  # 如果不足两个不同点，返回NaN
            continue
        interpolator = KroghInterpolator(group['B_ANAL_CURVETERM'].values, group['B_ANAL_YIELD'].values)
        interpolated_value = interpolator(1.3)
        results.append((name, interpolated_value))
    except Exception as e:
        print(f"插值失败，组 {name}，错误信息：{e}")
        results.append((name, np.nan))  # 捕捉到任何异常，简单处理为返回 NaN

# 插值完成时间
interpolation_time = time.time()
# 将结果转换为 DataFrame
result_df = pd.DataFrame(results, columns=['Group', 'InterpolatedValue'])
# 输出结果和计时
interpolation_duration = interpolation_time - start_time
print(interpolation_duration)



# 扩展成1年数据的性能测试
# 生成日期
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date)

# 扩展数据到一整年
full_year_data = pd.concat([curveOneday]*len(date_range), ignore_index=True)
full_year_data['TRADE_DT'] = np.repeat(date_range, len(curveOneday))
grouped = full_year_data.groupby(['TRADE_DT', 'B_ANAL_CURVENUMBER'])
# 循环处理每个组
results = []
start_time = time.time()

for name, group in grouped:
    try:
        if group['B_ANAL_CURVETERM'].nunique() < 2:
            results.append((name, np.nan))  # 如果不足两个不同点，返回NaN
            continue
        interpolator = KroghInterpolator(group['B_ANAL_CURVETERM'].values, group['B_ANAL_YIELD'].values)
        interpolated_value = interpolator(1.3)
        results.append((name, interpolated_value))
    except Exception as e:
        print(f"插值失败，组 {name}，错误信息：{e}")
        results.append((name, np.nan))  # 捕捉到任何异常，简单处理为返回 NaN
# 插值完成时间
interpolation_time = time.time()
# 将结果转换为 DataFrame
result_df = pd.DataFrame(results, columns=['Group', 'InterpolatedValue'])
# 输出结果和计时
interpolation_duration = interpolation_time - start_time
print(interpolation_duration)
