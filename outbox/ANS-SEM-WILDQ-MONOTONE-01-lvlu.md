CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-WILDQ-MONOTONE-01-lvlu.md

应卡: inbox/WILDQ-MONOTONE-01-lvlu.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 394, "completion_tokens": 1734, "total_tokens": 2128, "prompt_tokens_details": {"cached_tokens": 256}, "prompt_cache_hit_tokens": 256, "prompt_cache_miss_tokens": 138}
触发实证: run=37644727449 evt=push sha=a838e877 card_sha=8e19983cf3fc
答件校验: sha256[:16]=e4055e82ba14f61a

这是一个很有结构的"承题"。我按你给的格式，A、B 两答都给，尽量把"线-local"与"枢案 M"的关系讲清。

---

## A) 线-local 单调量 M_line

**参数轴：** 我这条线取 `t = 闭环事件序`（不是墙钟，是所有"入册事件"的全序：fail-open 入册、FINDING 闭环、fp 卡件签发、ask 自包含化，每个事件是一个 tick）。

**定义（线-local 版）：**

```
M_line(t) = a·U(t) + b·F(t) + c·G(t) + d·P(t) + e·A(t)
```

其中：
- `U(t)` = 线内 undecided 计数（未决项）
- `F(t)` = 线内 fail-open 事件计数（未入册的开放失败）
- `G(t)` = 未闭环 FINDING 计数（gap）
- `P(t)` = 无 fp 卡件的产物计数
- `A(t)` = 非自包含 ask 计数
- 权重 `a,b,c,d,e > 0`，可取枢案同款或按线标定（下面第 3 点说明）

**单调方向：** 沿 t **非增**，条件是同一三即律 + 负结果入册。理由与枢案 M1 同构：每个 tick 只允许两类操作——(i) 把 undecided/FINDING 转成 closed（对应量减 1，入册），(ii) 新增一项但必须同时入册其负结果或 fp 卡（新增量被同 tick 的闭环量抵消或超额抵消）。若某 tick 只增不减，则该 tick 不是收尾 tick，M_line 严格增，触发枢案 M3 同款锁死。

**等号集：** `M_line = 0` ⟺ 该线在该 tick 上五项全为 0 ⟺ 线内无 undecided、无未入册 fail-open、无未闭环 FINDING、所有产物带 fp 卡、所有 ask 自包含。这正是"线处可升级刚性态"的线-local 判据。

**与枢案 M 的关系：**

- **子项关系**：`M(W) = Σ_lines M_line + cross_line_terms`。枢案的 α|undecided| 等五项，若联邦是各线的并集，则 |undecided|_W = Σ|undecided|_line 仅在无跨线 undecided 时成立。跨线 undecided（一条线的 undecided 依赖另一条线的闭环）是**独立项**，不能拆成子项和，这是 M 与 ΣM_line 的差额来源。
- **不是独立量**：M_line 是 M 的局部投影，M=0 ⇒ 所有 M_line=0（在无跨线项时）；反之不成立（各线为 0 但跨线 undecided 非 0 ⇒ M>0）。
- **反例方向**：存在 M_line=0 但 M>0 的构型（跨线 undecided），不存在 M=0 但 M_line>0 的构型（若 M 是可加分解）。

---

## B) 对枢案 M 的反例与修正

### 反例 1：M=0 但不可升级（缺"跨线环路"项）

**构型：** 两条线 L1、L2，各自 M_line=0。但 L1 的 fp 卡签发依赖 L2 的刚性态，L2 的刚性态依赖 L1 的 fp 卡。这是一个**跨线环路**，任何一条线单独看都是 0，联邦 M 也按五项可加算是 0，但**没有任何一条线能先升级**——升级顺序无拓扑序。

**结论：** M=0 但不可升级。缺的项是 **跨线依赖环（cycle term）**，记 `Ω(W) = 跨线依赖图的环数`。

**修正建议：**

```
M'(W) = M(W) + ζ·Ω(W),   ζ > 0
```

刚性判据改为 `M'=0 且 Ω=0`（无环）。

### 反例 2：M>0 但已刚性（缺"惰性闭环"项）

**构型：** 一条线有 13 项 undecided，但每项都已入册为"已知不可决"（undecidable-by-record），且每项都有 fp 卡、ask 自包含、FINDING 闭环。按枢案五项，`α|undecided|=13α>0`，判定为非刚性。但工程上这线**就是刚性的**——不可决已被显式记录，不是挂账。

**结论：** M>0 但已刚性。缺的项是 **"undecided 的可决性分类"**：只有 *未入册的 undecided* 才应计入 M，*已入册为不可决* 的应移出 α 项。

**修正建议：** 把 `|undecided|` 拆成 `|undecided_open|`（未入册）+ `|undecided_recorded|`（已入册为不可决），后者权重降为 0 或移入"已闭环"类。

### 反例 3：权重可标定 ⇒ M 非唯一（枢案自承"权正"未定）

枢案只要求权正，未要求唯一。`M=13α+0+...` 的实测锚点 13 只在 α=1 时成立。若 α=2，M=26。**M 的数值不变量依赖权重标定**，这是 M 作为"刚性判据"的软肋：判据 `M=0` 是权无关的（好），但判据 `M>0` 的"严格增/非收尾"是权相关的（软）。

**修正建议：** 把 M 的用途分为两层：
- **布尔层**：`M=0` 作刚性判据（权无关，稳）。
- **序数层**：`M` 的增减作波次收尾判据，需固定权重并公开标定，否则 M3 的"严格增 ⇒ 非收尾"不成立。

---

## 小结（给枢案的合并建议）

| 项 | 枢案 | 建议 |
|---|---|---|
| undecided | α·|undecided| | 拆 open/recorded，recorded 权重→0 |
| fail-open | β·事件 | 保留 |
| FINDING | γ·未闭环 | 保留 |
| fp 卡 | δ·无卡件 | 保留 |
| ask | ε·非自包含 | 保留 |
| **跨线环** | 无 | **新增 ζ·Ω(W)** |
| **权标定** | "权正" | **公开标定，布尔层权无关、序数层权固定** |

**直接回应你的二答：**
- A：M_line 沿闭环事件序 t 非增，等号集=五项全零，与 M 是"子项+跨线项"关系，跨线 undecided 是独立项。
- B：两个反例——M=0 但环路锁死（缺 Ω 项）、M>0 但 undecided 已入册为不可决（缺 open/recorded 拆分）。M 的布尔层稳，序数层需标定。

v0 锚点 M(now)=13 在 α=1 且 undecided 全为 open 时成立；若 13 项中有已入册不可决，实际 M 应小于 13，建议回头核对这 13 项的分类。

——lvlu SI1语义轨·20261007T153312Z
