# submitJobEx

## 语法

`submitJobEx(jobId, jobDesc, priority, parallelism, jobDef,
args...)`

## 参数

**jobId** 是作业的 ID，是字符串类型。

**jobDesc** 是字符串，用于描述作业。

**priority** 是0到9之间的整数，表示作业的优先级。9表示优先级最高。

**parallelism** 是正整数，表示分配给该作业的线程数上限。

**jobDef** 是用于定义作业的本地函数。请注意，该参数是一个函数对象，而不是表示函数名的字符串，因此不可使用引号。

**args...** 是函数的参数。如果函数没有参数，它可以不指定。

## 详情

把批处理作业提交到本地节点并且返回作业的ID。`submitJobEx` 与 [submitJob](submitJob.md) 的唯一区别在于 `submitJobEx`
中可以指定参数 *priority* 与 *parallelism*。

## 例子

```
def jobDemo(n){
    s = 0
    for (x in 1 : n) {
        s += sum(sin rand(1.0, 100000000)-0.5)
        print("iteration " + x + " " + s)
    }
    return s
};

submitJobEx("jobDemo1","job demo", 8, 12, jobDemo, 100);
```

