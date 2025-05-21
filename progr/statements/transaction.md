# transaction

## 语法

```
transaction{

<statement block>;

}
```

## 详情

transaction 将对单个内存表（包含 mvccTable
或共享内存表）操作的多个 SQL 语句封装为一个事务，以保证语句块的原子性、一致性和隔离性，即若 transaction
执行过程中某条语句报错，则回滚所有语句。

**注意**：目前 transaction 仅支持除 create, alter，insert into 以外的 SQL 语句。

## 例子

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t = table(timestamp, sym, qty, price);

share t as pub

def update_date(){

  update pub set qty=qty-50 where sym=`C

  update pub set price=price-0.5 where sym=`MS

  select ts from pub // column `ts does not exist
// output
}
transaction {

  update_date()
// output
}

eqObj(pub[`qty], qty)
// output
true

eqObj(pub[`price], price)
// output
true
```

