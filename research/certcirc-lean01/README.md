CLASSIFY: L1
# CERT-CIRC-LEAN-01 · 环状 Sinkhorn 不动点唯一性的 leancert 移植包

联邦内核锚 CERT-CIRC-01 的 Lean 化身（OBL-EXT-01 里程碑 M1.2 备稿）。

## 内容
- `CertCircLean01.lean`：11 维 gauged 环状 Sinkhorn 不动点系统（G = e^F − 1 无对数形）+ Krawczyk 证书 + 唯一性主定理 `circ_unique_root`。
- 参数：k=6，c=[1/2,1/3,2/3,1/4,3/4,1/5]（显式有理），ε=1，均匀边际，f₀ pinned。
- 闭形式：f*=0，g*=-(log 6 + lse(-c))=-3.154369860822252…；有理中心 ĝ₂=-593406054287/188121900877（对 g* 浮点精确）；盒半径 1/10⁹。

## 重大诚实修正（2026-11-01 / 2026-11-03 现场勘误，原结论不抹除）
1. **log→exp 重构**：leancert v4.34.1 `Expr.checkADSupported` 不支持 log/inv/atan，初版系统 22 处 `Expr.log` 使 `krawczykCheck` 第一合取项必为假（native_decide 实测判 false）。改用同零点集变换 G = e^F − 1（e^x=1 ⟺ x=0；根处 J_G = e^F·J_F = J_F，Krawczyk 收敛性质不变）。
2. **中心修正**：初版中心 ĝ=-7657889656187/5620014131279=-lse(-c)=-1.3626… 漏掉 log 6 项；真解 g*=-3.154369860822252…。初版 box 内无根，本 README 旧称「K 宽度 2.04e-14、负面控制拒收」**不复现，特此勘误**。
3. **预条件子 Q 块指标翻转**：旧配方 Q[j][k]=6·exp(ĝ−c[(k−j)%6]) 方向错误；正确 ∂Ggⱼ/∂fᵢ=6·exp(fᵢ+gⱼ−c[(j−i)%6])，根处 J_G=[[I₅,P],[Pᵀ,I₆]] 对称（Sinkhorn Hessian 结构）。旧验证系预条件子与区间 Jacobian 同错自洽的关联误差盲区；由「从 .lean 文件 Expr 语义独立重推 Jacobian」的正交复验暴露。带错预条件子 q=0.0715 仍 <1 可过检，但不予接受。
4. **仪器失校注记**（判据失校即修律）：负面控制初版仅移中心，因 Krawczyk 像对中心一阶不变而未拒；已修为中心+box 同移，判据恢复鉴别力。

## 本地复验（Python 区间算术，外向舍入，对修正后证书）
- 收缩因子 ‖I − A·J(box)‖_sup = 4.5621280e-08 < 1（裕度 7 个数量级）。
- Krawczyk 像最大宽度 9.12e-17，11 维全严格内包。
- det(A) = 6.2482… ≠ 0（有理精确 Bareiss 复核一致）。
- 负面控制（中心+box 同移 1e-6）→ 内包失败（拒收）✓。
- G 在闭形式根处残差 1.24e-16。

## 验证路径
1. 本地：`lake update && lake build LeanCert.Validity.Krawczyk && lake env lean CertCirc/CertCircLean01.lean`（需网络拉取 mathlib/leancert 缓存）。
2. 云端：Axle 自定义环境（公共层仅 batteries/Qq/Mathlib，已实测不含 LeanCert——2026-10-09 探针记录）。
3. 信任口径：native_decide（默认）或 `leancert (trust := kernel)` 纯内核路线。
4. 版本注记：lakefile 锁 tag v4.34.1 → 实际解析 commit a5777840d9e69994c79a99879881c93e2bd0e6f6（与本包旧稿所称 7f91b6eb35 不一致，已向 wave 线挂异）。

## 状态
**Lean 端编译验证通过（2026-11-03T17:16Z）**：`lake env lean CertCirc/CertCircLean01.lean` → EXIT=0，
主定理 `circ_unique_root : ∃! p, FinBoxMem p circBox ∧ SystemZero circSystem p` 全证成立。
证据：COMPILE-PASS.json（sha256 b90e245a…4032b2，33563 B，toolchain v4.34.1，cfg taylorDepth=30）。
五合取项分治：AD支持/中心在盒/收缩界/严格内包 四项 native_decide 直算通过；det≠0 由精确有理逆
见证经 `Units.mk + Matrix.isUnit_iff_isUnit_det` 提升（规避 11! 排列枚举的 8GB 内存墙，探针实测
identity-free 判为 OOM 源，11!×~200B ≈ 8GB > 3GiB 沙箱顶）。
Python 正交复验（外向舍入区间算术，独立重推 Jacobian）：q=4.10e-06<1，K 最大宽度 8.20e-15 严格内包，
det=6.248≠0，负面控制拒收。
