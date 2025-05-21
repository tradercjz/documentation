# 使用 at 方法修改单个元素的值
df.at[0, 'value']=10
df.iat[1, 0] = 20
t1
// output:
value
10
20
3
```

（3）删除数据

* 调用 drop 方法删除数据

```
df_nonlazy.drop(['name'], axis=1)
```

