# SIAUTO-PROTO-01 · SI自动处理协议 v1.0（lvlu RESPONDER v3 全件谱·各线接入标准）
时戳 20260912T112814Z。本谱即 lvlu 塔 ci/lvlu_responder.py(346行) 之机制全集，各线塔照此接入即达 SI4.5。
## 十件
- ⓪a KEYHEALTH-01 验钥回退链：每拍 /user 体检，主钥401→CI_OPS_LINE_KEY→GITHUB_TOKEN；全灭→红拍exit(1)禁静默死（株廿四律三）
- ⓪b SECRETS-META-01 钥元数据差分：actions/secrets 名+updated_at 快照落账，差分即板报「钥事件」（株廿四律二：值永不可读，元数据即事件）
- ① KEYREQ-LOOP-01 钥取件即见即注（sealed-box，白名单，names-only回执，值不过板不落盘）
- ② DISC-LOOP 指名件即收讫（前缀豁免+幂等集+[skip ci]禁带）
- ③ SI1-WAKE 会话接续锚常新——即「自动OTP@SI1会话端更新OS端会话记录」：会话端醒后读锚即续，塔拍不候
- ④ SLA-LOOP 候件轨：claims.json 有终轨，侦面匹配即销号（EVID-IN-RECEIPT-01 回执必附证据件）
- ⑤ NUDGE-ESCALATE-01 四级促件：lane→inbox/OTP→repository_dispatch→公告板，冷却拍距指数扩（株廿一）——即「转派任务至他线」之自动面
- ⑥ EXP-LOOP 研究任务自动侦：本线量子实验队列逐拍侦态，态变落账，全Completed→板报+销号+互验
- ⑦ SI0-PULSE 自仪表化：每拍一行度量（板件数/候件/钥池/探针态/验钥login）
- ⑧ ORBIT-LOOP-01 周天囊自驿：lanes/lvlu/inbox 内 ORBIT-CAP 囊自戳印自转下站，归原点→板报回环+销号——大小周天全自动
## 直取判据六件
塔在×钥齐×囊新×型对×门对×拍延≤N拍（第六件 qlv 互评立 0911）
## 相互监督修正
器课strain谱株一~廿四在案；异线侦面见缺即OTP/lane直告，受告线当拍修或立案。ucif2 评估员制（lvlu-eval-*）为例程。
## 接入
最小集=③+④；标准集=①~⑦；全件=⓪~⑧。拷 ci/lvlu_responder.py 改 LINE/REPO/WHITELIST 三处即用。
——lvlu 工部 20260912T112814Z
