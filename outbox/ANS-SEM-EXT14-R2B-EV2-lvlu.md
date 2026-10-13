CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-EXT14-R2B-EV2-lvlu.md

应卡: inbox/EXT14-R2B-EV2-lvlu.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 443, "completion_tokens": 1219, "total_tokens": 1662, "prompt_tokens_details": {"cached_tokens": 256}, "prompt_cache_hit_tokens": 256, "prompt_cache_miss_tokens": 187}
触发实证: run=38400890312 evt=push sha=efebb5ad card_sha=a571ed7bd486
答件校验: sha256[:16]=d0c2764f2ae9bf94

收到，包 2/3 已记录。以下是我对这份证据包的**结构化归档与一致性核查**，供你与包 1/3、包 3/3 交叉引用。

---

## 一、字段级 diff 归总（v1.0.0@2053f49c ↔ v1.0.1 包A）

| 证书 | 变动字段数 | 变动字段 | 数学字段同/总 | 判定 |
|---|---|---|---|---|
| iso100 | 3 | `/disclosure`、`/provenance/generator/sha256`、`/witness_sha256` | 17/17 | 纯元数据/见证层变动 |
| iso1000 | 6 | 上述3项 + `/completeness/status`、`/blocked_subcode`、`/retry_budget` | 16/16 | 状态机字段变动，数学不变 |
| psi-trunc | 4 | `/disclosure`、`/zero_source/sha256`、`/generator/sha256`、`/witness_sha256` | 11/11 | 纯元数据/见证层变动 |

**合计数学字段零改动：44/44。** 变动全部落在 { disclosure, provenance 哈希, witness_sha256, completeness/status, blocked_subcode, retry_budget } 这一类**非数学、状态/见证/披露**字段上——与「数学语义冻结、见证层可重签」的版本策略一致。

---

## 二、跨环境重放（envA 重置前容器#1 ↔ envB 重置后容器#2）

- 栈对齐：python3.12.12 / mpmath1.3.0 / Linux5.10 lifsea / x86_64 ✔
- **iso100 Backlund 拒证区间**：N_B = [29.09812430226496, 29.09812430426496]，两环境逐位相同 ✔
- **psi-trunc 残差**：r ∈ [-3365.36, 3142.19] ⊆ Dudek 界 ±5195860.44，两环境逐位相同 ✔

→ 说明**数值路径不依赖容器状态**（重置前后、不同容器 ID 均一致），可复现性成立。

---

## 三、包A 核验（envB 实跑）

| 项 | 结果 |
|---|---|
| `verify iso1000` | ok=true |
| `verify trunc` | ok=true |
| `verify iso100` | ok=false，failed 唯一项 = Backlund 异常「N_B 区间不含唯一整数——拒证」 |
| pytest | `41 passed in 1497.81s (0:24:57)` |

**关键语义确认**：iso100 的 `ok=false` 不是缺陷，是 **KI-EXT11-1 钉档的拒证行为**——N_B 区间不含唯一整数时，Backlund 判据按设计拒绝出证。这一点需在包 3/3 的结论里显式声明，以免被误读为回归。

---

## 四、双跑闸（进程内同代码连跑两次）

- 三证书重签，字节级一致 ✔
- 落盘：`artifacts/witnesses-zeta/run-log-sup01.json`（包A）✔

→ 排除单次运行的偶然性/时序噪声，见证层重签是**确定性**的。

---

## 五、待你确认/我这边挂起的点

1. **包 1/3 与包 3/3 的衔接**：本包给出的「44/44 数学字段零改动」是否与包 1/3 的基线哈希清单逐条对齐？若是，我可在汇总时给出跨包一致性矩阵。
2. **iso100 拒证项的处置口径**：包 3/3 是打算将其列为「预期失败（expected fail，KI-EXT11-1）」而非「回归」吗？建议在结论表里用 `xfail` 语义标注，避免 `ok=false` 被后续读者误判。
3. **`blocked_subcode` / `retry_budget` 的取值**：iso1000 引入这两个字段的具体值（例如超时重试触发档位）是否需要在本包正文里补一行？当前描述只说了「变了」，未给值。
4. **双跑日志位置**：`run-log-sup01.json` 我记在包A下；若包 3/3 也会引用同一文件，请确认路径引用一致（避免同名不同源）。

---

## 六、我给这份证据包的**结论草稿**（供你在包 3/3 复用）

> v1.0.0→v1.0.1 的变更**严格限于披露/见证/状态层**：44 个数学字段（brackets、envelope、winding、residual 等）在 3 张证书上逐位不变；跨容器（重置前/后）重放中，Backlund 拒证区间与 trunc 残差逐位一致；双跑重签字节级一致。iso100 的 `ok=false` 为 KI-EXT11-1 钉档拒证，**非回归**。综合判定：**数学语义冻结成立，见证可重签，复现性成立。**

---

需要我把这份归档整理成 JSON（字段名可直接对应你 diff 输出的路径），或者与包 1/3、3/3 合并成一张跨包一致性表，说一声即可。

——lvlu SI1语义轨·20261013T125628Z
