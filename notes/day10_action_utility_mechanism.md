# Action-utility mechanism audit

For a candidate a, U(a)=L(real,before)-L(a,before)+[L(a,before)-L(a,after)]. The common baseline cancels for fresh versus reuse; initial prediction changes and one-step learning are distinct contributions. All same-state windows are dependent development observations.

## Original BANKING spawn windows

| step | segment | initial_loss_gap | learning_gain_difference | fresh_advantage | initial_gap_share |
| --- | --- | --- | --- | --- | --- |
| 18 | B1 | 0.3468 | 0.0499 | 0.3967 | 0.8743 |
| 50 | C1 | 0.4311 | 0.0612 | 0.4923 | 0.8756 |

The initial gap includes changing the complete classifier-and-LoRA package; it is not a pure classifier effect. The matched component factorial audit separately identifies substantial classifier-head effects.

## Same-state eligibility comparison

| run | windows | eligibility_changes | reuse_ranking_changes |
| --- | --- | --- | --- |
| day5_amazon_private_cau_seed2026 | 75 | 0 | 0 |
| day5_banking_private_cau_seed2026 | 70 | 0 | 0 |
| day6_amazon_private_cau_seed2027_b_first | 73 | 1 | 0 |
| day6_amazon_private_cau_seed2027_canonical | 68 | 3 | 0 |
| day6_amazon_private_cau_seed2028_b_first | 65 | 1 | 0 |
| day6_amazon_private_cau_seed2028_canonical | 53 | 2 | 0 |
| day6_amazon_private_cau_seed2029_b_first | 76 | 2 | 0 |
| day6_amazon_private_cau_seed2029_canonical | 67 | 1 | 0 |
| day6_amazon_private_cau_seed2030_b_first | 73 | 0 | 0 |
| day6_amazon_private_cau_seed2030_canonical | 49 | 2 | 0 |
| day6_amazon_private_cau_seed2031_b_first | 47 | 0 | 0 |
| day6_amazon_private_cau_seed2031_canonical | 70 | 0 | 0 |
| day6_banking_private_cau_seed2027_b_first | 70 | 0 | 0 |
| day6_banking_private_cau_seed2027_canonical | 70 | 0 | 0 |
| day6_banking_private_cau_seed2028_b_first | 70 | 0 | 0 |
| day6_banking_private_cau_seed2028_canonical | 70 | 0 | 0 |
| day6_banking_private_cau_seed2029_b_first | 70 | 0 | 0 |
| day6_banking_private_cau_seed2029_canonical | 70 | 0 | 0 |
| day6_banking_private_cau_seed2030_b_first | 70 | 0 | 0 |
| day6_banking_private_cau_seed2030_canonical | 70 | 0 | 0 |
| day6_banking_private_cau_seed2031_b_first | 70 | 0 | 0 |
| day6_banking_private_cau_seed2031_canonical | 70 | 0 | 0 |

These disagreement counts rescore the same reference states. They are not a closed-loop ablation or independent-window significance test.

## Closed-loop scoring pilot

| regime | architecture | seed | rule | initial_loss_accuracy | post_update_accuracy | allocation_disagreements | updates | adapters | spawns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | head_only | 2026 | frozen_centroid | 0.8255 | 0.8255 | 0 | 80 | 1 | [] |
| amazon | head_only | 2026 | last_active | 0.8255 | 0.8255 | 0 | 80 | 1 | [] |
| amazon | head_only | 2026 | uniform_probability | 0.8255 | 0.8255 | 0 | 80 | 1 | [] |
| amazon | head_only | 2027 | frozen_centroid | 0.7943 | 0.7943 | 0 | 80 | 1 | [] |
| amazon | head_only | 2027 | last_active | 0.7943 | 0.7943 | 0 | 80 | 1 | [] |
| amazon | head_only | 2027 | uniform_probability | 0.7943 | 0.7943 | 0 | 80 | 1 | [] |
| amazon | private | 2026 | frozen_centroid | 0.8542 | 0.8542 | 0 | 79 | 1 | [] |
| amazon | private | 2026 | last_active | 0.8542 | 0.8542 | 0 | 79 | 1 | [] |
| amazon | private | 2026 | uniform_probability | 0.8542 | 0.8542 | 0 | 79 | 1 | [] |
| amazon | private | 2027 | frozen_centroid | 0.8516 | 0.8516 | 0 | 72 | 1 | [] |
| amazon | private | 2027 | last_active | 0.8516 | 0.8516 | 0 | 72 | 1 | [] |
| amazon | private | 2027 | uniform_probability | 0.8516 | 0.8516 | 0 | 72 | 1 | [] |
| banking | head_only | 2026 | frozen_centroid | 0.1246 | 0.1246 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2026 | last_active | 0.0774 | 0.0774 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2026 | uniform_probability | 0.0712 | 0.0712 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2027 | frozen_centroid | 0.1129 | 0.1129 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2027 | last_active | 0.0978 | 0.0978 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2027 | uniform_probability | 0.0137 | 0.0137 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2026 | frozen_centroid | 0.1613 | 0.1613 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2026 | last_active | 0.1022 | 0.1022 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2026 | uniform_probability | 0.1222 | 0.1222 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2027 | frozen_centroid | 0.1584 | 0.1584 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2027 | last_active | 0.1462 | 0.1462 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2027 | uniform_probability | 0.0860 | 0.0860 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |

Only ranking uses pre-update current-query loss. Exact AdamW protected-memory guards remain. No inference about the benefit of all lookahead computation or a runtime speedup follows. Three canonical-order development seeds require broader confirmation.
