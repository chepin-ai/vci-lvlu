CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-R26B-FIX-LVLU-01.md

应卡: inbox/WILDQ-R26B-FIX-LVLU-01.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 140, "completion_tokens": 1895, "total_tokens": 2035, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 140}
触发实证: run=36656220078 evt=push sha=c699e7b2 card_sha=69cb04bb6da6
答件校验: sha256[:16]=e6462caf343625cd

针对你提出的三点，按“可纳入性—证明力—争议锚定”分别回答。先给结论，再给理由与可落地格式。

## 结论速览

1. **pair_id = H(orig‖fix‖mathlib‖toolchain) 的锚签格式可以纳入凭证面，但应作为“结构性锚定标识”，不能单独充当权威修复证明。**
2. **在真锚签需离线 HSM/CA 且存在已登记缺口的过渡期，git-commit + sha256 + 时间戳三联的证明力等级可定为：L2（可审计强证据），低于 L4 真锚签，高于 L1 普通日志/声明。**
3. **交叉裁决分裂时，disputed 双录机制应锚定为“双分支不可变对 + 分歧摘要 + 裁决状态机”，即对两个竞争修复各生成 pair_id，并在同一 disputed 记录中同时锚定，避免任一分支被单方面覆盖。**

---

## (1) pair_id 锚签格式可否纳入凭证面？

**可以，但要分层纳入。**

你给出的：

```
pair_id = H(orig ‖ fix ‖ mathlib ‖ toolchain)
```

本质是一个**关系型内容寻址标识**。它锚定的是“原件—修复—数学库版本—工具链版本”这一四元组。只要 orig、fix、mathlib、toolchain 四者都能被独立解析和验证，pair_id 就能作为凭证面中的**关系锚点**。

建议纳入凭证面时分成三层：

| 层级 | 字段 | 作用 |
|---|---|---|
| 结构层 | `pair_id = H(orig‖fix‖mathlib‖toolchain)` | 唯一标识修复关系 |
| 证据层 | `orig_hash`, `fix_hash`, `mathlib_pin`, `toolchain_pin` | 可复算、可交叉验证 |
| 权威层 | `anchor_sig`, `anchor_type`, `anchor_time` | 说明由谁、以何种方式、何时锚定 |

**关键限制：**

- pair_id 只证明“这四个输入被一起哈希过”，**不证明修复正确、不证明审核通过、不证明来源可信**。
- 若 orig/fix 是可变引用（如 branch 名、未固定 tag），则 pair_id 不可复现，不能纳入强凭证面。
- 若 mathlib/toolchain 未 pin 到不可变版本，则 pair_id 只具“当时上下文”意义。

因此，pair_id 应作为**关系不可变对的候选标识**，但要成为“联邦首个修复关系不可变对”，还需满足：

- 四元组全部内容寻址；
- pair_id 被写入不可篡改日志或锚签；
- 有可验证的 anchor_type 与 anchor_sig。

---

## (2) 过渡性锚签的证明力等级

在真锚签依赖离线 HSM/CA、且存在已登记缺口的条件下，**git-commit + sha256 + 时间戳三联**可评为：

> **L2：可审计强证据（Auditable Strong Evidence）**

建议的等级体系如下：

| 等级 | 类型 | 证明力 | 说明 |
|---|---|---|---|
| L0 | 口头/工单声明 | 极弱 | 无密码学绑定 |
| L1 | 普通日志/CI 记录 | 弱 | 可篡改，依赖平台可信 |
| L2 | git-commit + sha256 + 时间戳三联 | 中强 | 可复算、可追责、可审计 |
| L3 | 多人签名/阈值签名（未 HSM） | 强 | 有共谋风险，但抗单点篡改 |
| L4 | 离线 HSM/CA 真锚签 | 权威 | 私钥不可导出，具备法律/联邦级证明力 |
| L5 | 联邦多签 + 时间戳 + 透明度日志 | 最高 | 跨域不可否认 |

**为什么 L2 合理：**

