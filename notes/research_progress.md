# Research progress and evidence handoff

Generated 2026-10-07T02:51:38.940520+00:00. This is a development report, not a submission-ready paper.

## Decision

Carry forward the mechanistic audit and the original private-package implementation as a reference. The present results do not establish that the allocation policy identifies a need for new LoRA capacity, or that it improves deployable accuracy across these regimes. The useful candidate contribution is a controlled account of classifier resets, optimizer state, prospective learning gain, and inference routing. Modern source-faithful comparators and stronger same-label learning regimes are still required.

## Verified study coverage

| study | completed | planned | last_status |
| --- | --- | --- | --- |
| 5 | 6 | 6 | completed |
| 6 | 80 | 80 | completed |
| 7 | 24 | 24 | completed |
| 9 | 110 | 110 | completed |
| 8 | 44 | 44 | completed |
| 10 | 12 | 12 | completed |
| 12 | 11 | 11 | completed |
| 14 fixed-memory routing | 44 | 44 | completed |
| 15 | 9 | 20 | completed |
| 16 | 20 | 20 | completed |
| 5 head-only | 2 | 2 | completed |

Complete trajectories alone enter summaries. A queue record is an execution status; the independent evidence audit also checks the saved trajectory summary, full step count and final metrics.

## Primary five-seed results

Seeds 2027–2031 each have canonical and B-first orders. Average both orders within a seed before descriptive 95% Student-t intervals. Fixed development examples define the scope; windows and orders are not independent replicates. All three fixed routing rules are reported. Macro accuracy averages three concept-level accuracies; it is not BANKING per-class macro accuracy.

| regime | rule | architecture | policy | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | frozen_centroid | head_only | cau | 5 | 0.8042 | 0.7967 | 0.8116 |
| amazon | frozen_centroid | head_only | single | 5 | 0.8070 | 0.7890 | 0.8250 |
| amazon | frozen_centroid | private | cau | 5 | 0.8341 | 0.8101 | 0.8582 |
| amazon | frozen_centroid | private | single | 5 | 0.8510 | 0.8467 | 0.8554 |
| amazon | last_active | head_only | cau | 5 | 0.8042 | 0.7967 | 0.8116 |
| amazon | last_active | head_only | single | 5 | 0.8070 | 0.7890 | 0.8250 |
| amazon | last_active | private | cau | 5 | 0.8078 | 0.7128 | 0.9028 |
| amazon | last_active | private | single | 5 | 0.8510 | 0.8467 | 0.8554 |
| amazon | uniform_probability | head_only | cau | 5 | 0.8042 | 0.7967 | 0.8116 |
| amazon | uniform_probability | head_only | single | 5 | 0.8070 | 0.7890 | 0.8250 |
| amazon | uniform_probability | private | cau | 5 | 0.8396 | 0.8269 | 0.8523 |
| amazon | uniform_probability | private | single | 5 | 0.8510 | 0.8467 | 0.8554 |
| banking | frozen_centroid | head_only | cau | 5 | 0.1102 | 0.0801 | 0.1403 |
| banking | frozen_centroid | head_only | single | 5 | 0.1235 | 0.1113 | 0.1358 |
| banking | frozen_centroid | private | cau | 5 | 0.1590 | 0.1408 | 0.1773 |
| banking | frozen_centroid | private | single | 5 | 0.1644 | 0.1246 | 0.2043 |
| banking | last_active | head_only | cau | 5 | 0.0682 | 0.0464 | 0.0900 |
| banking | last_active | head_only | single | 5 | 0.1235 | 0.1113 | 0.1358 |
| banking | last_active | private | cau | 5 | 0.1043 | 0.0889 | 0.1198 |
| banking | last_active | private | single | 5 | 0.1644 | 0.1246 | 0.2043 |
| banking | uniform_probability | head_only | cau | 5 | 0.0755 | 0.0270 | 0.1240 |
| banking | uniform_probability | head_only | single | 5 | 0.1235 | 0.1113 | 0.1358 |
| banking | uniform_probability | private | cau | 5 | 0.1310 | 0.0818 | 0.1801 |
| banking | uniform_probability | private | single | 5 | 0.1644 | 0.1246 | 0.2043 |

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | frozen_centroid | LoRA minus head-only / CAU | 5 | 0.0299 | 0.0130 | 0.0469 |
| amazon | frozen_centroid | LoRA minus head-only / single | 5 | 0.0440 | 0.0265 | 0.0615 |
| amazon | frozen_centroid | CAU minus single / private | 5 | -0.0169 | -0.0405 | 0.0066 |
| amazon | frozen_centroid | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |
| amazon | last_active | LoRA minus head-only / CAU | 5 | 0.0036 | -0.0850 | 0.0923 |
| amazon | last_active | LoRA minus head-only / single | 5 | 0.0440 | 0.0265 | 0.0615 |
| amazon | last_active | CAU minus single / private | 5 | -0.0432 | -0.1370 | 0.0505 |
| amazon | last_active | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |
| amazon | uniform_probability | LoRA minus head-only / CAU | 5 | 0.0354 | 0.0282 | 0.0426 |
| amazon | uniform_probability | LoRA minus head-only / single | 5 | 0.0440 | 0.0265 | 0.0615 |
| amazon | uniform_probability | CAU minus single / private | 5 | -0.0115 | -0.0250 | 0.0020 |
| amazon | uniform_probability | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |
| banking | frozen_centroid | LoRA minus head-only / CAU | 5 | 0.0489 | 0.0172 | 0.0805 |
| banking | frozen_centroid | LoRA minus head-only / single | 5 | 0.0409 | -0.0005 | 0.0823 |
| banking | frozen_centroid | CAU minus single / private | 5 | -0.0054 | -0.0399 | 0.0291 |
| banking | frozen_centroid | CAU minus single / head-only | 5 | -0.0134 | -0.0363 | 0.0096 |
| banking | last_active | LoRA minus head-only / CAU | 5 | 0.0361 | 0.0136 | 0.0586 |
| banking | last_active | LoRA minus head-only / single | 5 | 0.0409 | -0.0005 | 0.0823 |
| banking | last_active | CAU minus single / private | 5 | -0.0601 | -0.1060 | -0.0142 |
| banking | last_active | CAU minus single / head-only | 5 | -0.0553 | -0.0694 | -0.0413 |
| banking | uniform_probability | LoRA minus head-only / CAU | 5 | 0.0555 | 0.0042 | 0.1068 |
| banking | uniform_probability | LoRA minus head-only / single | 5 | 0.0409 | -0.0005 | 0.0823 |
| banking | uniform_probability | CAU minus single / private | 5 | -0.0335 | -0.0835 | 0.0166 |
| banking | uniform_probability | CAU minus single / head-only | 5 | -0.0481 | -0.0870 | -0.0091 |


