# Normalization Report

## Summary

- input record 数: 2006
- normalized record 数: 2006
- merged rule 数: 255
- case_library 数: 15
- executable_rule 输入数: 144
- diagnostic_hypothesis 输入数: 113
- case_observation 输入数: 15
- irrelevant_noise 输入数: 1413
- comment-derived rule/candidate 数: 109
- minority_view 数: 108

## Rule Topic Distribution

- bidding_budget: 50
- ranking: 49
- keyword_research: 47
- campaign_structure: 41
- conversion_listing: 26
- data_diagnosis: 17
- traffic_allocation: 7
- product_targeting: 6
- seasonality: 6
- compliance_risk: 2
- launch: 2
- acos_profit: 2

## Rule Confidence Distribution

- medium: 232
- low: 23

## Noise Handling

- irrelevant_noise 未进入 merged_rules。
- comment_signal 仅作为弱信号保留在 normalized_records，不进入规则库。
- counterexample 进入 opposing_sources，不直接变成绝对规则。
- 不同 metric_threshold 以原文阈值保留，不强行折叠成固定阈值。
