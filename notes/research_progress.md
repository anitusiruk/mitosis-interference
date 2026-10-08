# Research progress and evidence handoff

Generated 2026-10-08T03:12:21.094362+00:00. This is a development report, not a submission-ready paper.

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
| 15 | 12 | 20 | completed |
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

The fixed-memory extension limits total stored training examples to 512 and preserves 64-example probes. It also caps the pool at eight. The rank-96 single baseline was selected by parameter arithmetic near three rank-8 private packages; it is not universally parameter matched to an uncapped growing pool. Memory, head storage, optimizer state, active-update compute and inference compute remain separate resources. Poor rank-96 performance under the shared fixed recipe does not establish superiority over a tuned larger static baseline; the subsequent Day-17 equal-grid study completed 24/24 pilot and 20/20 confirmation trajectories with a rate selected per rank before fresh-seed outcomes. This addresses the declared rate grid; broader tuning and complete-method confirmation remain open.

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
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0007 | -0.0142 | 0.0155 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0007 | -0.0142 | 0.0155 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0007 | -0.0142 | 0.0155 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0072 | -0.0042 | 0.0186 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0072 | -0.0042 | 0.0186 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0072 | -0.0042 | 0.0186 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0036 | -0.0176 | 0.0104 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0036 | -0.0176 | 0.0104 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0036 | -0.0176 | 0.0104 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0065 | -0.0045 | 0.0175 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0065 | -0.0045 | 0.0175 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0065 | -0.0045 | 0.0175 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0072 | 0.0052 | 0.0092 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0072 | 0.0052 | 0.0092 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0072 | 0.0052 | 0.0092 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0012 | -0.0034 | 0.0009 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0012 | -0.0034 | 0.0009 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0012 | -0.0034 | 0.0009 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0067 | 0.0050 | 0.0085 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0067 | 0.0050 | 0.0085 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0067 | 0.0050 | 0.0085 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0013 | -0.0035 | 0.0008 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0013 | -0.0035 | 0.0008 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0013 | -0.0035 | 0.0008 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.1996 | -0.2581 | -0.1412 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0069 | 0.0034 | 0.0104 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.1996 | -0.2581 | -0.1412 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0933 | -0.1169 | -0.0696 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0012 | -0.0031 | 0.0008 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0933 | -0.1169 | -0.0696 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.2017 | -0.2557 | -0.1477 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0048 | -0.0069 | 0.0166 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.2017 | -0.2557 | -0.1477 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0951 | -0.1174 | -0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0030 | -0.0066 | 0.0006 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0951 | -0.1174 | -0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.1931 | -0.2399 | -0.1462 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0135 | -0.0009 | 0.0279 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.1931 | -0.2399 | -0.1462 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.1017 | -0.1164 | -0.0870 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0096 | -0.0211 | 0.0019 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.1017 | -0.1164 | -0.0870 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.1914 | -0.2356 | -0.1472 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0152 | -0.0085 | 0.0388 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.2066 | -0.2622 | -0.1509 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.1914 | -0.2356 | -0.1472 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.1029 | -0.1167 | -0.0891 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0108 | -0.0235 | 0.0019 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0921 | -0.1175 | -0.0667 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.1029 | -0.1167 | -0.0891 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0026 | -0.0074 | 0.0125 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0026 | -0.0074 | 0.0125 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0026 | -0.0074 | 0.0125 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0019 | 0.0002 | 0.0036 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0019 | 0.0002 | 0.0036 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0019 | 0.0002 | 0.0036 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0005 | -0.0003 | 0.0013 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0005 | -0.0003 | 0.0013 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0005 | -0.0003 | 0.0013 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0000 | -0.0000 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0000 | -0.0000 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0000 | -0.0000 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0017 | -0.0104 | 0.0071 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0017 | -0.0104 | 0.0071 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0017 | -0.0104 | 0.0071 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0012 | -0.0001 | 0.0024 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0012 | -0.0001 | 0.0024 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0012 | -0.0001 | 0.0024 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0000 | -0.0006 | 0.0006 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0000 | -0.0006 | 0.0006 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0000 | -0.0006 | 0.0006 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0000 | -0.0001 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0000 | -0.0001 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0000 | -0.0001 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1161 | -0.1595 | -0.0727 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 3 | 0.0006 | -0.0017 | 0.0029 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.1161 | -0.1595 | -0.0727 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1168 | -0.1620 | -0.0716 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0001 | -0.0085 | 0.0084 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.1168 | -0.1620 | -0.0716 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0097 | -0.0261 | 0.0066 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 3 | -0.0075 | -0.0083 | -0.0066 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.0097 | -0.0261 | 0.0066 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0102 | -0.0257 | 0.0054 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0079 | -0.0080 | -0.0078 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.0102 | -0.0257 | 0.0054 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1096 | -0.1469 | -0.0723 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 3 | 0.0072 | 0.0017 | 0.0126 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.1096 | -0.1469 | -0.0723 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1067 | -0.1460 | -0.0675 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 3 | 0.0100 | -0.0020 | 0.0219 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.1167 | -0.1580 | -0.0755 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.1067 | -0.1460 | -0.0675 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0182 | -0.0320 | -0.0045 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 3 | -0.0159 | -0.0183 | -0.0136 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.0182 | -0.0320 | -0.0045 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0182 | -0.0315 | -0.0050 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0160 | -0.0185 | -0.0134 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.0023 | -0.0177 | 0.0132 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.0182 | -0.0315 | -0.0050 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.0002 | -0.0109 | 0.0112 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | 0.0002 | -0.0109 | 0.0112 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0002 | -0.0109 | 0.0112 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | -0.0009 | -0.0064 | 0.0047 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | -0.0009 | -0.0064 | 0.0047 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | -0.0009 | -0.0064 | 0.0047 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | -0.0014 | -0.0019 | -0.0009 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | -0.0014 | -0.0019 | -0.0009 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | -0.0014 | -0.0019 | -0.0009 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.0000 | -0.0025 | 0.0025 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | 0.0000 | -0.0025 | 0.0025 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0000 | -0.0025 | 0.0025 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.0982 | 0.0517 | 0.1447 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_loss_decrease | 3 | 0.1145 | 0.0650 | 0.1639 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | local_improvement_increase | 3 | -0.0163 | -0.0224 | -0.0101 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.1145 | 0.0650 | 0.1639 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0982 | 0.0517 | 0.1447 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.0004 | -0.0034 | 0.0042 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | 0.0004 | -0.0034 | 0.0042 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0004 | -0.0034 | 0.0042 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_update_loss_decrease | 3 | 0.0028 | -0.0040 | 0.0096 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | local_improvement_increase | 3 | 0.0028 | -0.0040 | 0.0096 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_optimizer | average_over_all_other_factors | post_within_group_decrease | 3 | 0.0028 | -0.0040 | 0.0096 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_update_loss_decrease | 3 | -0.1473 | -0.1774 | -0.1173 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_loss_decrease | 3 | -0.1493 | -0.1849 | -0.1138 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | local_improvement_increase | 3 | 0.0020 | -0.0077 | 0.0116 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | initial_within_group_decrease | 3 | -0.1493 | -0.1849 | -0.1138 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_head_weights | average_over_all_other_factors | post_within_group_decrease | 3 | -0.1473 | -0.1774 | -0.1173 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_update_loss_decrease | 3 | 0.0006 | -0.0019 | 0.0030 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | local_improvement_increase | 3 | 0.0006 | -0.0019 | 0.0030 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_optimizer | average_over_all_other_factors | post_within_group_decrease | 3 | 0.0006 | -0.0019 | 0.0030 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_update_loss_decrease | 3 | -0.0632 | -0.0834 | -0.0430 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_loss_decrease | 3 | -0.0595 | -0.0784 | -0.0406 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | local_improvement_increase | 3 | -0.0037 | -0.0062 | -0.0012 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | initial_within_group_decrease | 3 | -0.0595 | -0.0784 | -0.0406 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| amazon | marginal | reset_lora_weights | average_over_all_other_factors | post_within_group_decrease | 3 | -0.0632 | -0.0834 | -0.0430 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0031 | -0.0117 | 0.0056 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0031 | -0.0117 | 0.0056 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.0006 | -0.0013 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0025 | -0.0105 | 0.0056 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0039 | -0.0081 | 0.0003 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0039 | -0.0081 | 0.0003 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.0029 | -0.0038 | -0.0020 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0010 | -0.0045 | 0.0024 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0037 | -0.0123 | 0.0050 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0037 | -0.0123 | 0.0050 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.0011 | -0.0018 | -0.0003 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0026 | -0.0107 | 0.0054 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0041 | -0.0084 | 0.0002 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0041 | -0.0084 | 0.0002 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.0030 | -0.0039 | -0.0021 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0011 | -0.0046 | 0.0024 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0017 | -0.0081 | 0.0048 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0017 | -0.0081 | 0.0048 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0007 | -0.0008 | 0.0021 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0023 | -0.0074 | 0.0027 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0022 | -0.0063 | 0.0019 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0022 | -0.0063 | 0.0019 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.0011 | -0.0021 | -0.0001 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0011 | -0.0044 | 0.0022 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0018 | -0.0081 | 0.0045 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0018 | -0.0081 | 0.0045 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0006 | -0.0009 | 0.0021 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0024 | -0.0073 | 0.0026 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0022 | -0.0063 | 0.0019 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0022 | -0.0063 | 0.0019 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.0011 | -0.0021 | -0.0001 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0011 | -0.0044 | 0.0022 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9099 | -0.9152 | -0.9046 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.9103 | -0.9194 | -0.9011 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0004 | -0.0034 | 0.0042 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | -0.8762 | -0.8794 | -0.8731 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.0340 | -0.0462 | -0.0219 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.8754 | -0.8821 | -0.8687 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0345 | -0.0465 | -0.0225 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.7981 | -0.8107 | -0.7855 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.7927 | -0.8083 | -0.7772 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0054 | -0.0083 | -0.0024 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | -0.7680 | -0.7768 | -0.7591 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0248 | -0.0336 | -0.0159 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.7736 | -0.7802 | -0.7670 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0245 | -0.0335 | -0.0154 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9125 | -0.9177 | -0.9073 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.9103 | -0.9194 | -0.9011 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0022 | -0.0062 | 0.0018 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | -0.8762 | -0.8794 | -0.8731 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.0340 | -0.0462 | -0.0219 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.8776 | -0.8847 | -0.8706 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0349 | -0.0470 | -0.0227 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.8033 | -0.8146 | -0.7919 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.7927 | -0.8083 | -0.7772 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0105 | -0.0148 | -0.0063 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | -0.7680 | -0.7768 | -0.7591 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0248 | -0.0336 | -0.0159 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.7784 | -0.7843 | -0.7726 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0248 | -0.0339 | -0.0158 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9085 | -0.9169 | -0.9000 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.9103 | -0.9194 | -0.9011 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0018 | -0.0016 | 0.0053 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | -0.8762 | -0.8794 | -0.8731 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.0340 | -0.0462 | -0.0219 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.8741 | -0.8814 | -0.8668 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0344 | -0.0499 | -0.0188 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.7964 | -0.8103 | -0.7825 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.7927 | -0.8083 | -0.7772 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0037 | -0.0053 | -0.0020 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | -0.7680 | -0.7768 | -0.7591 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0248 | -0.0336 | -0.0159 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.7719 | -0.7788 | -0.7649 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0245 | -0.0341 | -0.0150 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9106 | -0.9187 | -0.9024 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | -0.9103 | -0.9194 | -0.9011 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | local_improvement_increase | 3 | -0.0003 | -0.0030 | 0.0025 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | -0.8762 | -0.8794 | -0.8731 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | -0.0340 | -0.0462 | -0.0219 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.8760 | -0.8835 | -0.8685 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | -0.0346 | -0.0502 | -0.0190 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.8014 | -0.8141 | -0.7887 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | -0.7927 | -0.8083 | -0.7772 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | local_improvement_increase | 3 | -0.0087 | -0.0116 | -0.0058 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | -0.7680 | -0.7768 | -0.7591 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | -0.0248 | -0.0336 | -0.0159 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | -0.7765 | -0.7827 | -0.7704 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | -0.0249 | -0.0345 | -0.0152 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0027 | 0.0023 | 0.0032 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0027 | 0.0023 | 0.0032 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0022 | 0.0020 | 0.0025 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0005 | 0.0003 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0056 | 0.0043 | 0.0069 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0056 | 0.0043 | 0.0069 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0052 | 0.0038 | 0.0066 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0004 | 0.0003 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0002 | -0.0006 | 0.0009 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0002 | -0.0006 | 0.0009 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0000 | -0.0006 | 0.0006 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0001 | -0.0001 | 0.0004 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0005 | 0.0002 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0005 | 0.0002 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0004 | 0.0003 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0000 | -0.0001 | 0.0001 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0021 | 0.0017 | 0.0025 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0021 | 0.0017 | 0.0025 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_group_mass_decrease | 3 | 0.0018 | 0.0015 | 0.0021 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0003 | 0.0002 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0054 | 0.0042 | 0.0067 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0054 | 0.0042 | 0.0067 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0051 | 0.0037 | 0.0064 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0003 | 0.0002 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0001 | -0.0006 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | local_improvement_increase | 3 | 0.0001 | -0.0006 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_group_mass_decrease | 3 | -0.0001 | -0.0006 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_within_group_decrease | 3 | 0.0001 | -0.0003 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0004 | 0.0002 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | local_improvement_increase | 3 | 0.0004 | 0.0002 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_group_mass_decrease | 3 | 0.0004 | 0.0003 | 0.0005 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_within_group_decrease | 3 | 0.0000 | -0.0001 | 0.0001 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1382 | -0.1703 | -0.1061 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.1306 | -0.1614 | -0.0999 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 3 | -0.0076 | -0.0089 | -0.0063 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | -0.1207 | -0.1460 | -0.0954 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.0099 | -0.0192 | -0.0007 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | -0.1266 | -0.1525 | -0.1007 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.0116 | -0.0227 | -0.0006 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1353 | -0.1670 | -0.1037 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.1306 | -0.1614 | -0.0999 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0047 | -0.0065 | -0.0030 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | -0.1207 | -0.1460 | -0.0954 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.0099 | -0.0192 | -0.0007 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | -0.1236 | -0.1485 | -0.0987 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.0117 | -0.0229 | -0.0006 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0264 | -0.0522 | -0.0006 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.0131 | -0.0350 | 0.0089 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 3 | -0.0133 | -0.0173 | -0.0094 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | -0.0124 | -0.0281 | 0.0032 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.0006 | -0.0075 | 0.0062 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | -0.0248 | -0.0429 | -0.0068 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.0016 | -0.0104 | 0.0072 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0261 | -0.0514 | -0.0009 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.0131 | -0.0350 | 0.0089 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0131 | -0.0167 | -0.0094 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | -0.0124 | -0.0281 | 0.0032 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.0006 | -0.0075 | 0.0062 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | -0.0244 | -0.0422 | -0.0067 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.0017 | -0.0102 | 0.0068 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1390 | -0.1703 | -0.1077 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.1306 | -0.1614 | -0.0999 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | local_improvement_increase | 3 | -0.0084 | -0.0131 | -0.0037 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | -0.1207 | -0.1460 | -0.0954 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.0099 | -0.0192 | -0.0007 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | -0.1288 | -0.1544 | -0.1032 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.0102 | -0.0246 | 0.0043 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1357 | -0.1669 | -0.1046 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.1306 | -0.1614 | -0.0999 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0051 | -0.0111 | 0.0009 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | -0.1207 | -0.1460 | -0.0954 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.0099 | -0.0192 | -0.0007 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | -0.1256 | -0.1502 | -0.1009 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.0102 | -0.0246 | 0.0042 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0270 | -0.0539 | -0.0000 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_loss_decrease | 3 | -0.0131 | -0.0350 | 0.0089 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | local_improvement_increase | 3 | -0.0139 | -0.0197 | -0.0081 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_group_mass_decrease | 3 | -0.0124 | -0.0281 | 0.0032 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | initial_within_group_decrease | 3 | -0.0006 | -0.0075 | 0.0062 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_group_mass_decrease | 3 | -0.0266 | -0.0447 | -0.0085 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_within_group_decrease | 3 | -0.0004 | -0.0106 | 0.0099 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0266 | -0.0529 | -0.0003 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_loss_decrease | 3 | -0.0131 | -0.0350 | 0.0089 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | local_improvement_increase | 3 | -0.0135 | -0.0191 | -0.0080 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_group_mass_decrease | 3 | -0.0124 | -0.0281 | 0.0032 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | initial_within_group_decrease | 3 | -0.0006 | -0.0075 | 0.0062 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_group_mass_decrease | 3 | -0.0261 | -0.0440 | -0.0083 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_within_group_decrease | 3 | -0.0005 | -0.0103 | 0.0094 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.0017 | -0.0010 | 0.0045 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | -0.0000 | -0.0000 | -0.0000 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | 0.0017 | -0.0010 | 0.0045 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0016 | 0.0012 | 0.0021 |
| banking | interaction | reset_head_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0001 | -0.0024 | 0.0026 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | -0.0037 | -0.0046 | -0.0028 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | -0.0000 | -0.0000 | -0.0000 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | -0.0037 | -0.0046 | -0.0028 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | -0.0034 | -0.0043 | -0.0025 |
| banking | interaction | reset_head_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | -0.0003 | -0.0006 | -0.0001 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | -0.0002 | -0.0002 | -0.0002 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | -0.0002 | -0.0002 | -0.0002 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | -0.0002 | -0.0002 | -0.0001 |
| banking | interaction | reset_lora_optimizer x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | -0.0001 | -0.0001 | -0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | -0.0006 | -0.0040 | 0.0029 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | -0.0006 | -0.0040 | 0.0029 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | -0.0019 | -0.0023 | -0.0016 |
| banking | interaction | reset_lora_weights x reset_head_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0014 | -0.0018 | 0.0045 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.1106 | 0.1031 | 0.1180 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_loss_decrease | 3 | 0.1176 | 0.1075 | 0.1276 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | local_improvement_increase | 3 | -0.0070 | -0.0100 | -0.0040 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.1083 | 0.0969 | 0.1197 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | initial_within_group_decrease | 3 | 0.0093 | 0.0060 | 0.0126 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.1007 | 0.0901 | 0.1112 |
| banking | interaction | reset_lora_weights x reset_head_weights | marginal_over_other_factors | post_within_group_decrease | 3 | 0.0099 | 0.0054 | 0.0144 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_update_loss_decrease | 3 | 0.0017 | 0.0007 | 0.0028 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_loss_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | local_improvement_increase | 3 | 0.0017 | 0.0007 | 0.0028 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_group_mass_decrease | 3 | 0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | initial_within_group_decrease | 3 | -0.0000 | -0.0000 | 0.0000 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_group_mass_decrease | 3 | 0.0018 | 0.0007 | 0.0028 |
| banking | interaction | reset_lora_weights x reset_lora_optimizer | marginal_over_other_factors | post_within_group_decrease | 3 | -0.0001 | -0.0002 | 0.0001 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_update_loss_decrease | 3 | -0.0028 | -0.0085 | 0.0029 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | local_improvement_increase | 3 | -0.0028 | -0.0085 | 0.0029 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_group_mass_decrease | 3 | -0.0011 | -0.0021 | -0.0001 |
| banking | marginal | reset_head_optimizer | average_over_all_other_factors | post_within_group_decrease | 3 | -0.0018 | -0.0066 | 0.0031 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_update_loss_decrease | 3 | -0.8551 | -0.8645 | -0.8457 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_loss_decrease | 3 | -0.8515 | -0.8632 | -0.8398 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | local_improvement_increase | 3 | -0.0036 | -0.0060 | -0.0011 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_group_mass_decrease | 3 | -0.8221 | -0.8255 | -0.8187 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | initial_within_group_decrease | 3 | -0.0294 | -0.0399 | -0.0189 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_group_mass_decrease | 3 | -0.8254 | -0.8297 | -0.8212 |
| banking | marginal | reset_head_weights | average_over_all_other_factors | post_within_group_decrease | 3 | -0.0296 | -0.0412 | -0.0181 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_update_loss_decrease | 3 | 0.0021 | 0.0020 | 0.0023 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_loss_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | local_improvement_increase | 3 | 0.0021 | 0.0020 | 0.0023 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_group_mass_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | initial_within_group_decrease | 3 | 0.0000 | 0.0000 | 0.0000 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_group_mass_decrease | 3 | 0.0019 | 0.0017 | 0.0021 |
| banking | marginal | reset_lora_optimizer | average_over_all_other_factors | post_within_group_decrease | 3 | 0.0002 | 0.0002 | 0.0003 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_update_loss_decrease | 3 | -0.0818 | -0.1104 | -0.0532 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_loss_decrease | 3 | -0.0718 | -0.0981 | -0.0456 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | local_improvement_increase | 3 | -0.0100 | -0.0136 | -0.0063 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_group_mass_decrease | 3 | -0.0666 | -0.0868 | -0.0463 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | initial_within_group_decrease | 3 | -0.0053 | -0.0132 | 0.0027 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_group_mass_decrease | 3 | -0.0758 | -0.0971 | -0.0546 |
| banking | marginal | reset_lora_weights | average_over_all_other_factors | post_within_group_decrease | 3 | -0.0060 | -0.0169 | 0.0049 |


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