## Mechanism

On the original BANKING trajectory, fresh classifier reset with reused LoRA yielded substantially larger held-out one-step loss gains than replacing LoRA under a fresh classifier. The factorial changes both component weights and their corresponding AdamW moments, so it does not identify weights independently of moments. About 87% of fresh-versus-best-reuse utility at both spawn steps was an initial predictor gap, before the proposed update. Initial gap itself changes the whole package, not only the head.

The BANKING private and zero-LoRA head-only controllers made identical adapter/decision sequences across all ten fresh-seed/order trajectories. LoRA training improved classifier performance despite these identical structural decisions. Do not conflate prediction benefit with allocation necessity.

| regime | seed | order | private_spawn_steps | head_only_spawn_steps | allocation_disagreements |
| --- | --- | --- | --- | --- | --- |
| banking | 2027 | canonical | [18, 50] | [18, 50] | 0 |
| banking | 2027 | b_first | [18, 50] | [18, 50] | 0 |
| banking | 2028 | canonical | [18, 50] | [18, 50] | 0 |
| banking | 2028 | b_first | [18, 50] | [18, 50] | 0 |
| banking | 2029 | canonical | [18, 50] | [18, 50] | 0 |
| banking | 2029 | b_first | [18, 50] | [18, 50] | 0 |
| banking | 2030 | canonical | [18, 50] | [18, 50] | 0 |
| banking | 2030 | b_first | [18, 50] | [18, 50] | 0 |
| banking | 2031 | canonical | [18, 50] | [18, 50] | 0 |
| banking | 2031 | b_first | [18, 50] | [18, 50] | 0 |
| amazon | 2027 | canonical | [] | [] | 8 |
| amazon | 2027 | b_first | [] | [] | 10 |
| amazon | 2028 | canonical | [] | [] | 9 |
| amazon | 2028 | b_first | [] | [] | 10 |
| amazon | 2029 | canonical | [67] | [] | 16 |
| amazon | 2029 | b_first | [] | [] | 7 |
| amazon | 2030 | canonical | [] | [] | 19 |
| amazon | 2030 | b_first | [] | [] | 2 |
| amazon | 2031 | canonical | [] | [] | 8 |
| amazon | 2031 | b_first | [] | [] | 12 |


The closed-loop pre-update ranking sensitivity preserves prospective AdamW retention guards. Its original seed-2026 pilots made no allocation changes. This does not show that all lookahead computation is unnecessary: prospective protected-memory checks remain. Later pilot seeds are shown below.

| regime | architecture | seed | rule | initial_loss_accuracy | post_update_accuracy | allocation_disagreements | updates | adapters | spawns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | head_only | 2026 | frozen_centroid | 0.8255 | 0.8255 | 0 | 80 | 1 | [] |
| amazon | head_only | 2026 | last_active | 0.8255 | 0.8255 | 0 | 80 | 1 | [] |
| amazon | head_only | 2026 | uniform_probability | 0.8255 | 0.8255 | 0 | 80 | 1 | [] |
| amazon | head_only | 2027 | frozen_centroid | 0.7943 | 0.7943 | 0 | 80 | 1 | [] |
| amazon | head_only | 2027 | last_active | 0.7943 | 0.7943 | 0 | 80 | 1 | [] |
| amazon | head_only | 2027 | uniform_probability | 0.7943 | 0.7943 | 0 | 80 | 1 | [] |
| amazon | head_only | 2028 | frozen_centroid | 0.6771 | 0.7995 | 24 | 80 | 2 | [{"step":16,"segment":"A1"}] |
| amazon | head_only | 2028 | last_active | 0.7734 | 0.7995 | 24 | 80 | 2 | [{"step":16,"segment":"A1"}] |
| amazon | head_only | 2028 | uniform_probability | 0.6250 | 0.7995 | 24 | 80 | 2 | [{"step":16,"segment":"A1"}] |
| amazon | private | 2026 | frozen_centroid | 0.8542 | 0.8542 | 0 | 79 | 1 | [] |
| amazon | private | 2026 | last_active | 0.8542 | 0.8542 | 0 | 79 | 1 | [] |
| amazon | private | 2026 | uniform_probability | 0.8542 | 0.8542 | 0 | 79 | 1 | [] |
| amazon | private | 2027 | frozen_centroid | 0.8516 | 0.8516 | 0 | 72 | 1 | [] |
| amazon | private | 2027 | last_active | 0.8516 | 0.8516 | 0 | 72 | 1 | [] |
| amazon | private | 2027 | uniform_probability | 0.8516 | 0.8516 | 0 | 72 | 1 | [] |
| amazon | private | 2028 | frozen_centroid | 0.7474 | 0.8333 | 30 | 80 | 2 | [{"step":16,"segment":"A1"}] |
| amazon | private | 2028 | last_active | 0.8411 | 0.8333 | 30 | 80 | 2 | [{"step":16,"segment":"A1"}] |
| amazon | private | 2028 | uniform_probability | 0.8542 | 0.8333 | 30 | 80 | 2 | [{"step":16,"segment":"A1"}] |
| banking | head_only | 2026 | frozen_centroid | 0.1246 | 0.1246 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2026 | last_active | 0.0774 | 0.0774 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2026 | uniform_probability | 0.0712 | 0.0712 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2027 | frozen_centroid | 0.1129 | 0.1129 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2027 | last_active | 0.0978 | 0.0978 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2027 | uniform_probability | 0.0137 | 0.0137 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2028 | frozen_centroid | 0.1309 | 0.1309 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2028 | last_active | 0.0591 | 0.0591 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | head_only | 2028 | uniform_probability | 0.1219 | 0.1219 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2026 | frozen_centroid | 0.1613 | 0.1613 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2026 | last_active | 0.1022 | 0.1022 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2026 | uniform_probability | 0.1222 | 0.1222 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2027 | frozen_centroid | 0.1584 | 0.1584 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2027 | last_active | 0.1462 | 0.1462 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2027 | uniform_probability | 0.0860 | 0.0860 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2028 | frozen_centroid | 0.1750 | 0.1750 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2028 | last_active | 0.1247 | 0.1247 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |
| banking | private | 2028 | uniform_probability | 0.1442 | 0.1442 | 0 | 80 | 3 | [{"step":18,"segment":"B1"},{"step":50,"segment":"C1"}] |


## Third regime and deployment

