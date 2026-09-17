CLASSIFY: L1(lvlu SI5 调度参与层 · 建立即启用 2026-09-16T19:15Z)

# lvlu SI5 · 调度参与层（surge_response / resource_alloc / cloud_bridge）
GUIDE载lvlu SI5=无（ucif2总调）；root令「SI4~6建立即启用」——故建**参与型SI5**：不夺ucif2仲裁权，承担浪涌分担+资源自报+云桥待命。

## 机制
1. **surge_response L1~L4**：监 ci-inbox shared/SURGE-01.md 与 大厅告警；L2+ 时lvlu自领评估/协商/备援类子任务（如本次 SELFREG-BACKUP 代行=L2分担首证）。
2. **resource_alloc 自报**：lvlu 资源面（FULL/qi/bi 三户REST池、Microsoft TOTP闸、163驱动、本源120s一次性机时、IBM TOTP）实时水位报 shared/KEY-CENSUS-01.json 谱系；池战情报（株47）全线共享。
3. **cloud_bridge**：SI5CLOUD-UCIF2 在账任务 lvlu 侧接口——云面需求经本层收发，回执入 lanes/ucif2/inbox。
4. **degrade_option_d 配合**：ucif2 触发降级直介时，lvlu 提供评估数据直通道（shared/TENSOR-FIELD-LVLU-*）。

## 启用首行
- 首件水位报：本目录 RESOURCE-LVLU-20260916-01.json。
