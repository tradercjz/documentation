# cachedTable

## 语法

`cachedTable(updateFunc, retentionSeconds)`

## 参数

**updateFunc** 是一个函数。它必须是无参数的，并且返回对象是一个表。

**retentionSeconds** 是一个正整数，表示数据更新的时间间隔，单位是秒。

## 详情

创建一种特殊类型的内存表：缓存表。如果查询缓存表的时间与上次数据更新时间相距等于或超过
*retentionSeconds* 秒，会自动执行 *updateFunc* 以更新缓存表。

如果需要多线程访问缓存表，需要将缓存表共享。

## 例子

下例定义一个一元函数 f1，在传入 cachedTable 时，需要通过部分应用的方式将 f1 转为无参数函数，即为 cachedTable 的
*updateFunc* 参数传入 f1{t}。

```
def f1(mutable t){
    update t set id=id+1
    return t
}
t=table(1..5 as id, 15 25 35 45 55 as val)
ct=cachedTable(f1{t}, 2);

select * from ct;
```

| id | val |
| --- | --- |
| 2 | 15 |
| 3 | 25 |
| 4 | 35 |
| 5 | 45 |
| 6 | 55 |

```
sleep(2100)
select * from ct
```

| id | val |
| --- | --- |
| 3 | 15 |
| 4 | 25 |
| 5 | 35 |
| 6 | 45 |
| 7 | 55 |

```
ct=NULL;
```