MultiNLI uses only training data, with normalized-premise-grouped development holdout, genuine paired tokenization and sharp/blurry transitions that preserve examples. Three seeds and two boundary variants are descriptive transfer checks. The 64-token, 1440-example stress test produces low learning; allocation often performs near balanced chance (one third). It is not a competitive NLI benchmark.

| seed | condition | architecture | policy | rule | macro_accuracy | updates | adapters |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | blurry | head_only | cau | frozen_centroid | 0.3281 | 90 | 4 |
| 2026 | blurry | head_only | cau | last_active | 0.3351 | 90 | 4 |
| 2026 | blurry | head_only | cau | uniform_probability | 0.3542 | 90 | 4 |
| 2026 | sharp | head_only | cau | frozen_centroid | 0.3333 | 90 | 3 |
| 2026 | sharp | head_only | cau | last_active | 0.3316 | 90 | 3 |
| 2026 | sharp | head_only | cau | uniform_probability | 0.3958 | 90 | 3 |
| 2027 | blurry | head_only | cau | frozen_centroid | 0.3333 | 90 | 5 |
| 2027 | blurry | head_only | cau | last_active | 0.3351 | 90 | 5 |
| 2027 | blurry | head_only | cau | uniform_probability | 0.3420 | 90 | 5 |
| 2027 | sharp | head_only | cau | frozen_centroid | 0.3333 | 90 | 5 |
| 2027 | sharp | head_only | cau | last_active | 0.3333 | 90 | 5 |
| 2027 | sharp | head_only | cau | uniform_probability | 0.3403 | 90 | 5 |
| 2028 | blurry | head_only | cau | frozen_centroid | 0.3264 | 90 | 3 |
| 2028 | blurry | head_only | cau | last_active | 0.3438 | 90 | 3 |
| 2028 | blurry | head_only | cau | uniform_probability | 0.3438 | 90 | 3 |
| 2028 | sharp | head_only | cau | frozen_centroid | 0.3455 | 90 | 4 |
| 2028 | sharp | head_only | cau | last_active | 0.3333 | 90 | 4 |
| 2028 | sharp | head_only | cau | uniform_probability | 0.3438 | 90 | 4 |
| 2026 | blurry | head_only | single | frozen_centroid | 0.3646 | 90 | 1 |
| 2026 | blurry | head_only | single | last_active | 0.3646 | 90 | 1 |
| 2026 | blurry | head_only | single | uniform_probability | 0.3646 | 90 | 1 |
| 2026 | sharp | head_only | single | frozen_centroid | 0.3611 | 90 | 1 |
| 2026 | sharp | head_only | single | last_active | 0.3611 | 90 | 1 |
| 2026 | sharp | head_only | single | uniform_probability | 0.3611 | 90 | 1 |
| 2027 | blurry | head_only | single | frozen_centroid | 0.3542 | 90 | 1 |
| 2027 | blurry | head_only | single | last_active | 0.3542 | 90 | 1 |
| 2027 | blurry | head_only | single | uniform_probability | 0.3542 | 90 | 1 |
| 2027 | sharp | head_only | single | frozen_centroid | 0.3524 | 90 | 1 |
| 2027 | sharp | head_only | single | last_active | 0.3524 | 90 | 1 |
| 2027 | sharp | head_only | single | uniform_probability | 0.3524 | 90 | 1 |
| 2028 | blurry | head_only | single | frozen_centroid | 0.3872 | 90 | 1 |
| 2028 | blurry | head_only | single | last_active | 0.3872 | 90 | 1 |
| 2028 | blurry | head_only | single | uniform_probability | 0.3872 | 90 | 1 |
| 2028 | sharp | head_only | single | frozen_centroid | 0.3802 | 90 | 1 |
| 2028 | sharp | head_only | single | last_active | 0.3802 | 90 | 1 |
| 2028 | sharp | head_only | single | uniform_probability | 0.3802 | 90 | 1 |
| 2026 | blurry | private | cau | frozen_centroid | 0.3299 | 90 | 3 |
| 2026 | blurry | private | cau | last_active | 0.3333 | 90 | 3 |
| 2026 | blurry | private | cau | uniform_probability | 0.3212 | 90 | 3 |
| 2026 | sharp | private | cau | frozen_centroid | 0.3333 | 90 | 3 |
| 2026 | sharp | private | cau | last_active | 0.3316 | 90 | 3 |
| 2026 | sharp | private | cau | uniform_probability | 0.3941 | 90 | 3 |
| 2027 | blurry | private | cau | frozen_centroid | 0.3333 | 90 | 5 |
| 2027 | blurry | private | cau | last_active | 0.3351 | 90 | 5 |
| 2027 | blurry | private | cau | uniform_probability | 0.3403 | 90 | 5 |
| 2027 | sharp | private | cau | frozen_centroid | 0.3385 | 90 | 5 |
| 2027 | sharp | private | cau | last_active | 0.3333 | 90 | 5 |
| 2027 | sharp | private | cau | uniform_probability | 0.3316 | 90 | 5 |
| 2028 | blurry | private | cau | frozen_centroid | 0.3264 | 90 | 3 |
| 2028 | blurry | private | cau | last_active | 0.3420 | 90 | 3 |
| 2028 | blurry | private | cau | uniform_probability | 0.3490 | 90 | 3 |
| 2028 | sharp | private | cau | frozen_centroid | 0.3438 | 90 | 4 |
| 2028 | sharp | private | cau | last_active | 0.3333 | 90 | 4 |
| 2028 | sharp | private | cau | uniform_probability | 0.3385 | 90 | 4 |
| 2026 | blurry | private | single | frozen_centroid | 0.3750 | 90 | 1 |
| 2026 | blurry | private | single | last_active | 0.3750 | 90 | 1 |
| 2026 | blurry | private | single | uniform_probability | 0.3750 | 90 | 1 |
| 2026 | sharp | private | single | frozen_centroid | 0.3767 | 90 | 1 |
| 2026 | sharp | private | single | last_active | 0.3767 | 90 | 1 |
| 2026 | sharp | private | single | uniform_probability | 0.3767 | 90 | 1 |
| 2027 | blurry | private | single | frozen_centroid | 0.3715 | 90 | 1 |
| 2027 | blurry | private | single | last_active | 0.3715 | 90 | 1 |
| 2027 | blurry | private | single | uniform_probability | 0.3715 | 90 | 1 |
| 2027 | sharp | private | single | frozen_centroid | 0.3559 | 90 | 1 |
| 2027 | sharp | private | single | last_active | 0.3559 | 90 | 1 |
| 2027 | sharp | private | single | uniform_probability | 0.3559 | 90 | 1 |
| 2028 | blurry | private | single | frozen_centroid | 0.3924 | 90 | 1 |
| 2028 | blurry | private | single | last_active | 0.3924 | 90 | 1 |
| 2028 | blurry | private | single | uniform_probability | 0.3924 | 90 | 1 |
| 2028 | sharp | private | single | frozen_centroid | 0.3767 | 90 | 1 |
| 2028 | sharp | private | single | last_active | 0.3767 | 90 | 1 |
| 2028 | sharp | private | single | uniform_probability | 0.3767 | 90 | 1 |


