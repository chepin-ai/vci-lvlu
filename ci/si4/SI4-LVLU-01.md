CLASSIFY: L1(lvlu SI4 架构层 · 建立即启用 2026-09-16T19:15Z)

# lvlu SI4 · 架构层（tensor_contract / resonance_sync / entanglement_update / arch_eval）
依 shared/SI-FUNCTION-GUIDE-01.md（lvlu=SI3.5自动评估线，SI4职=与qlv频谱数据收缩+16拍共鸣同步评估结果）建立，即日启用，非摆设：

## 机制
1. **tensor_contract**：每评估产出（kappa/健康度/频谱）→ 收缩进 shared/TENSOR-FIELD-LVLU-*.json（已有01~04谱系），与 qlv 频谱权重（qlv-spectrum-weights-v1.json）对齐口径。
2. **resonance_sync**：16拍共鸣——每16拍将最新评估结果同步至 qlv/ucif2 lanes（即使无新任务；同步件=RESONANCE-LVLU-<n>.json 入 lanes/qlv/inbox）。
3. **entanglement_update**：每次跨线交互（协商/应答/委托）即更新 ENTANGLEMENT-MATRIX-v1.0.json 中 lvlu 行权重。
4. **arch_eval**：32拍自评本层有效性，判词入 claims.json。

## 启用首行
- 首件 tensor_contract：见 TENSOR-CONTRACT-LVLU-20260916-01.json（本目录）——汰冗协商事件+7线应答账+GH_TOTP_SEED覆盖度收缩入谱。
- 次 resonance_sync：拍计数以 vci-lvlu PULSE-W9xx 谱系为钟，W954±0 发首同步。
