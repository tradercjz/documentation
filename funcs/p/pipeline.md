# pipeline

## 语法

`pipeline(initTasks, followers,
[queueDepth=2])`

## 参数

**initTasks** 是所有任务初始步骤的集合，其中每个任务都是由无参数的函数表示。例如，我们有10个任务，那么 *initTasks*
是一个包含10个无参数函数的元组。

**followers** 是一元函数的集合，每个函数代表初始步骤之后的一个步骤。如果一个任务有 N
个步骤，*followers* 具有N-1个一元函数。*followers* 的输出是下一个 *followers*
的输入。最后一个 *followers* 有可能返回一个对象。任务的初始步骤是在主线程（接受任务的线程）中执行的，剩下的步骤在单独的线程中执行。如果
`pipeline` 函数用于执行 N 个步骤的任务，系统会创建 N-1 个线程并且这些线程会在工作完成后销毁。

**queueDepth**
是队列的最大长度。每个步骤的中间结果保存在队列中，用于下一个步骤。若队列满了，执行会中止，直到下一个步骤使用了队列中的数据。队列的长度越长，下一个步骤的等待时间越短。但是，长的队列会占用更多内存。*queueDepth*
的默认值是2。

## 详情

通过多线程优化符合如下条件的任务：

(1) 可分解为多个子任务。

(2) 每个子任务包含多个步骤。

(3) 第i个子任务的第 k 个步骤必须在第i个子任务的第 k-1 个步骤以及第 i-1 个子任务的第 k 个步骤完成后才能执行。

如果最后一个步骤返回一个对象，`pipeline` 函数返回一个元组，否则不返回任何内容。

## 例子

下例中，需要把分区表 stockData 转换成一个 csv
文件。该表包含了2008年到2018年的数据，超过了系统的可用内存，因此不能把整个表加载到内存后，再转换成 csv
文件。可把任务分为多个子任务，每个子任务包含两个步骤：加载一个月的数据到内存，然后将这些数据存储到 csv 文件中。每个月的数据存储到 csv
文件中时，必须保证该月数据已加载到内存，并且上个月的数据已经存储到 csv 文件中。

```
v = 2000.01M..2018.12M
def loadData(m){
return select * from loadTable("dfs://stockDB", "stockData") where TradingTime between datetime(date(m)) : datetime(date(m+1))
}

def saveData(tb){
tb.saveText("/hdd/hdd0/data/stockData.csv",',', true)
}

pipeline(each(partial{loadData}, v),saveData);
```