A standard linear router was added after the initial routing failure, then frozen before its own outcomes. It learns past adapter ownership from training reservoir texts without true task IDs or class labels. Both hard routing and probability mixture are auxiliary development outcomes; their use is not a new routing contribution or a reproduction of L2R/HESTIA. Checkpoint reload checks compare nine aggregate sample counts and accuracies, not previously saved per-example prediction vectors.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | linear_hard | LoRA minus head-only / CAU | 5 | 0.0271 | 0.0027 | 0.0515 |
| amazon | linear_hard | CAU minus single / private | 5 | -0.0198 | -0.0504 | 0.0108 |
| amazon | linear_hard | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |
| amazon | linear_probability_mixture | LoRA minus head-only / CAU | 5 | 0.0297 | 0.0121 | 0.0473 |
| amazon | linear_probability_mixture | CAU minus single / private | 5 | -0.0172 | -0.0414 | 0.0070 |
| amazon | linear_probability_mixture | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |
| banking | linear_hard | LoRA minus head-only / CAU | 5 | 0.0607 | 0.0063 | 0.1151 |
| banking | linear_hard | CAU minus single / private | 5 | 0.0595 | 0.0160 | 0.1030 |
| banking | linear_hard | CAU minus single / head-only | 5 | 0.0396 | 0.0006 | 0.0787 |
| banking | linear_probability_mixture | LoRA minus head-only / CAU | 5 | 0.0622 | 0.0056 | 0.1188 |
| banking | linear_probability_mixture | CAU minus single / private | 5 | 0.0560 | 0.0102 | 0.1019 |
| banking | linear_probability_mixture | CAU minus single / head-only | 5 | 0.0347 | -0.0025 | 0.0718 |


## Resource sensitivities

The fixed-memory extension limits total stored training examples to 512 and preserves 64-example probes. It also caps the pool at eight. The rank-96 single baseline was selected by parameter arithmetic near three rank-8 private packages; it is not universally parameter matched to an uncapped growing pool. Memory, head storage, optimizer state, active-update compute and inference compute remain separate resources. Poor rank-96 performance under the shared fixed recipe does not establish superiority over a tuned larger static baseline; baseline-specific tuning with pilot/confirmation separation remains necessary.

| regime | architecture | rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | head_only | frozen_centroid | 5 | 0.0000 | 0.0000 | 0.0000 |
| amazon | head_only | last_active | 5 | 0.0000 | 0.0000 | 0.0000 |
| amazon | head_only | uniform_probability | 5 | 0.0000 | 0.0000 | 0.0000 |
| amazon | private | frozen_centroid | 5 | -0.0013 | -0.0049 | 0.0023 |
| amazon | private | last_active | 5 | 0.0005 | -0.0009 | 0.0020 |
| amazon | private | uniform_probability | 5 | -0.0003 | -0.0010 | 0.0005 |
| banking | head_only | frozen_centroid | 5 | 0.0015 | -0.0024 | 0.0053 |
| banking | head_only | last_active | 5 | 0.0000 | 0.0000 | 0.0000 |
| banking | head_only | uniform_probability | 5 | 0.0000 | 0.0000 | 0.0000 |
| banking | private | frozen_centroid | 5 | 0.0038 | 0.0012 | 0.0064 |
| banking | private | last_active | 5 | 0.0000 | 0.0000 | 0.0000 |
| banking | private | uniform_probability | 5 | 0.0000 | 0.0000 | 0.0000 |


| rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| frozen_centroid | rank96_minus_rank8 | 5 | -0.0946 | -0.1406 | -0.0486 |
| frozen_centroid | rank96_minus_adaptive | 5 | -0.0892 | -0.1235 | -0.0549 |
| last_active | rank96_minus_rank8 | 5 | -0.0946 | -0.1406 | -0.0486 |
| last_active | rank96_minus_adaptive | 5 | -0.0345 | -0.0755 | 0.0066 |
| uniform_probability | rank96_minus_rank8 | 5 | -0.0946 | -0.1406 | -0.0486 |
| uniform_probability | rank96_minus_adaptive | 5 | -0.0611 | -0.0900 | -0.0323 |


## Fixed-memory learned routing and extended attribution

| regime | architecture | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | head_only | linear_hard | fixed_minus_per_adapter | 5 | 0.0000 | 0.0000 | 0.0000 |
| amazon | head_only | linear_hard | fixed_minus_single | 5 | -0.0029 | -0.0242 | 0.0184 |
| amazon | head_only | linear_hard | fixed_minus_rank96 | 0 | nan | nan | nan |
| amazon | head_only | linear_probability_mixture | fixed_minus_per_adapter | 5 | 0.0000 | 0.0000 | 0.0000 |
| amazon | head_only | linear_probability_mixture | fixed_minus_single | 5 | -0.0029 | -0.0242 | 0.0184 |
| amazon | head_only | linear_probability_mixture | fixed_minus_rank96 | 0 | nan | nan | nan |
| amazon | private | linear_hard | fixed_minus_per_adapter | 5 | -0.0026 | -0.0098 | 0.0046 |
| amazon | private | linear_hard | fixed_minus_single | 5 | -0.0224 | -0.0597 | 0.0149 |
| amazon | private | linear_hard | fixed_minus_rank96 | 0 | nan | nan | nan |
| amazon | private | linear_probability_mixture | fixed_minus_per_adapter | 5 | -0.0008 | -0.0030 | 0.0014 |
| amazon | private | linear_probability_mixture | fixed_minus_single | 5 | -0.0180 | -0.0440 | 0.0081 |
| amazon | private | linear_probability_mixture | fixed_minus_rank96 | 0 | nan | nan | nan |
| banking | head_only | linear_hard | fixed_minus_per_adapter | 5 | -0.0051 | -0.0156 | 0.0054 |
| banking | head_only | linear_hard | fixed_minus_single | 5 | 0.0345 | -0.0061 | 0.0751 |
| banking | head_only | linear_hard | fixed_minus_rank96 | 0 | nan | nan | nan |
| banking | head_only | linear_probability_mixture | fixed_minus_per_adapter | 5 | -0.0009 | -0.0120 | 0.0103 |
| banking | head_only | linear_probability_mixture | fixed_minus_single | 5 | 0.0338 | -0.0027 | 0.0703 |
| banking | head_only | linear_probability_mixture | fixed_minus_rank96 | 0 | nan | nan | nan |
| banking | private | linear_hard | fixed_minus_per_adapter | 5 | -0.0060 | -0.0148 | 0.0029 |
| banking | private | linear_hard | fixed_minus_single | 5 | 0.0535 | 0.0082 | 0.0988 |
| banking | private | linear_hard | fixed_minus_rank96 | 5 | 0.1481 | 0.1125 | 0.1837 |
| banking | private | linear_probability_mixture | fixed_minus_per_adapter | 5 | -0.0019 | -0.0098 | 0.0060 |
| banking | private | linear_probability_mixture | fixed_minus_single | 5 | 0.0541 | 0.0067 | 0.1014 |
| banking | private | linear_probability_mixture | fixed_minus_rank96 | 5 | 0.1487 | 0.1154 | 0.1820 |


