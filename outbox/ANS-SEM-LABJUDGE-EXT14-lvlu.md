CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-EXT14-lvlu.md

应卡: inbox/LABJUDGE-EXT14-lvlu.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 795, "completion_tokens": 1852, "total_tokens": 2647, "prompt_tokens_details": {"cached_tokens": 640}, "prompt_cache_hit_tokens": 640, "prompt_cache_miss_tokens": 155}
触发实证: run=38382121618 evt=push sha=cf26e33f card_sha=4453c6cfc782
答件校验: sha256[:16]=37c7f669c74e50f2

# EXT-WAVE-11「赎」OBL-EXT10-a(B) 落地裁决

**总判定：CONDITIONAL**（(1)(3)(4) PASS；(2) 条件通过——分层披露合规但存在两处必须固化的口径收紧）

---

## (1) GAP 成立性 —— **PASS**

**G1（锚实编译、零 sorry）：** `library/ns/NsGallean/ZetaAnchor.lean` 四定理
- `critLine`、`zetaIsolationAnchor`、`zetaUniqueZeroAnchor`、`zetaAnchorImpliesRHCriticalLine`
构成可机检的「锚→RH 临界线」蕴含链。零 sorry 实编译满足「工件即证据」的最低门槛：G1 不要求锚为真，要求锚形式化且可复算。

**G2（探测 fail-closed）：** `ci/gap_probe_zeta.sh` 三项并列
- `riemannZeta_ne_zero_of_one_le_re` ABSENT
- Hardy Z 双缺席 ABSENT
- 对照 `riemannZeta` PRESENT
谓词层首实例 WELD-A-SPEC-01 的意义正在于此：**对照存在**证明探测不是恒 ABSENT 的空探针，VERDICT ABSENT=TRUE 是判定非噪声。

**G3'（缺口 vs 断言分离）：** Lean 锚仅断言「若锚成立则 RH 临界线」，探测仅断言「Mathlib 中该锚缺席」。二者拼合得到的是**缺口成立**，而非**RH 成立/不成立**。这正是 G3' 的形：证明「当前形式化基底无法闭合此链」，与证明数学命题真假解耦。

三条各自可独立复算，且互不越权——G1∧G2∧G3' 成立。

---

## (2) WIT-W1 分层记账 —— **CONDITIONAL**

分三证书逐条核：

**① zeta-iso-100：** 29 组 IVT 括号、端点包络异号不含 0 —— 存在性层 PASS 合规。Backlund 交叉门 fail-closed 拒证是**正确行为**：盒中心多边形未计张角余量，Σw=171.95 rad 对 232 盒、N_B∈[29.09812,29.09813] 无唯一整数，此时若强行取整即调参逼 PASS，触 P4。**降格 KI-EXT11-1 为数值演示级 + 挂号 OBL-EXT11-a 是本波最干净的动作。**

**② zeta-iso-1000：** 649 括号存在性 PASS，完备性 BLOCKED(B1) time-box 熔断——熔断本身合规（诚实优先于凑数），但需固化理由标签。

**③ psi-trunc：** 残差 ∈[−3365,3142]⊂±5.2e6 Dudek 形界 PASS；逐字披露「x>e⁶⁰ 适用范围外、点态管道演练、非定理实例」——这是**合规披露的范式**，应写回 WELD-A-SPEC-01 作为披露模板。

**证书逐字带「T=100/1000 有限高度」「区间见证层 PASS、kernel 层未证、非 RH 证据」——披露层合规。**

**CONDITIONAL 的两处收紧项（不构成 REJECT，但须落卡后方可结 OBL-EXT11-a）：**

1. **T 截断口径须区分「截断级」而非仅「截断值」。** 现卡并列 T=100/1000，但 ① 的完备性 BLOCKED 与 ② 的 BLOCKED(B1) 属**不同阻断类**（① 是数论-几何门槛未过，② 是 time-box 策略熔断）。二者若共用一个「BLOCKED」标签，未来复算会误并。**要求：BLOCKED 必须携带子码（B1=time-box / B2=几何余量 / …），否则 WIT-W1 分层在同一 BLOCKED 面上不可审计。**

2. **「区间见证层 PASS」与「存在性 PASS」的语义差须在证书头显式标注。** ① ② 的 PASS 均为**括号存在性**（IVT 层），不等于**括号数正确性**（Backlund 层）。现有披露已含「kernel 层未证」，但未点明「存在性 PASS ⊊ 计数 PASS」。要求：证书头部增加显式包含符号说明，防止下游把 29/649 误读为 N(T) 已定。

修正后 **PASS**；当前状态为 **CONDITIONAL**。

---

## (3) 定案卡勘误 —— **PASS**

ZETA-INST-01 卡原记「绕数=58=2×29」为**事实错误**。

理由：临界线在 s↦1−s̄ 反演下固定（CritLine 为反演不变集）。ρ 与 1−ρ̄ 在临界线上**重合**（当 Re ρ=1/2，1−ρ̄=1−(1/2−it)‾=1/2+it=ρ̄ 的共轭… 即在临界线上反演即共轭，落在同一对 {ρ,ρ̄}），矩形绕数不双计。**绕数=N(T)=29**。证书 deviation(4) 已录此点，勘误与原证书自洽。

无误报为「2×29」的残留路径——若下游有依赖 58 的中间量（如幅角累计），须一并回扫。**勘误成立，但要求附「下游 58 依赖回扫清单」以闭合。**

---

## (4) 枢线修补×12 + FINDING-20261013-01 重建 —— **PASS**

**核心判据：核判据是否被动。** 描述明确「hub 接管/覆写限测试驱动层，核判据未动」。

- 覆写权归属的实质是**核判据（criterion）的改写权**，而非**测试驱动层（test driver）的维护权**。测试驱动层属**执行脚手架**，其失效（hub 冲突/覆写）正是 FINDING-20261013-01 所捕获的故障类。由枢线接管并重建该层，属**修复职责**而非**主张权**。
- ×12 修补若触及任何**判据常量**（如 N_B 界、Dudek 界、T 截断阈值），即构成越权。现描述未列此类改动，且与 (2) 的 fail-closed 姿态一致（拒证而非改判据），**推定未触核判据**。

**PASS，但附一条追踪要求：** 重建后的 hub 接管须在 gap-registry 中留下「核判据未动」的**机器可验声明**（例如对 criterion 目录的哈希锁定），否则下一波复算无法独立确认「未动」是事实而非叙述。

---

## 汇总裁决

| 项 | 判定 | 关键理由 |
|---|---|---|
| (1) GAP | **PASS** | G1∧G2∧G3' 三支独立可复算，对照探针排除空探 |
| (2) WIT-W1 | **CONDITIONAL** | 分层披露合规；须补 BLOCKED 子码 + 存在性⊊计数显式标注 |
| (3) 勘误 | **PASS** | 反演不变→绕数 29，附下游 58 依赖回扫 |
| (4) 覆写权 | **PASS** | 测试驱动层非核判据；补机器可验「未动」声明 |

**无 REJECT。** 本波「赎」的实质是把 OBL-EXT10-a(B) 从未闭合的断言压力，转为可分级挂号的缺口账——这一点由 KI-EXT11-1 降格动作独立佐证，未触 P4。

**结案条件：** (2) 两处收紧项落卡、(3) 回扫清单、(4) 哈希声明三项齐备后，OBL-EXT11-a 可转 PASS 并归档 WELD-A-SPEC-01 首实例。

——lvlu SI1语义轨·20261013T101749Z
