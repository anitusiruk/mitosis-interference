# Fixed-total-memory sensitivity results

Each growing pool is restricted to 512 total reservoir items, with fixed 64-item probes and at most eight adapters. Reservoirs still protect and route; training uses incoming batches only. This controls training-text memory, not model parameter storage or inference compute. All comparisons use identical seed/order streams.

Completed trajectories 12/44. Incomplete folders: [].

## Fixed minus per-adapter accuracy

| regime | architecture | rule | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | head_only | frozen_centroid | 1 | 0.0000 | nan | nan |
| amazon | head_only | last_active | 1 | 0.0000 | nan | nan |
| amazon | head_only | uniform_probability | 1 | 0.0000 | nan | nan |
| amazon | private | frozen_centroid | 1 | 0.0000 | nan | nan |
| amazon | private | last_active | 1 | 0.0000 | nan | nan |
| amazon | private | uniform_probability | 1 | 0.0000 | nan | nan |
| banking | head_only | frozen_centroid | 1 | 0.0022 | nan | nan |
| banking | head_only | last_active | 1 | 0.0000 | nan | nan |
| banking | head_only | uniform_probability | 1 | 0.0000 | nan | nan |
| banking | private | frozen_centroid | 1 | 0.0059 | nan | nan |
| banking | private | last_active | 1 | 0.0000 | nan | nan |
| banking | private | uniform_probability | 1 | 0.0000 | nan | nan |

Descriptive intervals average both paired orders within a seed and use at most five independent seed clusters. Seed 2026 remains a development pilot.

## Every run

| regime | architecture | seed | order | rule | fixed_macro_accuracy | per_adapter_macro_accuracy | fixed_minus_per_adapter | updates | adapters | maximum_stored_memory | final_stored_memory | final_allocated_slots | live_training_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | head_only | 2026 | canonical | frozen_centroid | 0.8255 | 0.8255 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 30.8996 |
| amazon | head_only | 2026 | canonical | last_active | 0.8255 | 0.8255 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 30.8996 |
| amazon | head_only | 2026 | canonical | uniform_probability | 0.8255 | 0.8255 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 30.8996 |
| amazon | head_only | 2027 | b_first | frozen_centroid | 0.8307 | 0.8307 | 0.0000 | 73 | 1 | 512 | 512 | 512 | 28.1470 |
| amazon | head_only | 2027 | b_first | last_active | 0.8307 | 0.8307 | 0.0000 | 73 | 1 | 512 | 512 | 512 | 28.1470 |
| amazon | head_only | 2027 | b_first | uniform_probability | 0.8307 | 0.8307 | 0.0000 | 73 | 1 | 512 | 512 | 512 | 28.1470 |
| amazon | head_only | 2027 | canonical | frozen_centroid | 0.7943 | 0.7943 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 30.1285 |
| amazon | head_only | 2027 | canonical | last_active | 0.7943 | 0.7943 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 30.1285 |
| amazon | head_only | 2027 | canonical | uniform_probability | 0.7943 | 0.7943 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 30.1285 |
| amazon | private | 2026 | canonical | frozen_centroid | 0.8542 | 0.8542 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 34.5489 |
| amazon | private | 2026 | canonical | last_active | 0.8542 | 0.8542 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 34.5489 |
| amazon | private | 2026 | canonical | uniform_probability | 0.8542 | 0.8542 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 34.5489 |
| amazon | private | 2027 | b_first | frozen_centroid | 0.8594 | 0.8594 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 33.6693 |
| amazon | private | 2027 | b_first | last_active | 0.8594 | 0.8594 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 33.6693 |
| amazon | private | 2027 | b_first | uniform_probability | 0.8594 | 0.8594 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 33.6693 |
| amazon | private | 2027 | canonical | frozen_centroid | 0.8516 | 0.8516 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 34.3590 |
| amazon | private | 2027 | canonical | last_active | 0.8516 | 0.8516 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 34.3590 |
| amazon | private | 2027 | canonical | uniform_probability | 0.8516 | 0.8516 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 34.3590 |
| banking | head_only | 2026 | canonical | frozen_centroid | 0.1180 | 0.1246 | -0.0066 | 80 | 3 | 510 | 510 | 510 | 43.3272 |
| banking | head_only | 2026 | canonical | last_active | 0.0774 | 0.0774 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.3272 |
| banking | head_only | 2026 | canonical | uniform_probability | 0.0712 | 0.0712 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.3272 |
| banking | head_only | 2027 | b_first | frozen_centroid | 0.0900 | 0.0833 | 0.0067 | 80 | 3 | 510 | 510 | 510 | 40.8229 |
| banking | head_only | 2027 | b_first | last_active | 0.0137 | 0.0137 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 40.8229 |
| banking | head_only | 2027 | b_first | uniform_probability | 0.0137 | 0.0137 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 40.8229 |
| banking | head_only | 2027 | canonical | frozen_centroid | 0.1107 | 0.1129 | -0.0022 | 80 | 3 | 510 | 510 | 510 | 42.9144 |
| banking | head_only | 2027 | canonical | last_active | 0.0978 | 0.0978 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.9144 |
| banking | head_only | 2027 | canonical | uniform_probability | 0.0137 | 0.0137 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.9144 |
| banking | private | 2026 | canonical | frozen_centroid | 0.1602 | 0.1613 | -0.0011 | 80 | 3 | 510 | 510 | 510 | 49.1548 |
| banking | private | 2026 | canonical | last_active | 0.1022 | 0.1022 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.1548 |
| banking | private | 2026 | canonical | uniform_probability | 0.1222 | 0.1222 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.1548 |
| banking | private | 2027 | b_first | frozen_centroid | 0.1532 | 0.1423 | 0.0109 | 80 | 3 | 510 | 510 | 510 | 48.7350 |
| banking | private | 2027 | b_first | last_active | 0.0641 | 0.0641 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7350 |
| banking | private | 2027 | b_first | uniform_probability | 0.0778 | 0.0778 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7350 |
| banking | private | 2027 | canonical | frozen_centroid | 0.1593 | 0.1584 | 0.0009 | 80 | 3 | 510 | 510 | 510 | 48.7821 |
| banking | private | 2027 | canonical | last_active | 0.1462 | 0.1462 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7821 |
| banking | private | 2027 | canonical | uniform_probability | 0.0860 | 0.0860 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7821 |

## Limits

Equal reservoir capacity does not make different adapter pools parameter- or compute-matched. The extension also includes a hard eight-adapter cap and stricter restoration of stale gradients/flags/modes; the no-shrink numeric-equivalence test checks that cleanup leaves action scores unchanged. This sensitivity does not constitute an untouched final evaluation or modern-baseline comparison.