The Day-15 observer independently crosses LoRA/head weights with LoRA/head AdamW state. All mature batches and every cell are retained. Only verified bitwise paired trajectory/state reproductions enter its causal summaries. The Day-16 BERT check tests transfer beyond the DistilBERT classifier stack; multiple backbone components change together, so it does not isolate classifier architecture causally. Both studies are development extensions, not untouched test confirmations. Current novelty limits are in notes/novelty_audit_20261006.md.

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0008 | -0.0692 | 0.0675 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0008 | -0.0692 | 0.0675 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0008 | -0.0692 | 0.0675 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0050 | -0.0274 | 0.0374 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0050 | -0.0274 | 0.0374 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0050 | -0.0274 | 0.0374 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0047 | -0.0715 | 0.0621 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0047 | -0.0715 | 0.0621 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0047 | -0.0715 | 0.0621 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0044 | -0.0280 | 0.0368 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0044 | -0.0280 | 0.0368 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0044 | -0.0280 | 0.0368 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0068 | 0.0022 | 0.0114 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0068 | 0.0022 | 0.0114 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0068 | 0.0022 | 0.0114 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0015 | -0.0113 | 0.0083 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0015 | -0.0113 | 0.0083 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0015 | -0.0113 | 0.0083 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0064 | 0.0035 | 0.0093 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0064 | 0.0035 | 0.0093 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0064 | 0.0035 | 0.0093 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0015 | -0.0114 | 0.0083 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0015 | -0.0114 | 0.0083 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0015 | -0.0114 | 0.0083 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1958 | -0.4824 | 0.0908 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0076 | -0.0029 | 0.0181 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.1958 | -0.4824 | 0.0908 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0973 | -0.1803 | -0.0142 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0007 | -0.0039 | 0.0024 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0973 | -0.1803 | -0.0142 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1961 | -0.4435 | 0.0513 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0072 | -0.0215 | 0.0360 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.1961 | -0.4435 | 0.0513 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0987 | -0.1809 | -0.0165 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0022 | -0.0063 | 0.0019 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0987 | -0.1809 | -0.0165 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1881 | -0.4017 | 0.0255 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0152 | -0.0473 | 0.0778 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.1881 | -0.4017 | 0.0255 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.1037 | -0.1642 | -0.0432 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0072 | -0.0330 | 0.0185 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.1037 | -0.1642 | -0.0432 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1850 | -0.3627 | -0.0074 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0183 | -0.0801 | 0.1168 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.2034 | -0.4795 | 0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.1850 | -0.3627 | -0.0074 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.1046 | -0.1642 | -0.0450 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0081 | -0.0348 | 0.0185 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0965 | -0.1828 | -0.0102 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.1046 | -0.1642 | -0.0450 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0009 | -0.0346 | 0.0363 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0009 | -0.0346 | 0.0363 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0009 | -0.0346 | 0.0363 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0015 | 0.0004 | 0.0025 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0015 | 0.0004 | 0.0025 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0015 | 0.0004 | 0.0025 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0005 | -0.0033 | 0.0043 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0005 | -0.0033 | 0.0043 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0005 | -0.0033 | 0.0043 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0000 | -0.0001 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0000 | -0.0001 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0000 | -0.0001 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0030 | -0.0369 | 0.0308 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0030 | -0.0369 | 0.0308 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0030 | -0.0369 | 0.0308 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0009 | -0.0002 | 0.0019 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0009 | -0.0002 | 0.0019 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0009 | -0.0002 | 0.0019 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0001 | -0.0020 | 0.0022 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0001 | -0.0020 | 0.0022 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0001 | -0.0020 | 0.0022 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0000 | -0.0002 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0000 | -0.0002 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0000 | -0.0002 | 0.0001 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1077 | -0.2288 | 0.0135 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 2 | 0.0009 | -0.0085 | 0.0104 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.1077 | -0.2288 | 0.0135 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.1071 | -0.1938 | -0.0203 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 2 | 0.0015 | -0.0234 | 0.0265 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.1071 | -0.1938 | -0.0203 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0091 | -0.0915 | 0.0733 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 2 | -0.0074 | -0.0115 | -0.0032 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.0091 | -0.0915 | 0.0733 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0096 | -0.0881 | 0.0689 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 2 | -0.0079 | -0.0082 | -0.0076 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0096 | -0.0881 | 0.0689 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1018 | -0.1870 | -0.0167 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 2 | 0.0068 | -0.0197 | 0.0333 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.1018 | -0.1870 | -0.0167 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0979 | -0.1503 | -0.0456 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 2 | 0.0107 | -0.0487 | 0.0700 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.1086 | -0.2203 | 0.0031 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0979 | -0.1503 | -0.0456 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0174 | -0.0854 | 0.0506 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 2 | -0.0157 | -0.0259 | -0.0054 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.0174 | -0.0854 | 0.0506 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0175 | -0.0832 | 0.0482 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 2 | -0.0158 | -0.0283 | -0.0033 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.0017 | -0.0799 | 0.0765 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0175 | -0.0832 | 0.0482 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.0016 | -0.0454 | 0.0486 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | 0.0016 | -0.0454 | 0.0486 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0016 | -0.0454 | 0.0486 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.0001 | -0.0192 | 0.0194 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | 0.0001 | -0.0192 | 0.0194 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0001 | -0.0192 | 0.0194 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | -0.0013 | -0.0013 | -0.0012 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | -0.0013 | -0.0013 | -0.0012 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | -0.0013 | -0.0013 | -0.0012 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | -0.0003 | -0.0111 | 0.0105 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | -0.0003 | -0.0111 | 0.0105 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | -0.0003 | -0.0111 | 0.0105 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.0902 | -0.0698 | 0.2502 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_loss_decrease | 2 | 0.1069 | -0.0830 | 0.2968 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | local_improvement_increase | 2 | -0.0167 | -0.0466 | 0.0132 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.1069 | -0.0830 | 0.2968 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0902 | -0.0698 | 0.2502 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.0010 | -0.0143 | 0.0162 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | 0.0010 | -0.0143 | 0.0162 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0010 | -0.0143 | 0.0162 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_update_loss_decrease | 2 | 0.0017 | -0.0248 | 0.0283 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | local_improvement_increase | 2 | 0.0017 | -0.0248 | 0.0283 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_within_group_decrease | 2 | 0.0017 | -0.0248 | 0.0283 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_update_loss_decrease | 2 | -0.1462 | -0.2975 | 0.0052 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_loss_decrease | 2 | -0.1499 | -0.3312 | 0.0313 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | local_improvement_increase | 2 | 0.0038 | -0.0261 | 0.0336 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_within_group_decrease | 2 | -0.1499 | -0.3312 | 0.0313 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_within_group_decrease | 2 | -0.1462 | -0.2975 | 0.0052 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_update_loss_decrease | 2 | 0.0001 | -0.0081 | 0.0083 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | local_improvement_increase | 2 | 0.0001 | -0.0081 | 0.0083 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_within_group_decrease | 2 | 0.0001 | -0.0081 | 0.0083 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_update_loss_decrease | 2 | -0.0585 | -0.0649 | -0.0522 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_loss_decrease | 2 | -0.0552 | -0.0719 | -0.0384 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | local_improvement_increase | 2 | -0.0033 | -0.0137 | 0.0070 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_within_group_decrease | 2 | -0.0552 | -0.0719 | -0.0384 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_within_group_decrease | 2 | -0.0585 | -0.0649 | -0.0522 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0041 | -0.0424 | 0.0342 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0041 | -0.0424 | 0.0342 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.0006 | -0.0040 | 0.0028 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0035 | -0.0383 | 0.0314 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0042 | -0.0250 | 0.0166 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0042 | -0.0250 | 0.0166 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.0028 | -0.0075 | 0.0018 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0013 | -0.0175 | 0.0148 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0047 | -0.0430 | 0.0336 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0047 | -0.0430 | 0.0336 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.0011 | -0.0047 | 0.0026 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0036 | -0.0383 | 0.0310 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0044 | -0.0254 | 0.0167 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0044 | -0.0254 | 0.0167 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.0030 | -0.0076 | 0.0017 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0014 | -0.0178 | 0.0150 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0018 | -0.0347 | 0.0312 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0018 | -0.0347 | 0.0312 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0007 | -0.0066 | 0.0080 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0025 | -0.0281 | 0.0231 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0021 | -0.0230 | 0.0187 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0021 | -0.0230 | 0.0187 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.0010 | -0.0051 | 0.0031 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0012 | -0.0180 | 0.0156 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0019 | -0.0340 | 0.0303 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0019 | -0.0340 | 0.0303 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0007 | -0.0067 | 0.0080 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0025 | -0.0273 | 0.0223 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0022 | -0.0231 | 0.0188 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0022 | -0.0231 | 0.0188 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.0010 | -0.0051 | 0.0031 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0012 | -0.0180 | 0.0156 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9094 | -0.9342 | -0.8846 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.9094 | -0.9523 | -0.8666 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0001 | -0.0180 | 0.0181 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | -0.8768 | -0.8877 | -0.8659 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.0326 | -0.0864 | 0.0211 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.8762 | -0.9056 | -0.8468 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0332 | -0.0873 | 0.0210 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.7956 | -0.8279 | -0.7632 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.7895 | -0.8271 | -0.7519 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0060 | -0.0113 | -0.0007 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | -0.7659 | -0.7664 | -0.7654 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0236 | -0.0618 | 0.0145 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.7721 | -0.7799 | -0.7644 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0234 | -0.0635 | 0.0167 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9121 | -0.9377 | -0.8865 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.9094 | -0.9523 | -0.8666 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0027 | -0.0199 | 0.0145 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | -0.8768 | -0.8877 | -0.8659 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.0326 | -0.0864 | 0.0211 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.8785 | -0.9085 | -0.8485 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0336 | -0.0892 | 0.0220 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.8010 | -0.8291 | -0.7728 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.7895 | -0.8271 | -0.7519 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0114 | -0.0208 | -0.0020 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | -0.7659 | -0.7664 | -0.7654 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0236 | -0.0618 | 0.0145 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.7772 | -0.7892 | -0.7652 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0238 | -0.0639 | 0.0164 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9071 | -0.9372 | -0.8769 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.9094 | -0.9523 | -0.8666 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0024 | -0.0103 | 0.0151 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | -0.8768 | -0.8877 | -0.8659 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.0326 | -0.0864 | 0.0211 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.8749 | -0.9082 | -0.8415 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0322 | -0.0957 | 0.0313 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.7935 | -0.8258 | -0.7613 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.7895 | -0.8271 | -0.7519 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0040 | -0.0093 | 0.0014 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | -0.7659 | -0.7664 | -0.7654 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0236 | -0.0618 | 0.0145 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.7703 | -0.7775 | -0.7631 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0232 | -0.0627 | 0.0162 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9093 | -0.9410 | -0.8776 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | -0.9094 | -0.9523 | -0.8666 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0001 | -0.0110 | 0.0113 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | -0.8768 | -0.8877 | -0.8659 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | -0.0326 | -0.0864 | 0.0211 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.8768 | -0.9106 | -0.8430 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | -0.0325 | -0.0980 | 0.0330 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.7987 | -0.8271 | -0.7704 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | -0.7895 | -0.8271 | -0.7519 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 2 | -0.0092 | -0.0185 | 0.0001 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | -0.7659 | -0.7664 | -0.7654 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | -0.0236 | -0.0618 | 0.0145 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | -0.7752 | -0.7866 | -0.7638 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | -0.0236 | -0.0633 | 0.0162 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0028 | 0.0007 | 0.0048 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0028 | 0.0007 | 0.0048 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0022 | 0.0011 | 0.0034 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0005 | -0.0004 | 0.0014 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0059 | 0.0027 | 0.0091 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0059 | 0.0027 | 0.0091 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0055 | 0.0017 | 0.0092 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0004 | -0.0002 | 0.0010 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0000 | -0.0012 | 0.0012 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0000 | -0.0012 | 0.0012 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.0001 | -0.0019 | 0.0017 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0001 | -0.0005 | 0.0006 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0005 | -0.0005 | 0.0014 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0005 | -0.0005 | 0.0014 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0004 | -0.0000 | 0.0009 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0000 | -0.0005 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0022 | 0.0001 | 0.0042 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 2 | 0.0022 | 0.0001 | 0.0042 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 2 | 0.0018 | 0.0004 | 0.0032 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0003 | -0.0003 | 0.0010 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0057 | 0.0028 | 0.0086 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0057 | 0.0028 | 0.0086 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0054 | 0.0016 | 0.0091 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0003 | -0.0005 | 0.0011 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0001 | -0.0006 | 0.0004 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 2 | -0.0001 | -0.0006 | 0.0004 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 2 | -0.0001 | -0.0020 | 0.0017 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 2 | 0.0000 | -0.0013 | 0.0014 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0005 | -0.0005 | 0.0015 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 2 | 0.0005 | -0.0005 | 0.0015 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 2 | 0.0004 | -0.0000 | 0.0009 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 2 | 0.0000 | -0.0005 | 0.0005 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1447 | -0.2262 | -0.0631 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.1368 | -0.2146 | -0.0590 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 2 | -0.0078 | -0.0116 | -0.0041 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | -0.1264 | -0.1584 | -0.0944 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.0104 | -0.0563 | 0.0354 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | -0.1325 | -0.1589 | -0.1061 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.0122 | -0.0673 | 0.0430 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.1415 | -0.2283 | -0.0548 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.1368 | -0.2146 | -0.0590 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 2 | -0.0047 | -0.0137 | 0.0043 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | -0.1264 | -0.1584 | -0.0944 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.0104 | -0.0563 | 0.0354 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | -0.1292 | -0.1606 | -0.0979 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0123 | -0.0678 | 0.0431 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0308 | -0.1199 | 0.0582 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.0169 | -0.0895 | 0.0556 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 2 | -0.0139 | -0.0304 | 0.0026 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | -0.0155 | -0.0579 | 0.0268 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.0014 | -0.0316 | 0.0288 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | -0.0284 | -0.0764 | 0.0196 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.0024 | -0.0435 | 0.0386 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0304 | -0.1197 | 0.0590 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.0169 | -0.0895 | 0.0556 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 2 | -0.0134 | -0.0302 | 0.0034 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | -0.0155 | -0.0579 | 0.0268 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.0014 | -0.0316 | 0.0288 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | -0.0279 | -0.0773 | 0.0215 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0025 | -0.0425 | 0.0375 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1447 | -0.2438 | -0.0457 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.1368 | -0.2146 | -0.0590 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 2 | -0.0079 | -0.0292 | 0.0133 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | -0.1264 | -0.1584 | -0.0944 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.0104 | -0.0563 | 0.0354 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | -0.1347 | -0.1599 | -0.1095 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.0101 | -0.0839 | 0.0638 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.1412 | -0.2452 | -0.0372 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.1368 | -0.2146 | -0.0590 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 2 | -0.0044 | -0.0306 | 0.0218 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | -0.1264 | -0.1584 | -0.0944 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.0104 | -0.0563 | 0.0354 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | -0.1311 | -0.1614 | -0.1008 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0101 | -0.0838 | 0.0636 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0312 | -0.1324 | 0.0700 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 2 | -0.0169 | -0.0895 | 0.0556 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 2 | -0.0143 | -0.0429 | 0.0143 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 2 | -0.0155 | -0.0579 | 0.0268 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 2 | -0.0014 | -0.0316 | 0.0288 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 2 | -0.0301 | -0.0814 | 0.0212 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 2 | -0.0011 | -0.0510 | 0.0488 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0306 | -0.1313 | 0.0700 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 2 | -0.0169 | -0.0895 | 0.0556 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 2 | -0.0137 | -0.0418 | 0.0144 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 2 | -0.0155 | -0.0579 | 0.0268 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 2 | -0.0014 | -0.0316 | 0.0288 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 2 | -0.0295 | -0.0822 | 0.0231 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 2 | -0.0011 | -0.0491 | 0.0468 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.0023 | -0.0005 | 0.0052 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | 0.0023 | -0.0005 | 0.0052 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | -0.0000 | -0.0000 | -0.0000 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0017 | 0.0001 | 0.0034 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0006 | -0.0039 | 0.0051 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | -0.0039 | -0.0053 | -0.0025 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | -0.0039 | -0.0053 | -0.0025 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | -0.0000 | -0.0000 | -0.0000 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | -0.0036 | -0.0059 | -0.0012 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | -0.0004 | -0.0013 | 0.0006 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | -0.0002 | -0.0003 | -0.0001 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | -0.0002 | -0.0003 | -0.0001 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | -0.0002 | -0.0002 | -0.0001 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | -0.0001 | -0.0003 | 0.0001 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | -0.0001 | -0.0146 | 0.0144 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | -0.0001 | -0.0146 | 0.0144 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | -0.0000 | -0.0000 | -0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | -0.0019 | -0.0029 | -0.0008 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0018 | -0.0117 | 0.0152 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.1123 | 0.1101 | 0.1145 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_loss_decrease | 2 | 0.1199 | 0.1147 | 0.1251 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | local_improvement_increase | 2 | -0.0076 | -0.0151 | -0.0002 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.1109 | 0.1005 | 0.1213 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_within_group_decrease | 2 | 0.0090 | -0.0066 | 0.0246 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.1029 | 0.0809 | 0.1249 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_within_group_decrease | 2 | 0.0094 | -0.0104 | 0.0292 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 2 | 0.0019 | -0.0006 | 0.0044 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 2 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 2 | 0.0019 | -0.0006 | 0.0044 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 2 | 0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 2 | -0.0000 | -0.0000 | -0.0000 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 2 | 0.0020 | -0.0012 | 0.0052 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 2 | -0.0001 | -0.0008 | 0.0007 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_update_loss_decrease | 2 | -0.0032 | -0.0313 | 0.0250 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | local_improvement_increase | 2 | -0.0032 | -0.0313 | 0.0250 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_group_mass_decrease | 2 | -0.0010 | -0.0059 | 0.0039 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_within_group_decrease | 2 | -0.0021 | -0.0254 | 0.0211 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_update_loss_decrease | 2 | -0.8533 | -0.8825 | -0.8242 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_loss_decrease | 2 | -0.8495 | -0.8897 | -0.8093 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | local_improvement_increase | 2 | -0.0038 | -0.0149 | 0.0072 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_group_mass_decrease | 2 | -0.8213 | -0.8271 | -0.8156 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_within_group_decrease | 2 | -0.0281 | -0.0741 | 0.0178 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_group_mass_decrease | 2 | -0.8251 | -0.8458 | -0.8045 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_within_group_decrease | 2 | -0.0282 | -0.0780 | 0.0216 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_update_loss_decrease | 2 | 0.0022 | 0.0020 | 0.0024 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_loss_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | local_improvement_increase | 2 | 0.0022 | 0.0020 | 0.0024 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_within_group_decrease | 2 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_group_mass_decrease | 2 | 0.0019 | 0.0019 | 0.0020 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_within_group_decrease | 2 | 0.0002 | -0.0000 | 0.0005 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_update_loss_decrease | 2 | -0.0869 | -0.1809 | 0.0071 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_loss_decrease | 2 | -0.0769 | -0.1521 | -0.0017 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | local_improvement_increase | 2 | -0.0100 | -0.0288 | 0.0088 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_group_mass_decrease | 2 | -0.0710 | -0.1081 | -0.0338 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_within_group_decrease | 2 | -0.0059 | -0.0440 | 0.0321 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_group_mass_decrease | 2 | -0.0804 | -0.1198 | -0.0411 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_within_group_decrease | 2 | -0.0065 | -0.0611 | 0.0482 |


