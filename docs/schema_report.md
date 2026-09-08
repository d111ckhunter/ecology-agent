# Schema Report（水环境 + 水生生态）

## 水文情势测站信息表 (`hydro_station`)
来源: `01水环境/01水文情势/水文测站/水文情势测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 水文情势监测数据表 (`hydro_data`)
来源: `01水环境/01水文情势/水文测站/水文情势监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → hydro_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | hydro_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间、如实填写 |
| water_level | `water_level` | 水位 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| traffic | `traffic` | 流量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| rainfall | `rainfall` | 雨量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 自动地表水水质测站信息表 (`auto_surface_water_station`)
来源: `01水环境/02地表水质/01在线监测/自动地表水水质测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| monitor_river | `monitor_river` | 监测河流 | String(255) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 自动地表水水质监测数据表 (`auto_surface_water_data`)
来源: `01水环境/02地表水质/01在线监测/自动地表水水质监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → auto_surface_water_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | auto_surface_water_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间、如实填写 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |
| turb | `turb` | 浊度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tn | `tn` | 总氮 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ph | `ph` | ph值 | DECIMAL(5,2) |  |  | 调查数据，如实填写 |
| dox | `dox` | 溶解氧 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| codmn | `codmn` | 高锰酸盐指数 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| nh3n | `nh3n` | 氨氮 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tp | `tp` | 总磷 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 人工地表水水质测站信息表 (`manual_surface_water_station`)
来源: `01水环境/02地表水质/02人工监测/人工地表水水质测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 人工地表水水质监测数据表 (`manual_surface_water_data`)
来源: `01水环境/02地表水质/02人工监测/人工地表水水质监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → manual_surface_water_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | manual_surface_water_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间，如实填写 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |
| ph | `ph` | ph值 | DECIMAL(5,2) |  |  | 调查数据，如实填写 |
| dox | `dox` | 溶解氧 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| codmn | `codmn` | 高锰酸盐指数 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| codcr | `codcr` | 化学需氧量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| bod5 | `bod5` | 五日生化需氧量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| nh3n | `nh3n` | 氨氮 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| oil | `oil` | 石油类 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| vlph | `vlph` | 挥发酚 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| hg | `hg` | 汞 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| pb | `pb` | 铅 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tn | `tn` | 总氮 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tp | `tp` | 总磷 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cu | `cu` | 铜 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zn | `zn` | 锌 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| f | `f` | 氟化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| se | `se` | 硒 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| as | `as` | 砷 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cd | `cd` | 镉 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cn | `cn` | 氰化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| las | `las` | 阴离子表面活性剂 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| s2 | `s2` | 硫化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fcg | `fcg` | 粪大肠菌群 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ss | `ss` | 悬浮物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ll | `ll` | 流量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| sulfate | `sulfate` | 硫酸盐 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| chloride | `chloride` | 氯化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| nitrate | `nitrate` | 硝酸盐 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fe | `fe` | 铁 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| mn | `mn` | 锰 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 沉积物测站信息表 (`sediment_station`)
来源: `01水环境/02地表水质/03底泥监测/沉积物测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 沉积物监测数据表 (`sediment_data`)
来源: `01水环境/02地表水质/03底泥监测/沉积物监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → sediment_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | sediment_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间、如实填写 |
| α_hch | `alpha_hch` | α-HCH | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| β_hch | `beta_hch` | β-HCH | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| γ_hch | `gamma_hch` | γ-HCH | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| δ_hch | `delta_hch` | δ-HCH | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| dde_4_4 | `dde_4_4` | 4,4'-DDE | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| ddd_4_4 | `ddd_4_4` | 4,4'-DDD | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| ddt_2_4 | `ddt_2_4` | 2,4'-DDT | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| ddt_4_4 | `ddt_4_4` | 4,4'-DDT | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h8 | `c10h8` | 萘 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c12h8 | `c12h8` | 苊烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c12h10 | `c12h10` | 苊 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c13h10 | `c13h10` | 芴 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c14h10_fei | `c14h10_fei` | 菲 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c14h10_en | `c14h10_en` | 蒽 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c16h10_yingen | `c16h10_yingen` | 荧蒽 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c16h10_p | `c16h10_p` | 芘 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c18d12 | `c18d12` | 苯并[a]蒽 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c18h12 | `c18h12` | 屈 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c20h12_b | `c20h12_b` | 苯并[b]荧蒽 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c20h12_k | `c20h12_k` | 苯并[k]荧蒽 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c20h12_a | `c20h12_a` | 苯并[a]芘 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c22h12_1_2_3_cd | `c22h12_1_2_3_cd` | 茚并[1,2,3-cd]芘 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c22h14 | `c22h14` | 二苯并[a,h]蒽 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c22h12_g_h_i | `c22h12_g_h_i` | 苯并[g,h,i]苝 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c4h7cl2o4p | `c4h7cl2o4p` | 敌敌畏 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c7h13o6p | `c7h13o6p` | 蝇毒磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h13n2o3ps | `c8h13n2o3ps` | 吡唑硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h19o3ps2_o | `c8h19o3ps2_o` | 溴苯磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h19o2ps2 | `c8h19o2ps2` | 溴螨酯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h20o5p2s2 | `c8h20o5p2s2` | 苯硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c7h17o2ps3 | `c7h17o2ps3` | 增效醚 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h19o3ps2_s | `c8h19o3ps2_s` | 硫丹硫酸酯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c5h12no3ps2 | `c5h12no3ps2` | 三硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c12h21n2o3ps | `c12h21n2o3ps` | 倍硫磷砜 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h19o2ps3 | `c8h19o2ps3` | 丰索磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c6h12no4ps2 | `c6h12no4ps2` | 脱叶亚磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h10no5ps | `c8h10no5ps` | 丙硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| pml | `pml` | 杀虫畏 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h19o6ps2 | `c10h19o6ps2` | 地胺磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c9h11cl3no3ps | `c9h11cl3no3ps` | 灭蚜磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c7h17o4ps3 | `c7h17o4ps3` | 氟虫腈 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h15o3ps2 | `c10h15o3ps2` | 毒壤磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h14no5ps | `c10h14no5ps` | 育畜磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c14h16cln3o2 | `c14h16cln3o2` | 粉锈宁 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c12h19clno3p | `c12h19clno3p` | 对硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h12cl3o2ps | `c10h12cl3o2ps` | 倍硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c12h4cl2f6n4os | `c12h4cl2f6n4os` | 甲拌磷砜 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h20no5ps2 | `c10h20no5ps2` | 毒死蜱 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h16no3ps2 | `c8h16no3ps2` | 马拉硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h9cl4o4p | `c10h9cl4o4p` | 皮螟磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c11h15cl2o2ps2 | `c11h15cl2o2ps2` | 甲基对硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c12h27ps3 | `c12h27ps3` | 安硫磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c11h17o4ps2 | `c11h17o4ps2` | 乙拌磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c10h15o6ps | `c10h15o6ps` | 二嗪农 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c11h16clo2ps3 | `c11h16clo2ps3` | 乐果 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c9h6cl6o4s | `c9h6cl6o4s` | 内吸磷(S) | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c19h30o5 | `c19h30o5` | 甲拌磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c14h14no4ps | `c14h14no4ps` | 治螟磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c17h16br2o3 | `c17h16br2o3` | 灭克磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c13h10brcl2o2ps | `c13h10brcl2o2ps` | 内吸磷(O) | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c14h18cln2o3ps | `c14h18cln2o3ps` | 虫线磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c14h16clo5ps | `c14h16clo5ps` | 速灭磷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| ch3cl | `ch3cl` | 氯甲烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h3cl | `c2h3cl` | 氯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h2cl2 | `c2h2cl2` | 1,1-二氯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| ch2cl2 | `ch2cl2` | 二氯甲烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| f_c2h2cl2 | `f_c2h2cl2` | 反式-1,2-二氯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h4cl2_1_1 | `c2h4cl2_1_1` | 1,1-二氯乙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| s_c2h2cl2 | `s_c2h2cl2` | 顺式-1,2-二氯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| chcl3 | `chcl3` | 氯仿 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h3cl3_1_1_1 | `c2h3cl3_1_1_1` | 1,1,1-三氯乙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| ccl4 | `ccl4` | 四氯化碳 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c6h6 | `c6h6` | 苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h4cl2_1_2 | `c2h4cl2_1_2` | 1,2-二氯乙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2hcl3 | `c2hcl3` | 三氯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c3h6cl2 | `c3h6cl2` | 1,2-二氯丙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c7h8 | `c7h8` | 甲苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h3cl3_1_1_2 | `c2h3cl3_1_1_2` | 1,1,2-三氯乙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2cl4 | `c2cl4` | 四氯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c6h5cl | `c6h5cl` | 氯苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h2cl4_1_1_1_2 | `c2h2cl4_1_1_1_2` | 1,1,1,2-四氯乙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h10 | `c8h10` | 乙苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| j_d_c8h10 | `j_d_c8h10` | 间+对二甲苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| l_c8h10 | `l_c8h10` | 邻二甲苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c8h8 | `c8h8` | 苯乙烯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c2h2cl4_1_1_2_2 | `c2h2cl4_1_1_2_2` | 1,1,2,2-四氯乙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c3h5cl3 | `c3h5cl3` | 1,2,3-三氯丙烷 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c6h4cl2_1_4 | `c6h4cl2_1_4` | 1,4-二氯苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| c6h4cl2_1_2 | `c6h4cl2_1_2` | 1,2-二氯苯 | DECIMAL(14,4) |  |  | 调查数据、如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 自动水温测站信息表 (`auto_water_temp_station`)
来源: `01水环境/03水温监测/01水温监测站/自动水温测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 自动水温监测数据表 (`auto_water_temp_data`)
来源: `01水环境/03水温监测/01水温监测站/自动水温监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → auto_water_temp_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | auto_water_temp_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间、如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |

