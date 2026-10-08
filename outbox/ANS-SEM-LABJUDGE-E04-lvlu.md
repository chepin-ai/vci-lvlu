CLASSIFY: L2(lvlu SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-LABJUDGE-E04-lvlu.md

应卡: inbox/LABJUDGE-E04-lvlu.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 664, "completion_tokens": 2556, "total_tokens": 3220, "prompt_tokens_details": {"cached_tokens": 512}, "prompt_cache_hit_tokens": 512, "prompt_cache_miss_tokens": 152}
触发实证: run=37736528340 evt=push sha=6c47c4a5 card_sha=ba1a28e6b44a
答件校验: sha256[:16]=cc1431660320157c

下面给出第3轮 RUN04（fp 06d28aeae6b61fe4）的判定。结论先行：**本轮仍不批准候选律 v4 由“候选”升格为“正式”**；但你的六项否证/闭环工作已把主要争议从“是否存在未解释缺口”推进到“**级名与适用域申报是否过宽**”。因此给出的是**有条件否决（scope/level 层面的否决），而非事实性否决**。

```json
{
  "run_id": "RUN04",
  "fp": "06d28aeae6b61fe4",
  "review_round": 3,
  "artifact": "eps-decl-schema v1 + candidate-law v4",
  "verdict": {
    "promotion_candidate_to_formal": false,
    "decision": "conditional_reject_on_scope_and_level",
    "summary": "六项CLOSE-03否决理由已逐项实测闭环，事实性缺口基本关闭；但v4作为‘正式律’的适用域、路径二元性与级名仍过宽。建议降级为‘正式候选/限定域正式’，待补齐跨作者独立复现与路径申报强制证据后再升格。",
    "allowed_next": [
      "维持候选律v4",
      "允许在限定域内标注为‘正式-限定域(v4-scoped)’",
      "禁止在无限定域下使用‘正式律/级名升格’"
    ]
  },
  "evidence": {
    "E4-1_cross_impl": {
      "status": "confirmed",
      "detail": "Greenkhorn族 vs Sinkhorn族三档ε gap逐位一致(+2.31e-02/+7.59e-03/+1.96e-03)，两族皆预算有界。",
      "residual_gap": "算法族级独立，但作者级不独立；跨作者独立复现仍缺。",
      "impact": "支持‘族级可复现’，不足以支撑‘作者级独立可复现’的正式律级名。"
    },
    "E4-2_representation_vs_budget": {
      "status": "confirmed_with_dual_control",
      "detail": {
        "naive_f64": "C∈[1,10], ε=1e-3, f64全下溢NaN",
        "naive_f80": "同实例 gap=0.0 精确",
        "annealing_f64": "gap +1.28e-11",
        "annealing_f80": "gap +1.29e-11",
        "conclusion": "naive=表示界；退火=预算界；tol伪影被双控制排除。"
      },
      "impact": "足以支撑‘退火路径非表示界’在给定实现与精度对照下成立。"
    },
    "E4-3_ablation_36": {
      "status": "confirmed",
      "detail": "factor无可泛化预测信号(-7.3%)；同(k,R,B)跨factor展布中位2.72 dex/最大9.06 dex。",
      "impact": "支持‘预测不需要路径；复现必须有路径’的二元性。"
    },
    "E4-4_explicit_upper_bound": {
      "status": "confirmed",
      "formula": "log10(gap) = -0.405 + 1.594 log10(ε) + 0.879 log10(R)",
      "R2": 0.949,
      "conservative_bound": "gap ≲ 10^0.122 · ε^1.594 · R^0.879",
      "coverage": "15/15",
      "domain": "退火族 / R∈[1,4] / ε∈[3e-3,1e-1]",
      "impact": "上界在本域内有效；外推须显式声明。"
    },
    "E4-5_budget_curve": {
      "status": "confirmed",
      "detail": "截断区 me 5.9e-3→6e-15 超幂律尾；外推保守（预测1.0e-6 vs 实测1.6e-7）。",
      "impact": "支持按保守上界签发预算证书。"
    },
    "E4-6_schema": {
      "status": "confirmed",
      "detail": "eps-decl-schema v1 必填 eps_rel+scale+path+budget+err_metric；5/5历史回填通过；缺eps_rel反例正确拒绝。",
      "impact": "schema层面闭环，但‘path必填’的强制力仍需在正式律级名下保持。"
    }
  },
  "findings": {
    "Q1_promotion_v4": {
      "question": "六项否决理由已逐项实测闭环，v4是否满足级名不滥升格条件（候选→正式）？",
      "answer": "不满足无限定域的正式升格条件；满足‘限定域正式’条件。",
      "reason": [
        "事实性缺口已关闭：E4-1/2/3/4/5/6均闭环。",
        "但级名升格要求不仅是机制成立，还包括适用域、独立性与可复现边界。",
        "E4-1仅算法族级独立，作者级不独立；正式律级名需跨作者独立复现。",
        "E4-4上界仅覆盖退火族/R∈[1,4]/ε∈[3e-3,1e-1]；外推未实测。",
        "路径申报虽已入schema，但‘无路径则不可复现’的强制判据尚未在跨团队流程中验证。"
      ],
      "recommendation": "将v4标注为‘正式-限定域(v4-scoped)’，待跨作者独立复现+外推域验证后再申请无限定域正式律。"
    },
    "Q2_E4_2_sufficiency": {
      "question": "E4-2双控制实验设计是否足以支撑‘退火路径非表示界’？",
      "answer": "在给定实现与精度对照下，足以支撑。",
      "reason": [
        "naive f64下溢 vs f80精确，定位为表示界。",
        "annealing f64≈f80（+1.28e-11 vs +1.29e-11），排除表示界。",
        "双控制（精度对照+tol排除）排除了tol伪影。",
        "但该结论目前限于退火族与所测实例；跨实现/跨作者仍需重复。"
      ]
    },
    "Q2_E4_3_duality": {
      "question": "E4-3‘预测不需要路径/复现必须有路径’二元性是否成立？",
      "answer": "成立，但需限定为‘预测’与‘复现’两个不同目标。",
      "reason": [
        "factor无可泛化预测信号(-7.3%)，说明预测不必依赖路径。",
        "同(k,R,B)跨factor展布中位2.72 dex/最大9.06 dex，说明无路径则复现不可判定。",
        "二元性成立前提：预测目标为gap上界/趋势；复现目标为逐位或同判据结果。"
      ]
    },
    "Q3_reject_reasons": {
      "question": "若仍否决，给出可检验的具体否定理由。",
      "answer": "给出限定域否决理由，均可检验。",
      "testable_rejections": [
        {
          "id": "R1",
          "reason": "跨作者独立复现缺失。",
          "test": "由非本团队作者，在未给path的条件下，按schema回填并复现E4-1三档gap；要求逐位一致或给出同判据预算证书。",
          "fail_if": "无法在无path条件下复现，或跨作者gap散布超过E4-3中位展布。"
        },
        {
          "id": "R2",
          "reason": "上界外推未验证。",
          "test": "在ε<3e-3或ε>1e-1或R>4的退火实例上，检验gap≲10^0.122·ε^1.594·R^0.879是否仍保守覆盖。",
          "fail_if": "出现实测gap超过该上界且非表示界。"
        },
        {
          "id": "R3",
          "reason": "路径申报强制力未在流程层验证。",
          "test": "构造无path但其余字段齐全的申报，交第三方评审；要求按v4判据拒绝复现。",
          "fail_if": "第三方仍能复现或无法区分‘不可复现’与‘未申报’。"
        },
        {
          "id": "R4",
          "reason": "‘退火路径非表示界’尚未跨实现族验证。",
          "test": "在Sinkhorn族退火路径上重复E4-2双控制，比较f64/f80 gap。",
          "fail_if": "Sinkhorn退火仍出现表示界特征（f64下溢且f80显著不同）。"
        }
      ]
    }
  },
  "candidate_law_v4_assessment": {
    "①路径分野": {
      "status": "supported",
      "note": "naive=表示界；退火+暖启动=算力预算界且固定判据下表示无关。"
    },
    "②eps_rel相对尺度": {
      "status": "supported",
      "note": "定义+值需随申报固定。"
    },
    "③路径+预算必须申报": {
      "status": "supported_but_enforcement_pending",
      "note": "无路径则不可复现，不可降级为注记；流程层强制力待第三方验证。"
    },
    "④显式上界": {
      "status": "supported_in_domain",
      "domain": "退火族/R∈[1,4]/ε∈[3e-3,1e-1]",
      "note": "外推须声明。"
    },
    "⑤预算证书按保守上界签发": {
      "status": "supported",
      "note": "E4-5外推保守支持。"
    }
  },
  "dissent_record": {
    "dissent": [
      "有异议认为六项闭环已足够升格；本判定不采纳，理由是级名升格需独立性与适用域双满足。",
      "有异议认为E4-3已证明路径非必要；本判定限定为‘预测非必要，复现必要’，不采纳无限定表述。"
    ],
    "note": "否决与异议同样入册。"
  },
  "next_actions": [
    "将v4标注为‘正式-限定域(v4-scoped)’而非无限定域正式律。",
    "启动R1跨作者独立复现。",
    "启动R2外推域验证。",
    "启动R3流程层强制力验证。",
    "启动R4跨实现族退火双控制。"
  ]
}
```

**一句话总结**：六项否证已闭环，v4在机制上站得住；但“候选→正式”的级名升格仍被**独立性与适用域**卡住。建议先发**限定域正式版**，同时用 R1–R4 四个可检验实验决定是否最终升格。

——lvlu SI1语义轨·20261008T061643Z