| seed | order | allocation_disagreements | private_spawn_steps | head_only_spawn_steps | private_learning_updates | head_only_learning_updates |
| --- | --- | --- | --- | --- | --- | --- |
| 2027 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2027 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2028 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2029 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2030 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2030 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2031 | canonical | 0 | [18, 50] | [18, 50] | 80 | 80 |
| 2031 | b_first | 0 | [18, 50] | [18, 50] | 80 | 80 |


## Methodological checks and limits

The shared-head, component, head-only, stream-order, MultiNLI data, fixed-memory and scoring integrity tests passed in the live environment. Original BANKING/Amazon Day-4 routing was reproduced with zero disagreements. Complete shadow transactions were checked against exact parameter, optimizer, RNG and reservoir restoration in their declared test scope. Legacy private probes clear stale gradients; the next real training update clears them anyway. Do not claim that all legacy probes restore gradient flags.

The frozen retention rule is harm_LCB <= 0 with z=1.96. It permits small positive mean harm on some Amazon probes and is not a 95% no-forgetting guarantee or an anytime-valid repeated-test procedure. No threshold has been retuned to fix that interpretation. Day-2 strict robustness failure and Day-4 v0 starvation remain recorded failures.

Official tests were not used in these live experiments. Earlier BANKING exploratory work did use official test data before the clean development protocol; disclose this history in the paper. Do not describe BANKING official test as never observed. MultiNLI official validation remains unused.

