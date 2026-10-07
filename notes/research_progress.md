# Research progress and evidence handoff

Generated 2026-10-07T02:01:15.507410+00:00. This is a development report, not a submission-ready paper.

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
| 15 | 6 | 20 | completed |
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
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0062 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0062 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0062 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0025 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0025 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0025 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0100 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0100 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0100 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0018 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0018 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0018 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0072 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0072 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0072 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0022 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0022 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0022 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0066 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0066 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0066 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0023 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0023 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0023 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.2184 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0068 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.2184 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1038 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0005 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.1038 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.2156 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0095 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.2156 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1052 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0019 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.1052 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.2049 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0202 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.2049 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1085 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0052 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.1085 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.1990 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0261 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.2251 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.1990 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1093 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0060 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.1033 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.1093 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0019 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0019 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0019 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0014 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0014 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0014 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0057 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0057 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0057 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0003 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0003 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0003 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1172 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 1 | 0.0002 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.1172 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1139 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 1 | 0.0035 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.1139 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0026 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 1 | -0.0070 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.0026 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0034 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 1 | -0.0079 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.0034 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1085 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 1 | 0.0089 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.1085 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1021 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 1 | 0.0153 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | -0.1174 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.1021 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0121 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 1 | -0.0165 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.0121 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0124 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 1 | -0.0168 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | 0.0044 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.0124 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.0053 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | 0.0053 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0053 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.0016 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | 0.0016 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0016 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | -0.0013 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | -0.0013 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | -0.0013 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.0005 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | 0.0005 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0005 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.1028 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_loss_decrease | 1 | 0.1218 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | local_improvement_increase | 1 | -0.0190 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.1218 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_within_group_decrease | 1 | 0.1028 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.0022 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | 0.0022 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0022 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.0003 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | local_improvement_increase | 1 | -0.0003 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_within_group_decrease | 1 | -0.0003 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.1581 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_loss_decrease | 1 | -0.1642 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | local_improvement_increase | 1 | 0.0061 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_within_group_decrease | 1 | -0.1642 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_within_group_decrease | 1 | -0.1581 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.0005 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | local_improvement_increase | 1 | -0.0005 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_within_group_decrease | 1 | -0.0005 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.0590 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_loss_decrease | 1 | -0.0565 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | local_improvement_increase | 1 | -0.0025 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_within_group_decrease | 1 | -0.0565 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_within_group_decrease | 1 | -0.0590 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0011 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0011 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | -0.0004 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0007 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0025 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0025 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.0025 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0001 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0017 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0017 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | -0.0008 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0009 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0027 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0027 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.0026 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0001 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0008 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0008 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0013 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.0007 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0002 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0007 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0007 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0012 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0006 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.0007 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9113 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.9128 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0015 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | -0.8759 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.0369 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | -0.8739 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0374 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.7981 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.7925 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0056 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | -0.7659 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.0266 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.7715 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0266 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9142 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.9128 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0014 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | -0.8759 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.0369 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | -0.8762 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0380 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.8032 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.7925 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0107 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | -0.7659 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.0266 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.7762 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0269 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9094 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.9128 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0034 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | -0.8759 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.0369 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | -0.8722 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0372 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.7961 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.7925 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0036 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | -0.7659 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.0266 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.7697 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0263 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9118 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | -0.9128 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0010 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | -0.8759 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | -0.0369 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | -0.8742 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0377 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.8010 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | -0.7925 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 1 | -0.0085 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | -0.7659 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | -0.0266 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | -0.7743 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | -0.0267 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0029 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0029 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0023 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0006 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0056 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0056 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0052 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0004 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0006 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0006 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0005 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0023 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 1 | 0.0023 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0019 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 1 | 0.0004 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0055 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0055 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0051 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0004 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 1 | -0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 1 | -0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0005 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 1 | 0.0005 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 1 | 0.0005 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1511 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | -0.1430 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 1 | -0.0081 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | -0.1289 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | -0.0140 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | -0.1346 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.0165 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1484 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | -0.1430 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 1 | -0.0054 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | -0.1289 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | -0.0140 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | -0.1317 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.0167 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0378 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | -0.0227 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 1 | -0.0152 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | -0.0189 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | -0.0038 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | -0.0322 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.0057 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0374 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | -0.0227 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 1 | -0.0147 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | -0.0189 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | -0.0038 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | -0.0318 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.0056 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1525 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | -0.1430 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 1 | -0.0096 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | -0.1289 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | -0.0140 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | -0.1367 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.0159 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1494 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | -0.1430 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 1 | -0.0064 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | -0.1289 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | -0.0140 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | -0.1335 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.0159 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0392 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 1 | -0.0227 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 1 | -0.0165 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 1 | -0.0189 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 1 | -0.0038 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 1 | -0.0341 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 1 | -0.0050 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0386 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 1 | -0.0227 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 1 | -0.0159 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 1 | -0.0189 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 1 | -0.0038 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 1 | -0.0337 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 1 | -0.0049 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.0021 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | 0.0021 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0019 | nan | nan |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0003 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | -0.0038 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | -0.0038 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | -0.0034 | nan | nan |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | -0.0004 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | -0.0002 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | -0.0002 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | -0.0001 | nan | nan |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | -0.0001 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | -0.0012 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | -0.0012 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | -0.0019 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0007 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.1121 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_loss_decrease | 1 | 0.1203 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | local_improvement_increase | 1 | -0.0082 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.1101 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_within_group_decrease | 1 | 0.0102 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.1012 | nan | nan |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0109 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 1 | 0.0017 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 1 | 0.0017 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 1 | -0.0000 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 1 | 0.0017 | nan | nan |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.0009 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | local_improvement_increase | 1 | -0.0009 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_group_mass_decrease | 1 | -0.0006 | nan | nan |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_within_group_decrease | 1 | -0.0003 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.8556 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_loss_decrease | 1 | -0.8527 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | local_improvement_increase | 1 | -0.0030 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_group_mass_decrease | 1 | -0.8209 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_within_group_decrease | 1 | -0.0318 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_group_mass_decrease | 1 | -0.8235 | nan | nan |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_within_group_decrease | 1 | -0.0321 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_update_loss_decrease | 1 | 0.0022 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_loss_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | local_improvement_increase | 1 | 0.0022 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_within_group_decrease | 1 | 0.0000 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_group_mass_decrease | 1 | 0.0019 | nan | nan |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_within_group_decrease | 1 | 0.0002 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_update_loss_decrease | 1 | -0.0943 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_loss_decrease | 1 | -0.0828 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | local_improvement_increase | 1 | -0.0115 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_group_mass_decrease | 1 | -0.0739 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_within_group_decrease | 1 | -0.0089 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_group_mass_decrease | 1 | -0.0835 | nan | nan |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_within_group_decrease | 1 | -0.0108 | nan | nan |


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