The working branch is day5-causal-audit; master remains the restored Day-4 reference. All live trajectories record source hashes, package versions, stream hashes and saved final learner state. The older model-revision field is null; exact historical backbone identity was not recorded. The restart records an explicit Hugging Face commit and backbone file hashes, and verifies saved aggregate predictions and losses before new outcomes. This numerical reload check does not prove historical byte identity. The October 8 restart SHA256-verified 580 unique LFS objects, 783 LFS working files and all 1566 checkpoint-manifest files before the bounded continuation. notes/day21_restore_integrity.json records that restoration; the current snapshot requires its own day21_github_save_verification.json receipt. Source-only archives and Git bundles omit LFS tensor content. New work requires its own successful GitHub save before pod shutdown.

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
4. Finish the remaining eight original weight/state factorial cells and test an intervention whose structural interpretation matches its claimed capacity resource.
5. Only after complete-method freeze, run held-out evaluation with the earlier BANKING exposure disclosed, dedicated resource measurement and external baselines.
6. Write a claim-supported paper and author verification record. The fifteen-day plan is a planning budget, not a reason to submit unsupported findings.

## Day-5 tracker

Causal audit: complete. Core LoRA-specific allocation claim: not established. Seed/order diagnosis: complete. Third-regime stress test: complete but low learning. Further controls: coverage table above. Modern baselines, complete-method confirmation and submission readiness: pending.


## October 8 bounded continuation

The original factorial queue now has 12/20 independently verified trajectories and three paired training seeds in each regime. Two additional original seed-2029 B-first cells passed exact replay gates; no contrast was changed. `notes/day21_factorial_integrity.json` checks every mature batch and all cells. The auxiliary Online-LoRA CPU source diagnostic does not reproduce its image benchmark. Close 2026 prior work and remaining gaps are in `notes/day21_novelty_and_next_evidence.md`. Final test evaluation remains untouched.