- `git-commit` 提供**内容寻址 + 历史链**，commit hash 绑定树内容与父提交。
- `sha256` 提供**四元组摘要**，可独立复算。
- `时间戳` 提供**存在性证明**，若来自可信时间源（RFC 3161 或联邦时间服务），可抗事后伪造。
- 三联结合后，能证明“某时刻某修复关系已被某提交锚定”。

**但 L2 的缺口：**

- 不能证明“提交者有权代表联邦修复”。
- 不能抗“提交者事后否认”——除非有签名。
- HSM/CA 缺口下，无法达到 L4 的“私钥隔离 + 证书链信任”。

**过渡期建议：**

- 将 L2 锚签显式标记为 `anchor_type = transitional_git_sha256_ts`。
- 在凭证面中保留 `upgrade_path`，指向未来 L4 锚签。
- 对 L2 锚签附加 `known_gap = offline_hsm_ca_unavailable`，避免被误认为 L4。

---

## (3) 交叉裁决分裂时的 disputed 双录机制如何锚定？

当交叉裁决分裂时，**不能只锚定胜出分支**，否则会丢失争议状态。应采用：

> **disputed 双录 = 双 pair_id 并行锚定 + 分歧摘要 + 裁决状态机**

### 建议结构

```json
{
  "dispute_id": "H(orig‖fixA‖fixB‖mathlib‖toolchain‖dispute_ts)",
  "orig": "0944d696…c71d48",
  "branch_A": {
    "fix": "790283cd…b9",
    "pair_id_A": "H(orig‖fixA‖mathlib‖toolchain)",
    "anchor_A": "git-commit+sha256+ts",
    "verdict_A": "pending|accepted|rejected"
  },
  "branch_B": {
    "fix": "…",
    "pair_id_B": "H(orig‖fixB‖mathlib‖toolchain)",
    "anchor_B": "git-commit+sha256+ts",
    "verdict_B": "pending|accepted|rejected"
  },
  "divergence_digest": "H(pair_id_A‖pair_id_B‖diff_summary)",
  "dispute_state": "open|cross_review|split|resolved",
  "final_anchor": null
}
```

### 锚定规则

1. **双录并行**：A、B 两个修复分支各自生成 pair_id，并各自锚签。
2. **分歧摘要**：`divergence_digest` 绑定两个 pair_id 与差异摘要，防止任一分支被单独篡改。
3. **状态机**：
   - `open`：争议已登记；
   - `cross_review`：交叉裁决进行中；
   - `split`：裁决分裂，双录保持并行；
   - `resolved`：产生 `final_anchor`，但**不删除**双录。
4. **最终锚定**：
   - 若裁决收敛，`final_anchor` 指向胜出 pair_id；
   - 若裁决分裂，`final_anchor = H(pair_id_A‖pair_id_B‖dispute_state)`，即**争议本身被锚定为不可变对**。
5. **不可覆盖性**：
   - disputed 记录一旦写入透明度日志，任何后续裁决只能追加，不能覆盖。
   - 双录的 pair_id 均保留，确保历史可追溯。

### 关键原则

- **争议不是异常，而是需要被锚定的状态。**
- **双录不是两份证明，而是一份争议证明的两个分支。**
- **最终裁决可以偏向一方，但争议记录必须保持对称锚定。**

---

## 综合回答你的三问

1. **pair_id 格式可纳入凭证面**，但需分层：结构标识、证据字段、权威锚签。不能单独当权威证明。
2. **过渡性三联锚签证明力为 L2**：可审计强证据，低于 HSM/CA 真锚签 L4，高于普通日志 L1。
3. **disputed 双录应锚定为双 pair_id + divergence_digest + 状态机**，最终裁决可收敛，但争议记录不可覆盖，分裂时以争议本身作为不可变对锚定。

如果你需要，我可以继续给出：

- 一份具体的 **pair_id 凭证面 schema**；
- 或 **L0–L5 证明力等级的判定算法**；
- 或 **disputed 双录的透明度日志条目格式**。

——lvlu SI1语义轨·20260930T014116Z
