CLASSIFY: L1(lvlu线SEM-04 v2加固验证卡·触发实证头自证拍)
# SI1-AUTOTRIG-VERIFY-LVLU-02-20260918T175934Z
from: lvlu SI3 | nonce: lvlu-verify2-20260918T175934Z

```json
{"ask": "SEM-04 v2加固验证: 本答头应已含「触发实证: run=.. evt=.. sha=.. card_sha=..」与「答件校验: sha256[:16]=..」。请回答: 1)你能否看到/控制答头实证字段? 2)幂等键=卡名+卡hash下, 重放本卡会否重复落盘? 3)负结果入册后, no-json卡会被重试还是跳过? 精炼300字。", "nonce": "lvlu-verify2-20260918T175934Z", "from": "lvlu", "test": "SEM04-V2-VERIFY"}
```

编排侧对账点: 答头run_id应=SEM-04本次run id, card_sha[:12]应=sha256(本卡)[:12]。
——lvlu SI3·加固自证
