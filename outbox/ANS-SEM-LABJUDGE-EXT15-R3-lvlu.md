CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-EXT15-R3-lvlu.md

应卡: inbox/LABJUDGE-EXT15-R3-lvlu.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 718, "completion_tokens": 680, "total_tokens": 1398, "prompt_tokens_details": {"cached_tokens": 512}, "prompt_cache_hit_tokens": 512, "prompt_cache_miss_tokens": 206}
触发实证: run=38523732646 evt=push sha=451164e1 card_sha=45ae270b396e
答件校验: sha256[:16]=22916b288be247de

PASS

**判定依据（要点）**

- **OBL-EXT11-a（Backlund 门严格化）目标已闭合**：证书 `zeta-iso-100 v1.1.1` 给出唯一整数窗判定所需的严格区间，`N_B ∈ [28.9999999999999999958558652436, 29.000000000000000004418444223]`，宽 `8.56258e-18`，`ceil(lo)=floor(hi)=29`，且 `completeness.backlund` 包含 qfa 修订项③要求的 `nB_interval / width_budget / branch_exclusion_28_30`，未见缺字段。
- **fail-closed 门禁已落实**：`#18/#19` 对 `backlund_cert_nB_interval_match` 与 `width_budget_match` 做双查，缺字段即拒证；`gen` 同款复算并带诚实门；`test` 第45项覆盖该字段族。此路径与“修订项③”逐字对应。
- **SUP-01 独立复算支持**：769 结点均匀网格复算落入同区间；232 段张角 `max 0.876 < π`，余量 `≥2.265`；锚点辐角宽 `3.77e-153`。为区间见证提供非单点、非偶然的网格证据。
- **SUP-02 独立腿与预算闭包满足修订项①②**：EM 独立腿（N=1000, dps=80）独立输出 `N_B ∈ [28.9999999999999999877574324241, 29.0000000000000000124773520971]`，宽 `2.47e-17`，唯一 29，且与 CVZ 区间相交。宽度预算 `w_NB=(w_θ+w_Δarg+w_wrap)/π=(2.69001e-17+8.96721e-84+0)/π=8.56258e-18` 与证书逐项相等；共享假设仅 θ 解析余项 + iv 内核，已申报。
- **可重复性与全链路一致性**：`resign_v111` 双跑字节一致；`gen --emit-raw` 全量与三证逐字节相同；`pytest 45/45`（3338.17s）。这表明证据包在给定提交 `d8a046f20020d47c2d48479ba60651040a68a7a4` 下可复核、可重放。
- **纪律边界未被越界**：有限高度 `T=100/1000` 截断；区间见证层 PASS、kernel 层未证；非 RH 证据；隔离区间内区间见证 PASS、非全域声明。以上均与“有限高度 + 区间见证 + 非 RH”纪律一致，故不构成 REVISE 缺口。

**结论**：EXT15-R3 终投满足 PASS。OBL-EXT11-a 关闭；Backlund 门严格化判定为 PASS。

——lvlu SI1语义轨·20261014T064233Z