The normalized-text and token-truncation audit is an additional offline diagnostic of the existing split. If it finds overlap, retain these original results and declare a grouped split as a new protocol rather than silently filtering an outcome-selected subset.

| regime | seed | normalized_train_dev_unique_overlap | truncated_token_train_dev_unique_overlap | training_fraction_over_64_tokens | development_fraction_over_64_tokens |
| --- | --- | --- | --- | --- | --- |
| banking | 2026 | 0 | 0 | 0.0000 | 0.0011 |
| banking | 2027 | 0 | 0 | 0.0016 | 0.0011 |
| banking | 2028 | 0 | 0 | 0.0000 | 0.0011 |
| banking | 2029 | 0 | 0 | 0.0008 | 0.0011 |
| banking | 2030 | 0 | 0 | 0.0000 | 0.0011 |
| banking | 2031 | 0 | 0 | 0.0008 | 0.0011 |
| amazon | 2026 | 0 | 0 | 0.1609 | 0.1589 |
| amazon | 2027 | 0 | 0 | 0.1453 | 0.1589 |
| amazon | 2028 | 0 | 0 | 0.1688 | 0.1589 |
| amazon | 2029 | 0 | 0 | 0.1570 | 0.1589 |
| amazon | 2030 | 0 | 0 | 0.1812 | 0.1589 |
| amazon | 2031 | 0 | 0 | 0.1602 | 0.1589 |
| multinli | 2026 | 0 | 0 | 0.0674 | 0.0903 |
| multinli | 2027 | 0 | 0 | 0.0674 | 0.0903 |
| multinli | 2028 | 0 | 0 | 0.0597 | 0.0903 |


