# moveHotDataToColdVolume

## 语法

`moveHotDataToColdVolume([checkRange=240])`

## 参数

**checkRange** 整数，单位为小时，默认值为 10 天，即 240 小时。用于设置需迁移至
*coldVolumes* 的数据的时间范围。设置后，时间范围在 [当前时间 - *hoursToColdVolumes* -
*checkRange*, 当前时间 - *hoursToColdVolumes*) 内的数据将会被迁移至
*coldVolumes*。

## 详情

强制触发将用户指定范围的数据转存至 *coldVolumes*。

注：

* 该命令仅对当前节点有效。集群环境中，可通过 `pnodeRun`
  调用该函数，使其在其它节点生效。
* 该命令设置的转存策略与 [setRetentionPolicy](../s/setRetentionPolicy.md)
  设置的转存策略的有区别，详情请参考 [TieredStorage](../../db_distr_comp/db/tiered_storage.md)。