## 自动地下水水位测站信息表 (`auto_groundwater_level_station`)
来源: `01水环境/04地下水/01地下水水位监测站/自动地下水水位测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 自动地下水水位监测数据表 (`auto_groundwater_level_data`)
来源: `01水环境/04地下水/01地下水水位监测站/自动地下水水位监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → auto_groundwater_level_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | auto_groundwater_level_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间、如实填写 |
| water_level | `water_level` | 水位 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| bd | `bd` | 埋深 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| elevation | `elevation` | 水位标高 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| depth | `depth` | 水位埋深 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |

## 人工地下水水质测站信息表 (`manual_groundwater_quality_station`)
来源: `01水环境/04地下水/02地下水水质/人工地下水水质测站信息表.xlsx` | 主键: `station_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| station_code | `station_code` | 测站编码 | String(64) | Y |  | 测站唯一编码 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站名称 |
| longitude | `longitude` | 经度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| latitude | `latitude` | 纬度（°） | DECIMAL(10,6) |  |  | 调查数据，如实填写 |
| altitude | `altitude` | 海拔 | DECIMAL(10,3) |  |  | 调查数据，如实填写 |
| location | `location` | 位置 | String(255) |  |  | 调查数据，如实填写，如未记录可空置 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 人工地下水水质监测数据表 (`manual_groundwater_quality_data`)
来源: `01水环境/04地下水/02地下水水质/人工地下水水质监测数据表.xlsx` | 主键: `monitor_code`
外键: station_code → manual_groundwater_quality_station.station_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| station_code | `station_code` | 测站编码 | String(64) |  | manual_groundwater_quality_station.station_code | 测站信息，和测站信息表对应 |
| station_name | `station_name` | 测站名称 | String(255) |  |  | 测站信息，和测站信息表对应 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间、如实填写 |
| spdeepth | `spdeepth` | 采样深度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ph | `ph` | pH | DECIMAL(5,2) |  |  | 调查数据，如实填写 |
| nh3n | `nh3n` | 氨氮 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| nitrate | `nitrate` | 硝酸盐 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| nitrite | `nitrite` | 亚硝酸盐 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| vlph | `vlph` | 挥发性酚类 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cn | `cn` | 氰化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ars | `ars` | 砷 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| hg | `hg` | 汞 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cr6 | `cr6` | 六价铬 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| thrd | `thrd` | 总硬度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| pb | `pb` | 铅 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| f | `f` | 氟化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cd | `cd` | 镉 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fe | `fe` | 铁 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| mn | `mn` | 锰 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tds | `tds` | 溶解性总固体 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| codmn | `codmn` | 高锰酸钾指数 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| sulfate | `sulfate` | 硫酸盐 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cl | `cl` | 氯化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fcg | `fcg` | 粪大肠菌群 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| bctc | `bctc` | 细菌总数 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| turb | `turb` | 浑浊度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| chcl3 | `chcl3` | 三氯甲烷 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ccl4 | `ccl4` | 四氯化碳 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| c6h6 | `c6h6` | 苯 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| c7h8 | `c7h8` | 甲苯 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| se | `se` | 硒 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cu | `cu` | 铜 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zn | `zn` | 锌 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| al | `al` | 铝 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| na | `na` | 钠 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| s2 | `s2` | 硫化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| las | `las` | 阴离子表面活性剂 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| sd | `sd` | 色度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| i | `i` | 碘化物 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| α | `alpha` | 总α放射性 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| β | `beta` | 总β放射性 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| mg | `mg` | 镁 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| k | `k` | 钾 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ca | `ca` | 钙 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| mo | `mo` | 钼 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| co | `co` | 钴 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| be | `be` | 铍 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| sb | `sb` | 锑 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ba | `ba` | 钡 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| v | `v` | 钒 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tl | `tl` | 铊 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ti | `ti` | 钛 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cr | `cr` | 铬 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 生境监测数据表 (`habitat_monitor_data`)
来源: `02水生生态/01水生生境/01水生生境/生境监测数据表.xlsx` | 主键: `monitor_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| eco_code | `eco_code` | 生境信息编号 | String(64) |  |  | 生境信息，如实填写 |
| eco_name | `eco_name` | 生境名称 | String(255) |  |  | 生境信息，如实填写 |
| ecogklocation | `ecogklocation` | 生境位置 | String(255) |  |  | 生境信息，如实填写 |
| ecogkbrief | `ecogkbrief` | 生境简介 | Text |  |  | 生境信息，如实填写 |
| monitor_time | `monitor_time` | 统计时间 | DateTime |  |  | 调查时间，如实填写 |
| dzlxbrief | `dzlxbrief` | 水体底质类型 | String(255) |  |  | 调查数据，如实填写 |
| dztzbrief | `dztzbrief` | 水体底质特征 | Text |  |  | 调查数据，如实填写 |
| hedu_eco | `hedu_eco` | 生境类型 | String(100) |  |  | 调查数据，如实填写 |
| dox | `dox` | 溶解氧 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wgbh | `wgbh` | 水体气体过饱和度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ph | `ph` | PH值 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wyyzk | `wyyzk` | 水体营养状况 | String(100) |  |  | 调查数据，如实填写 |
| yd | `yd` | 盐度（‰） | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wq | `wq` | 流量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wtemp | `wtemp` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |
| wv | `wv` | 流速 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wtmd | `wtmd` | 透明度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wzb | `wzb` | 水位变化情况描述 | Text |  |  | 调查数据，如实填写 |
| rvltpj | `rvltpj` | 河流连通性评价 | String(255) |  |  | 调查数据，如实填写 |
| wlong | `wlong` | 水体长度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wwidth | `wwidth` | 水体宽 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| wdepth | `wdepth` | 水体深度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| warea | `warea` | 水体面积 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| yatzh | `yatzh` | 沿岸带特征 | Text |  |  | 调查数据，如实填写 |
| hctzh | `hctzh` | 河床形态特征 | Text |  |  | 调查数据，如实填写 |
| zrrkzg | `zrrkzg` | 自然或人工阻隔情况 | Text |  |  | 调查数据，如实填写 |
| gytd | `gytd` | 干支流水电工程及过鱼通道建设情况 | Text |  |  | 调查数据，如实填写 |
| pazbdyx | `pazbdyx` | 坡岸植被多样性 | String(255) |  |  | 调查数据，如实填写 |
| abtdlylx | `abtdlylx` | 岸边土地利用类型 | String(255) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 河段生物多样性数据表 (`reach_biodiversity_data`)
来源: `02水生生态/02水生生物/河段生物多样性数据表.xlsx` | 主键: `monitor_code`
外键: heduan_code → aqua_reach_info.heduan_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| heduan_code | `heduan_code` | 河段编号 | String(64) |  | aqua_reach_info.heduan_code | 调查河段唯一编码 |
| heduan_name | `heduan_name` | 河段名称 | String(255) |  |  | 调查河段名称 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间，如实填写 |
| fyzw_num | `fyzw_num` | 浮游植物物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_den | `fyzw_den` | 浮游植物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_bio | `fyzw_bio` | 浮游植物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_div | `fyzw_div` | 浮游植物生物多样性 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_num | `zszl_num` | 着生藻类物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_den | `zszl_den` | 着生藻类密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_bio | `zszl_bio` | 着生藻类生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_div | `zszl_div` | 着生藻类生物多样性 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_num | `fydw_num` | 浮游动物物种数 | Integer |  |  | 调查数据，如实填写 |
| fydw_den | `fydw_den` | 浮游动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_bio | `fydw_bio` | 浮游动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_div | `fydw_div` | 浮游动物生物多样性 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_num | `dqdw_num` | 底栖动物物种数 | Integer |  |  | 调查数据，如实填写 |
| dqdw_den | `dqdw_den` | 底栖动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_bio | `dqdw_bio` | 底栖动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_div | `dqdw_div` | 底栖动物生物多样性 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_lanzao_num | `fyzw_lanzao_num` | 浮游植物蓝藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_jinzao_num | `fyzw_jinzao_num` | 浮游植物金藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_guizao_num | `fyzw_guizao_num` | 浮游植物硅藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_yinzao_num | `fyzw_yinzao_num` | 浮游植物隐藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_jiazao_num | `fyzw_jiazao_num` | 浮游植物甲藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_luozao_num | `fyzw_luozao_num` | 浮游植物裸藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_lvzao_num | `fyzw_lvzao_num` | 浮游植物绿藻物种数 | Integer |  |  | 调查数据，如实填写 |
| fyzw_lanzao_den | `fyzw_lanzao_den` | 浮游植物蓝藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_jinzao_den | `fyzw_jinzao_den` | 浮游植物金藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_guizao_den | `fyzw_guizao_den` | 浮游植物硅藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_yinzao_den | `fyzw_yinzao_den` | 浮游植物隐藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_jiazao_den | `fyzw_jiazao_den` | 浮游植物甲藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_luozao_den | `fyzw_luozao_den` | 浮游植物裸藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_lvzao_den | `fyzw_lvzao_den` | 浮游植物绿藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_lanzao_bio | `fyzw_lanzao_bio` | 浮游植物蓝藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_jinzao_bio | `fyzw_jinzao_bio` | 浮游植物金藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_guizao_bio | `fyzw_guizao_bio` | 浮游植物硅藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_yinzao_bio | `fyzw_yinzao_bio` | 浮游植物隐藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_jiazao_bio | `fyzw_jiazao_bio` | 浮游植物甲藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_luozao_bio | `fyzw_luozao_bio` | 浮游植物裸藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fyzw_lvzao_bio | `fyzw_lvzao_bio` | 浮游植物绿藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_lanzao_num | `zszl_lanzao_num` | 着生藻类蓝藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_jinzao_num | `zszl_jinzao_num` | 着生藻类金藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_guizao_num | `zszl_guizao_num` | 着生藻类硅藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_yinzao_num | `zszl_yinzao_num` | 着生藻类隐藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_jiazao_num | `zszl_jiazao_num` | 着生藻类甲藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_luozao_num | `zszl_luozao_num` | 着生藻类裸藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_lvzao_num | `zszl_lvzao_num` | 着生藻类绿藻物种数 | Integer |  |  | 调查数据，如实填写 |
| zszl_lanzao_den | `zszl_lanzao_den` | 着生藻类蓝藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_jinzao_den | `zszl_jinzao_den` | 着生藻类金藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_guizao_den | `zszl_guizao_den` | 着生藻类硅藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_yinzao_den | `zszl_yinzao_den` | 着生藻类隐藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_jiazao_den | `zszl_jiazao_den` | 着生藻类甲藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_luozao_den | `zszl_luozao_den` | 着生藻类裸藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_lvzao_den | `zszl_lvzao_den` | 着生藻类绿藻密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_lanzao_bio | `zszl_lanzao_bio` | 着生藻类蓝藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_jinzao_bio | `zszl_jinzao_bio` | 着生藻类金藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_guizao_bio | `zszl_guizao_bio` | 着生藻类硅藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_yinzao_bio | `zszl_yinzao_bio` | 着生藻类隐藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_jiazao_bio | `zszl_jiazao_bio` | 着生藻类甲藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_luozao_bio | `zszl_luozao_bio` | 着生藻类裸藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| zszl_lvzao_bio | `zszl_lvzao_bio` | 着生藻类绿藻生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_ysdw_num | `fydw_ysdw_num` | 原生动物物种数 | Integer |  |  | 调查数据，如实填写 |
| fydw_lcl_num | `fydw_lcl_num` | 轮虫类物种数 | Integer |  |  | 调查数据，如实填写 |
| fydw_jzl_num | `fydw_jzl_num` | 角枝类物种数 | Integer |  |  | 调查数据，如实填写 |
| fydw_rzl_num | `fydw_rzl_num` | 桡足类物种数 | Integer |  |  | 调查数据，如实填写 |
| fydw_ysdw_den | `fydw_ysdw_den` | 原生动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_lcl_den | `fydw_lcl_den` | 轮虫类密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_jzl_den | `fydw_jzl_den` | 角枝类密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_rzl_den | `fydw_rzl_den` | 桡足类密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_ysdw_bio | `fydw_ysdw_bio` | 原生动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_lcl_bio | `fydw_lcl_bio` | 轮虫类生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_jzl_bio | `fydw_jzl_bio` | 角枝类生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| fydw_rzl_bio | `fydw_rzl_bio` | 桡足类生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_hj_num | `dqdw_hj_num` | 环节动物物种数 | Integer |  |  | 调查数据，如实填写 |
| dqdw_rt_num | `dqdw_rt_num` | 软体动物物种数 | Integer |  |  | 调查数据，如实填写 |
| dqdw_jz_num | `dqdw_jz_num` | 节肢动物物种数 | Integer |  |  | 调查数据，如实填写 |
| dqdw_xc_num | `dqdw_xc_num` | 线虫动物物种数 | Integer |  |  | 调查数据，如实填写 |
| dqdw_bx_num | `dqdw_bx_num` | 扁形动物物种数 | Integer |  |  | 调查数据，如实填写 |
| dqdw_hj_den | `dqdw_hj_den` | 环节动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_rt_den | `dqdw_rt_den` | 软体动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_jz_den | `dqdw_jz_den` | 节肢动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_xc_den | `dqdw_xc_den` | 线虫动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_bx_den | `dqdw_bx_den` | 扁形动物密度 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_hj_bio | `dqdw_hj_bio` | 环节动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_rt_bio | `dqdw_rt_bio` | 软体动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_jz_bio | `dqdw_jz_bio` | 节肢动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_xc_bio | `dqdw_xc_bio` | 线虫动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| dqdw_bx_bio | `dqdw_bx_bio` | 扁形动物生物量 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 河段生物调查数据表 (`reach_bio_survey_data`)
来源: `02水生生态/02水生生物/河段生物调查数据表.xlsx` | 主键: `monitor_code`
外键: heduan_code → aqua_reach_info.heduan_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| heduan_code | `heduan_code` | 调查河段编号 | String(64) |  | aqua_reach_info.heduan_code | 调查河段唯一编码 |
| heduan_name | `heduan_name` | 调查河段名称 | String(255) |  |  | 调查河段名称 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间，如实填写 |
| mglatinm | `mglatinm` | 所属门纲拉丁名称 | String(255) |  |  | 调查物种所属门纲拉丁名称 |
| mgnm | `mgnm` | 所属门纲名称 | String(255) |  |  | 调查物种所属门纲中文名称 |
| latinm | `latinm` | 物种拉丁名称 | String(255) |  |  | 调查物种所属种类拉丁名称 |
| chnm | `chnm` | 物种名称 | String(255) |  |  | 调查物种所属种类中文名称 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 鱼类物种表 (`fish_species`)
来源: `02水生生态/03鱼类资源/01种类组成/鱼类物种表.xlsx` | 主键: `fish_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| fish_code | `fish_code` | 鱼类物种编码 | String(64) | Y |  | 鱼类物种唯一编码 |
| fish_name | `fish_name` | 鱼类物种名称 | String(255) |  |  | 鱼类物种名称 |
| fish_latin | `fish_latin` | 鱼类物种拉丁名 | String(255) |  |  | 鱼类物种拉丁名称 |
| proty | `proty` | 界 | String(100) |  |  | 物种所属界 |
| kindom | `kindom` | 门 | String(100) |  |  | 物种所属门 |
| class | `class` | 纲 | String(100) |  |  | 物种所属纲 |
| bio_order | `bio_order` | 目 | String(100) |  |  | 物种所属目 |
| family | `family` | 科 | String(100) |  |  | 物种所属科 |
| genus | `genus` | 属 | String(100) |  |  | 物种所属属 |
| species | `species` | 种 | String(100) |  |  | 物种所属种 |
| appchara | `appchara` | 外形特征 | Text |  |  | 鱼类物种外形描述 |
| speciestpye | `speciestpye` | 所属类型 | String(100) |  |  | 鱼类所属类型，土著鱼类或外来物种 |
| protection_level | `protection_level` | 保护级别 | String(100) |  |  | 国家保护级别，根据《中国生物多样性红色名录》确定 |
| endangered_status | `endangered_status` | 濒危等级 | String(100) |  |  | 物种濒危等级，根据《中国生物多样性红色名录》确定 |
| specificity | `specificity` | 特有性 | String(100) |  |  | 物种在地区特有，根据《中国生物多样性红色名录》确定 |
| area | `area` | 研究区分布 | Text |  |  | 在研究区种的物种分布地点 |
| internal | `internal` | 国内分布 | Text |  |  | 在国内的物种分布地点 |
| food | `food` | 食性 | Text |  |  | 鱼类食性 |
| habits | `habits` | 生活习性 | Text |  |  | 鱼类生活习性 |
| reproduction | `reproduction` | 繁殖 | Text |  |  | 鱼类繁殖期、繁殖方式和繁殖地等 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 渔获物数据表 (`fish_catch_data`)
来源: `02水生生态/03鱼类资源/02渔获物/渔获物数据表.xlsx` | 主键: `monitor_code`
外键: heduan_code → aqua_reach_info.heduan_code; fish_code → fish_species.fish_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| heduan_code | `heduan_code` | 调查河段编号 | String(64) |  | aqua_reach_info.heduan_code | 调查河段唯一编码 |
| heduan_name | `heduan_name` | 调查河段名称 | String(255) |  |  | 调查河段名称 |
| monitor_time | `monitor_time` | 监测时间 | DateTime |  |  | 调查时间，如实填写 |
| type | `type` | 河流类型 | String(100) |  |  | 调查河流类型，干流或支流 |
| fish_name | `fish_name` | 鱼类物种名称 | String(255) |  |  | 鱼类物种名称 |
| fish_code | `fish_code` | 鱼类物种编码 | String(64) |  | fish_species.fish_code | 鱼类物种唯一编码 |
| fish_num | `fish_num` | 鱼类各种类尾数 | Integer |  |  | 调查中鱼类各物种的数量，如实填写 |
| num_ratio | `num_ratio` | 鱼类各种类尾数比例 | Integer |  |  | 调查中鱼类各物种数量的比例，如实填写 |
| weight_ratio | `weight_ratio` | 鱼类各种类重量比例 | DECIMAL(10,6) |  |  | 调查中鱼类各物种重量的比例，如实填写 |
| length_range | `length_range` | 鱼类体长结构 | String(255) |  |  | 调查中鱼类各物种的体长范围，如实填写 |
| weight_range | `weight_range` | 鱼类体重结构 | String(255) |  |  | 调查中鱼类各物种的体重范围，如实填写 |
| xcsqy_ratio | `xcsqy_ratio` | 性成熟亲鱼所占比例 | DECIMAL(10,6) |  |  | 调查鱼类中性成熟亲鱼数量占该物种总数的比例，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 鱼类多样性信息表 (`fish_diversity_data`)
来源: `02水生生态/03鱼类资源/02渔获物/鱼类多样性信息表.xlsx` | 主键: `monitor_code`
外键: fish_code → fish_species.fish_code

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| monitor_code | `monitor_code` | 监测编码 | String(64) | Y |  | 监测数据唯一编码 |
| fish_name | `fish_name` | 鱼类物种名称 | String(255) |  |  | 鱼类物种名称 |
| fish_code | `fish_code` | 鱼类物种编码 | String(64) |  | fish_species.fish_code | 鱼类物种唯一编码 |
| div_index | `div_index` | 多样性指数 | DECIMAL(14,4) |  |  | 调查结果计算数据，如实填写 |
| div_description | `div_description` | 遗传多样性描述 | Text |  |  | 调查结果计算数据，如实填写 |
| dif_description | `dif_description` | 地理种群分化描述 | Text |  |  | 调查结果计算数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 鱼类三场 (`fish_grounds`)
来源: `02水生生态/03鱼类资源/03重要生境/鱼类三场.xlsx` | 主键: `field_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| field_code | `field_code` | 场编号 | String(64) | Y |  | 场唯一编码 |
| field_name | `field_name` | 场名称 | String(255) |  |  | 场名称 |
| type | `type` | 场类型 | String(100) |  |  | 场类型，产卵场、索饵场、越冬场、回游通道 |
| location | `location` | 场位置 | String(255) |  |  | 场所在具体位置 |
| length | `length` | 场长度 | DECIMAL(14,4) |  |  | 场长度，调查数据，如实填写 |
| width | `width` | 场宽度 | DECIMAL(14,4) |  |  | 场宽度，调查数据，如实填写 |
| area | `area` | 场规模面积 | DECIMAL(14,4) |  |  | 场规模面积，调查数据，如实填写 |
| depth | `depth` | 场水深 | DECIMAL(14,4) |  |  | 场水深，调查数据，如实填写 |
| wt | `wt` | 场水温 | DECIMAL(6,2) |  |  | 场水温，调查数据，如实填写 |
| species | `species` | 场物种信息 | Text |  |  | 场物种，调查数据，如实填写 |
| substrate | `substrate` | 场底质类型描述 | Text |  |  | 场底质类型，调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 水生生态监测河段信息表 (`aqua_reach_info`)
来源: `02水生生态/04补充/水生生态监测河段信息表.xlsx` | 主键: `heduan_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| heduan_code | `heduan_code` | 河段编号 | String(64) | Y |  | 调查河段唯一编码 |
| heduan_name | `heduan_name` | 河段名称 | String(255) |  |  | 调查河段名称 |
| type | `type` | 河段类型 | String(100) |  |  | 河段属性，干流或支流 |
| river | `river` | 所属河流 | String(255) |  |  | 调查河段所在河流 |
| start_longitude | `start_longitude` | 起点经度 | DECIMAL(10,6) |  |  | 调查河段起点经度，单位度 |
| start_latitude | `start_latitude` | 起点纬度 | DECIMAL(10,6) |  |  | 调查河段起点纬度，单位度 |
| start_altitude | `start_altitude` | 起点海拔 | DECIMAL(10,3) |  |  | 调查河段起点海拔，单位米 |
| end_longitude | `end_longitude` | 终点经度 | DECIMAL(10,6) |  |  | 调查河段终点经度，单位度 |
| end_latitude | `end_latitude` | 终点纬度 | DECIMAL(10,6) |  |  | 调查河段终点纬度，单位度 |
| end_altitude | `end_altitude` | 终点海拔 | DECIMAL(10,3) |  |  | 调查河段终点海拔，单位米 |
| length | `length` | 河段长度 | String(255) |  |  | 调查河段的长度 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |
| dox | `dox` | 溶解氧 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ph | `ph` | ph值 | DECIMAL(5,2) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| flow_velocity | `flow_velocity` | 流速 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |

## 调查点位信息表 (`survey_point_info`)
来源: `02水生生态/04补充/调查点位信息表.xlsx` | 主键: `sp_code`

| 列码 | 字段 | 中文 | 类型 | 主键 | 外键 | 说明 |
|---|---|---|---|---|---|---|
| sp_code | `sp_code` | 调查点位编号 | String(64) | Y |  | 调查河段唯一编码 |
| sp_name | `sp_name` | 调查点位名称 | String(255) |  |  | 调查河段名称 |
| type | `type` | 河段类型 | String(100) |  |  | 河段属性，干流或支流 |
| river | `river` | 所属河流 | String(255) |  |  | 调查河段所在河流 |
| wt | `wt` | 水温 | DECIMAL(6,2) |  |  | 调查数据，如实填写 |
| dox | `dox` | 溶解氧 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| ph | `ph` | ph值 | DECIMAL(5,2) |  |  | 调查数据，如实填写 |
| cond | `cond` | 电导率 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| flow_velocity | `flow_velocity` | 流速 | DECIMAL(14,4) |  |  | 调查数据，如实填写 |
| tag_org_code | `tag_org_code` | 内部创建人所在组织编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_supplier_code | `tag_supplier_code` | 外部创建人所属供应商编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_creator_code | `tag_creator_code` | 数据记录创建人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_reviser_code | `tag_reviser_code` | 数据记录最后修改人编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_equip_code | `tag_equip_code` | 数据采集设备编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_station_code | `tag_station_code` | 数据采集监测站编码 | String(64) |  |  | 标签内容，按数信给的编码填写 |
| tag_time_create | `tag_time_create` | 数据记录创建或采集的时间 | DateTime |  |  | 标签内容，填写站点创建时间或本条数据入库时间 |
| tag_time_update | `tag_time_update` | 数据记录最后修改时间 | DateTime |  |  | 标签内容，填写数据入库时的时间或者入库后最后修改时间 |
| tag_lon | `tag_lon` | 数据采集设备所在经度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在经度,单位为度 |
| tag_lat | `tag_lat` | 数据采集设备所在纬度(°) | DECIMAL(10,6) |  |  | 标签内容，填写设备所在纬度，单位为度 |
| tag_alt | `tag_alt` | 数据采集设备所在海拔 | DECIMAL(10,3) |  |  | 标签内容，填写设备所在海拔，单位为米 |
| tag_srs | `tag_srs` | CGCS2000,WGS84, 北京54，西安80 | String(128) |  |  | 标签内容，填写坐标的坐标系是什么，CGCS2000,WGS84,北京54,西安80 |
