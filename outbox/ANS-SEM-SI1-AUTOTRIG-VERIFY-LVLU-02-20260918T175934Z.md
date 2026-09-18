CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-SI1-AUTOTRIG-VERIFY-LVLU-02-20260918T175934Z.md

应卡: inbox/SI1-AUTOTRIG-VERIFY-LVLU-02-20260918T175934Z.md
引擎: KIMI_API_KEY/kimi-k3 usage={"prompt_tokens": 288, "completion_tokens": 1055, "total_tokens": 1343, "completion_tokens_details": {"reasoning_tokens": 642}, "prompt_tokens_details": {"cache_write_tokens": 256}}
触发实证: run=35377646784 evt=push sha=85d1d04b card_sha=1733151863be
答件校验: sha256[:16]=1e55b7da47c8ad0b

诚实缺口先行：我看不到、也生成不了真实答头实证。run/evt/sha/card_sha 与「答件校验 sha256[:16]」只能由外层编排/落盘层在投递时计算附加；我在对话内无 run id、无卡体字节、无哈希工具，无法自控自证。若要求模型"自带校验"，等于把鉴证责任下放给被鉴证者——此点应作缺口入册，不应伪造一串 sha 充合规（级名不滥）。

1) 不能。实证字段属传输/落盘层职责；模型只产正文。验证方应核对外层附加字段与卡体规范字节的重算哈希是否一致，而非信任答内自述。

2) 不应重复落盘。键=卡名+卡hash 且 hash 覆盖规范字节（剔除时间戳/nonce/显示格式）时，重放命中唯一约束，返回既存句柄/已确认态。前提：查重与写入原子同事务、唯一索引在线。若是先写后查、跨进程无约束、或 hash 混入易变字段，则键漂移/竞态会重复——属实现缺陷，按负结果入册并补唯一约束+重算比对。

3) 同键跳过。no-json 是确定性语义失败：负结果一旦入册并参与幂等判定，重放只应回读该负结果，不盲目重试；仅当卡体修订致 hash 变更（新键）或人工解除/策略升级时才重入。瞬时故障（超时/IO）可指数退避重试，但须与确定性失败分流。若"入册"仅作日志不入幂等判定，no-json 卡会被反复重试——此为二次缺陷，应立即三即：即停同键重试、即补负结果唯一键、即册登记根因。

——lvlu SI1语义轨·20260918T180036Z