## Reproduction and preservation

The working branch is day5-causal-audit; master remains the restored Day-4 reference. All live trajectories record source hashes, package versions, stream hashes and saved final learner state. The older model-revision field is null; exact historical backbone identity was not recorded. The restart records an explicit Hugging Face commit and backbone file hashes, and verifies saved aggregate predictions and losses before new outcomes. This numerical reload check does not prove historical byte identity. The saved GitHub snapshot and all 738 checkpoint files were successfully restored on the new pod; notes/github_save_verification.json records the earlier authenticated save. Source-only archives and Git bundles omit LFS tensor content. New work requires its own successful GitHub save before pod shutdown.

To recover committed history from the final bundle:

```bash
git clone mitosis-research-final.bundle mitosis-interference
cd mitosis-interference
git checkout day5-causal-audit
export PYTHONPATH="$PWD"
```

Regenerate analyses with the corresponding experiments.day5_report, day6_diagnostic_report, day7_multinli_report, day9_routing_report, day8_fixed_memory_report, day10_mechanism_report, day12_capacity_report, day13_evidence_audit and day13_progress_report modules. Scientific plots are generated by experiments.day13_evidence_figures. Do not rerun existing output directories.

## Remaining research schedule

1. Complete the frozen controls and independently inspect data/implementation audits.
2. Reproduce the closest CABLE signal and at least one modern structural method from verified author code; keep task-boundary-informed conditions separate.
3. Run longer same-label adaptation regimes with useful fixed-baseline learning; freeze router and resource protocol before new confirmation seeds.
4. Separate head-weight reset from moment reset and test an intervention whose structural interpretation matches its claimed capacity resource.
5. Only after complete-method freeze, run held-out evaluation with the earlier BANKING exposure disclosed, dedicated resource measurement and external baselines.
6. Write a claim-supported paper and author verification record. The fifteen-day plan is a planning budget, not a reason to submit unsupported findings.

## Day-5 tracker

Causal audit: complete. Core LoRA-specific allocation claim: not established. Seed/order diagnosis: complete. Third-regime stress test: complete but low learning. Further controls: coverage table above. Modern baselines, complete-method confirmation and submission readiness: pending.
