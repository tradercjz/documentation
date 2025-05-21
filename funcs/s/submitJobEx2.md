# submitJobEx2

## 语法

`submitJobEx2(jobId, jobDesc, priority, parallelism, onComplete, jobDef,
args...)`

## 详情

提交批处理作业到本地节点并返回作业的 ID，待作业完成后，执行回调函数。

注： `submitJobEx2` 与 [submitJobEx](submitJobEx.html) 的区别在于：执行完成后，`submitJobEx2`
会执行回调函数。

## 参数

**jobId** 是作业的 ID，字符串类型。

**jobDesc** 是字符串，用于描述作业。

**priority** 是 0 到 9 之间的整数，表示作业的优先级。9 表示优先级最高。

**parallelism** 是正整数，表示分配给该作业的线程数上限。

**onComplete** 是回调函数，当批处理作业执行完毕（包括有异常的情况）后，会执行该函数。该函数接受 4 个参数：

* jobId：作业的ID
* jobDesc：作业的描述。
* success：布尔值，表示作业是否执行成功。
* result：作业的结果。

**jobDef** 是用于定义作业的本地函数。

注： 该参数是一个函数对象，而非表示函数名的字符串，因此不可使用引号。

**args…** 是函数的参数。如果函数没有参数，它可以不指定。

## 例子

```
def jobDemo(n){
    s = 0
    for (x in 1 : n) {
        s += sum(sin rand(1.0, 100000000)-0.5)
        print("iteration " + x + " " + s)
    }
    return s
}

def cbFunc(jobId, jobDesc, success, result){
    desc = jobId + " " + jobDesc
    if(success){
        desc += " successful " + result
    }
    else{
        desc += " with error: " + result
    }
    writeLog(desc)
}

submitJobEx2("jobDemo1","job demo", 8, 12, cbFunc, jobDemo, 100)
```

