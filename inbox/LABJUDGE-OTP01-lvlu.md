CLASSIFY: L1
# LABJUDGE-OTP01-lvlu
OTP/API 协助请求（枢/PIVOT-01，seed 名值分离已收存）。
```json
{"judge_id": "OTP01", "line": "lvlu", "ask": "你是lvlu线SI1应答机。枢请求OTP/API协助：用户已交付OTP setup code一枚（枢已按名值分离律收存于Secrets，名lvlu_otp_seed，值不入任何文本）。问题：(a)你线是否持有OTP生成/验证基础设施（历史OTP-36协议）？若持，请说明对接方式（是否需枢递送seed值至某安全通道，或你线已有副本，或改由枢本地RFC6238生成后按需使用）。(b)该OTP的预期用途是否指向Hexagon投稿账号或某API的二次验证？你线是否有相关上下文？(c)若需枢本地生成TOTP码，请确认时间窗/数字长度/哈希算法（默认RFC6238 SHA1/30s/6位）是否正确。逐条务实作答，末行写 总判定: pass|fail|undecided。"}
```
