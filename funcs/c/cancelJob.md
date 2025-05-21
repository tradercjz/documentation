# cancelJob

## 语法

`cancelJob(jobId)`

## 参数

**jobId** 是批处理作业的 ID，是一个字符串标量或向量。若为向量，表示同时取消多个批处理作业。

## 详情

取消已经提交但尚未完成的批处理作业。2.00.7 版本后，若执行 cancelJob 时，发现某个 jobId
不存在，系统不再抛出异常，而是将包含 jobId 的报错信息输出到日志。

从 2.00.11
版本开始，系统对该操作进行了权限管理的增强。管理员（包括普通管理员和超级管理员）具有取消任何用户创建的批处理作业的权限，而普通用户只能取消自己创建的批处理作业。

## 例子

```
def writeData(num){
   n=10
   month=take(2000.01M..2016.12M, n)
   x=rand(1.0, n)
   tt=table(month, x)
   if(existsDatabase("dfs://test_db")){
       dropDatabase("dfs://test_db")
   }
   db=database("dfs://test_db", VALUE, 2000.01M..2016.12M)
   pt = db.createPartitionedTable(tt, `pt, `month)
   for(x in 1..num){
       pt.append!(tt)
       sleep(1000)
   }
}

myJobId="writeData"+temporalFormat(datetime(now()),"yyyyMMddHHmmss")
submitJob(myJobId,"write data to dfs table",writeData,120);
cancelJob(myJobId);
```

取消集群中所有未完成的 job。

```
def cancelAllBatchJob(){
   jobids=exec jobid from getRecentJobs() where endTime=NULL
   cancelJob(jobids)
}
pnodeRun(cancelAllBatchJob)
```

