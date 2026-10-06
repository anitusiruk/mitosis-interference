# Fixed-total-memory sensitivity results

Each growing pool is restricted to 512 total reservoir items, with fixed 64-item probes and at most eight adapters. Reservoirs still protect and route; training uses incoming batches only. This controls training-text memory, not model parameter storage or inference compute. All comparisons use identical seed/order streams.

Completed trajectories 44/44. Incomplete folders: [].

## Fixed minus per-adapter accuracy

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
| amazon | head_only | 2028 | b_first | frozen_centroid | 0.8099 | 0.8099 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 29.7731 |
| amazon | head_only | 2028 | b_first | last_active | 0.8099 | 0.8099 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 29.7731 |
| amazon | head_only | 2028 | b_first | uniform_probability | 0.8099 | 0.8099 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 29.7731 |
| amazon | head_only | 2028 | canonical | frozen_centroid | 0.7995 | 0.7995 | 0.0000 | 66 | 1 | 512 | 512 | 512 | 29.0706 |
| amazon | head_only | 2028 | canonical | last_active | 0.7995 | 0.7995 | 0.0000 | 66 | 1 | 512 | 512 | 512 | 29.0706 |
| amazon | head_only | 2028 | canonical | uniform_probability | 0.7995 | 0.7995 | 0.0000 | 66 | 1 | 512 | 512 | 512 | 29.0706 |
| amazon | head_only | 2029 | b_first | frozen_centroid | 0.8099 | 0.8099 | 0.0000 | 73 | 1 | 512 | 512 | 512 | 29.3512 |
| amazon | head_only | 2029 | b_first | last_active | 0.8099 | 0.8099 | 0.0000 | 73 | 1 | 512 | 512 | 512 | 29.3512 |
| amazon | head_only | 2029 | b_first | uniform_probability | 0.8099 | 0.8099 | 0.0000 | 73 | 1 | 512 | 512 | 512 | 29.3512 |
| amazon | head_only | 2029 | canonical | frozen_centroid | 0.7812 | 0.7812 | 0.0000 | 63 | 1 | 512 | 512 | 512 | 28.8621 |
| amazon | head_only | 2029 | canonical | last_active | 0.7812 | 0.7812 | 0.0000 | 63 | 1 | 512 | 512 | 512 | 28.8621 |
| amazon | head_only | 2029 | canonical | uniform_probability | 0.7812 | 0.7812 | 0.0000 | 63 | 1 | 512 | 512 | 512 | 28.8621 |
| amazon | head_only | 2030 | b_first | frozen_centroid | 0.8047 | 0.8047 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 32.6612 |
| amazon | head_only | 2030 | b_first | last_active | 0.8047 | 0.8047 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 32.6612 |
| amazon | head_only | 2030 | b_first | uniform_probability | 0.8047 | 0.8047 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 32.6612 |
| amazon | head_only | 2030 | canonical | frozen_centroid | 0.8021 | 0.8021 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 29.6436 |
| amazon | head_only | 2030 | canonical | last_active | 0.8021 | 0.8021 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 29.6436 |
| amazon | head_only | 2030 | canonical | uniform_probability | 0.8021 | 0.8021 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 29.6436 |
| amazon | head_only | 2031 | b_first | frozen_centroid | 0.8125 | 0.8125 | 0.0000 | 63 | 1 | 512 | 512 | 512 | 28.9279 |
| amazon | head_only | 2031 | b_first | last_active | 0.8125 | 0.8125 | 0.0000 | 63 | 1 | 512 | 512 | 512 | 28.9279 |
| amazon | head_only | 2031 | b_first | uniform_probability | 0.8125 | 0.8125 | 0.0000 | 63 | 1 | 512 | 512 | 512 | 28.9279 |
| amazon | head_only | 2031 | canonical | frozen_centroid | 0.7969 | 0.7969 | 0.0000 | 78 | 1 | 512 | 512 | 512 | 32.2897 |
| amazon | head_only | 2031 | canonical | last_active | 0.7969 | 0.7969 | 0.0000 | 78 | 1 | 512 | 512 | 512 | 32.2897 |
| amazon | head_only | 2031 | canonical | uniform_probability | 0.7969 | 0.7969 | 0.0000 | 78 | 1 | 512 | 512 | 512 | 32.2897 |
| amazon | private | 2026 | canonical | frozen_centroid | 0.8542 | 0.8542 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 34.5489 |
| amazon | private | 2026 | canonical | last_active | 0.8542 | 0.8542 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 34.5489 |
| amazon | private | 2026 | canonical | uniform_probability | 0.8542 | 0.8542 | 0.0000 | 79 | 1 | 512 | 512 | 512 | 34.5489 |
| amazon | private | 2027 | b_first | frozen_centroid | 0.8594 | 0.8594 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 33.6693 |
| amazon | private | 2027 | b_first | last_active | 0.8594 | 0.8594 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 33.6693 |
| amazon | private | 2027 | b_first | uniform_probability | 0.8594 | 0.8594 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 33.6693 |
| amazon | private | 2027 | canonical | frozen_centroid | 0.8516 | 0.8516 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 34.3590 |
| amazon | private | 2027 | canonical | last_active | 0.8516 | 0.8516 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 34.3590 |
| amazon | private | 2027 | canonical | uniform_probability | 0.8516 | 0.8516 | 0.0000 | 72 | 1 | 512 | 512 | 512 | 34.3590 |
| amazon | private | 2028 | b_first | frozen_centroid | 0.8385 | 0.8385 | 0.0000 | 69 | 1 | 512 | 512 | 512 | 34.0634 |
| amazon | private | 2028 | b_first | last_active | 0.8385 | 0.8385 | 0.0000 | 69 | 1 | 512 | 512 | 512 | 34.0634 |
| amazon | private | 2028 | b_first | uniform_probability | 0.8385 | 0.8385 | 0.0000 | 69 | 1 | 512 | 512 | 512 | 34.0634 |
| amazon | private | 2028 | canonical | frozen_centroid | 0.8333 | 0.8333 | 0.0000 | 57 | 1 | 512 | 512 | 512 | 32.4787 |
| amazon | private | 2028 | canonical | last_active | 0.8333 | 0.8333 | 0.0000 | 57 | 1 | 512 | 512 | 512 | 32.4787 |
| amazon | private | 2028 | canonical | uniform_probability | 0.8333 | 0.8333 | 0.0000 | 57 | 1 | 512 | 512 | 512 | 32.4787 |
| amazon | private | 2029 | b_first | frozen_centroid | 0.8438 | 0.8438 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 35.2998 |
| amazon | private | 2029 | b_first | last_active | 0.8438 | 0.8438 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 35.2998 |
| amazon | private | 2029 | b_first | uniform_probability | 0.8438 | 0.8438 | 0.0000 | 80 | 1 | 512 | 512 | 512 | 35.2998 |
| amazon | private | 2029 | canonical | frozen_centroid | 0.7500 | 0.7630 | -0.0130 | 75 | 2 | 512 | 464 | 512 | 35.2169 |
| amazon | private | 2029 | canonical | last_active | 0.5052 | 0.5000 | 0.0052 | 75 | 2 | 512 | 464 | 512 | 35.2169 |
| amazon | private | 2029 | canonical | uniform_probability | 0.8151 | 0.8177 | -0.0026 | 75 | 2 | 512 | 464 | 512 | 35.2169 |
| amazon | private | 2030 | b_first | frozen_centroid | 0.8620 | 0.8620 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 35.2412 |
| amazon | private | 2030 | b_first | last_active | 0.8620 | 0.8620 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 35.2412 |
| amazon | private | 2030 | b_first | uniform_probability | 0.8620 | 0.8620 | 0.0000 | 77 | 1 | 512 | 512 | 512 | 35.2412 |
| amazon | private | 2030 | canonical | frozen_centroid | 0.8021 | 0.8021 | 0.0000 | 53 | 1 | 512 | 512 | 512 | 32.9502 |
| amazon | private | 2030 | canonical | last_active | 0.8021 | 0.8021 | 0.0000 | 53 | 1 | 512 | 512 | 512 | 32.9502 |
| amazon | private | 2030 | canonical | uniform_probability | 0.8021 | 0.8021 | 0.0000 | 53 | 1 | 512 | 512 | 512 | 32.9502 |
| amazon | private | 2031 | b_first | frozen_centroid | 0.8385 | 0.8385 | 0.0000 | 51 | 1 | 512 | 512 | 512 | 31.8340 |
| amazon | private | 2031 | b_first | last_active | 0.8385 | 0.8385 | 0.0000 | 51 | 1 | 512 | 512 | 512 | 31.8340 |
| amazon | private | 2031 | b_first | uniform_probability | 0.8385 | 0.8385 | 0.0000 | 51 | 1 | 512 | 512 | 512 | 31.8340 |
| amazon | private | 2031 | canonical | frozen_centroid | 0.8490 | 0.8490 | 0.0000 | 74 | 1 | 512 | 512 | 512 | 35.2580 |
| amazon | private | 2031 | canonical | last_active | 0.8490 | 0.8490 | 0.0000 | 74 | 1 | 512 | 512 | 512 | 35.2580 |
| amazon | private | 2031 | canonical | uniform_probability | 0.8490 | 0.8490 | 0.0000 | 74 | 1 | 512 | 512 | 512 | 35.2580 |
| banking | head_only | 2026 | canonical | frozen_centroid | 0.1180 | 0.1246 | -0.0066 | 80 | 3 | 510 | 510 | 510 | 43.3272 |
| banking | head_only | 2026 | canonical | last_active | 0.0774 | 0.0774 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.3272 |
| banking | head_only | 2026 | canonical | uniform_probability | 0.0712 | 0.0712 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.3272 |
| banking | head_only | 2027 | b_first | frozen_centroid | 0.0900 | 0.0833 | 0.0067 | 80 | 3 | 510 | 510 | 510 | 40.8229 |
| banking | head_only | 2027 | b_first | last_active | 0.0137 | 0.0137 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 40.8229 |
| banking | head_only | 2027 | b_first | uniform_probability | 0.0137 | 0.0137 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 40.8229 |
| banking | head_only | 2027 | canonical | frozen_centroid | 0.1107 | 0.1129 | -0.0022 | 80 | 3 | 510 | 510 | 510 | 42.9144 |
| banking | head_only | 2027 | canonical | last_active | 0.0978 | 0.0978 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.9144 |
| banking | head_only | 2027 | canonical | uniform_probability | 0.0137 | 0.0137 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.9144 |
| banking | head_only | 2028 | b_first | frozen_centroid | 0.1027 | 0.0972 | 0.0055 | 80 | 3 | 510 | 510 | 510 | 43.7473 |
| banking | head_only | 2028 | b_first | last_active | 0.0722 | 0.0722 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.7473 |
| banking | head_only | 2028 | b_first | uniform_probability | 0.0864 | 0.0864 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.7473 |
| banking | head_only | 2028 | canonical | frozen_centroid | 0.1244 | 0.1309 | -0.0066 | 80 | 3 | 510 | 510 | 510 | 43.5008 |
| banking | head_only | 2028 | canonical | last_active | 0.0591 | 0.0591 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.5008 |
| banking | head_only | 2028 | canonical | uniform_probability | 0.1219 | 0.1219 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.5008 |
| banking | head_only | 2029 | b_first | frozen_centroid | 0.1301 | 0.1281 | 0.0020 | 80 | 3 | 510 | 510 | 510 | 43.9926 |
| banking | head_only | 2029 | b_first | last_active | 0.0825 | 0.0825 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.9926 |
| banking | head_only | 2029 | b_first | uniform_probability | 0.1340 | 0.1340 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 43.9926 |
| banking | head_only | 2029 | canonical | frozen_centroid | 0.1477 | 0.1554 | -0.0077 | 80 | 3 | 510 | 510 | 510 | 44.4574 |
| banking | head_only | 2029 | canonical | last_active | 0.1086 | 0.1086 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 44.4574 |
| banking | head_only | 2029 | canonical | uniform_probability | 0.0933 | 0.0933 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 44.4574 |
| banking | head_only | 2030 | b_first | frozen_centroid | 0.0784 | 0.0781 | 0.0002 | 80 | 3 | 510 | 510 | 510 | 46.6857 |
| banking | head_only | 2030 | b_first | last_active | 0.0641 | 0.0641 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 46.6857 |
| banking | head_only | 2030 | b_first | uniform_probability | 0.0658 | 0.0658 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 46.6857 |
| banking | head_only | 2030 | canonical | frozen_centroid | 0.0839 | 0.0758 | 0.0080 | 80 | 3 | 510 | 510 | 510 | 42.8164 |
| banking | head_only | 2030 | canonical | last_active | 0.0376 | 0.0376 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.8164 |
| banking | head_only | 2030 | canonical | uniform_probability | 0.0777 | 0.0777 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.8164 |
| banking | head_only | 2031 | b_first | frozen_centroid | 0.1141 | 0.1063 | 0.0078 | 80 | 3 | 510 | 510 | 510 | 42.7356 |
| banking | head_only | 2031 | b_first | last_active | 0.0905 | 0.0905 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.7356 |
| banking | head_only | 2031 | b_first | uniform_probability | 0.0682 | 0.0682 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 42.7356 |
| banking | head_only | 2031 | canonical | frozen_centroid | 0.1345 | 0.1336 | 0.0009 | 80 | 3 | 510 | 510 | 510 | 46.4624 |
| banking | head_only | 2031 | canonical | last_active | 0.0559 | 0.0559 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 46.4624 |
| banking | head_only | 2031 | canonical | uniform_probability | 0.0798 | 0.0798 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 46.4624 |
| banking | private | 2026 | canonical | frozen_centroid | 0.1602 | 0.1613 | -0.0011 | 80 | 3 | 510 | 510 | 510 | 49.1548 |
| banking | private | 2026 | canonical | last_active | 0.1022 | 0.1022 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.1548 |
| banking | private | 2026 | canonical | uniform_probability | 0.1222 | 0.1222 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.1548 |
| banking | private | 2027 | b_first | frozen_centroid | 0.1532 | 0.1423 | 0.0109 | 80 | 3 | 510 | 510 | 510 | 48.7350 |
| banking | private | 2027 | b_first | last_active | 0.0641 | 0.0641 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7350 |
| banking | private | 2027 | b_first | uniform_probability | 0.0778 | 0.0778 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7350 |
| banking | private | 2027 | canonical | frozen_centroid | 0.1593 | 0.1584 | 0.0009 | 80 | 3 | 510 | 510 | 510 | 48.7821 |
| banking | private | 2027 | canonical | last_active | 0.1462 | 0.1462 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7821 |
| banking | private | 2027 | canonical | uniform_probability | 0.0860 | 0.0860 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7821 |
| banking | private | 2028 | b_first | frozen_centroid | 0.1022 | 0.1043 | -0.0022 | 80 | 3 | 510 | 510 | 510 | 50.3819 |
| banking | private | 2028 | b_first | last_active | 0.0733 | 0.0733 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.3819 |
| banking | private | 2028 | b_first | uniform_probability | 0.0972 | 0.0972 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.3819 |
| banking | private | 2028 | canonical | frozen_centroid | 0.1824 | 0.1750 | 0.0075 | 80 | 3 | 510 | 510 | 510 | 49.8690 |
| banking | private | 2028 | canonical | last_active | 0.1247 | 0.1247 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.8690 |
| banking | private | 2028 | canonical | uniform_probability | 0.1442 | 0.1442 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.8690 |
| banking | private | 2029 | b_first | frozen_centroid | 0.1657 | 0.1602 | 0.0055 | 80 | 3 | 510 | 510 | 510 | 50.6344 |
| banking | private | 2029 | b_first | last_active | 0.1283 | 0.1283 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.6344 |
| banking | private | 2029 | b_first | uniform_probability | 0.1142 | 0.1142 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.6344 |
| banking | private | 2029 | canonical | frozen_centroid | 0.1902 | 0.1942 | -0.0040 | 80 | 3 | 510 | 510 | 510 | 51.5785 |
| banking | private | 2029 | canonical | last_active | 0.1129 | 0.1129 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 51.5785 |
| banking | private | 2029 | canonical | uniform_probability | 0.1612 | 0.1612 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 51.5785 |
| banking | private | 2030 | b_first | frozen_centroid | 0.1764 | 0.1772 | -0.0008 | 80 | 3 | 510 | 510 | 510 | 50.7685 |
| banking | private | 2030 | b_first | last_active | 0.1397 | 0.1397 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.7685 |
| banking | private | 2030 | b_first | uniform_probability | 0.2052 | 0.2052 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.7685 |
| banking | private | 2030 | canonical | frozen_centroid | 0.1703 | 0.1589 | 0.0114 | 80 | 3 | 510 | 510 | 510 | 48.7890 |
| banking | private | 2030 | canonical | last_active | 0.0796 | 0.0796 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7890 |
| banking | private | 2030 | canonical | uniform_probability | 0.1776 | 0.1776 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 48.7890 |
| banking | private | 2031 | b_first | frozen_centroid | 0.1745 | 0.1656 | 0.0089 | 80 | 3 | 510 | 510 | 510 | 49.6727 |
| banking | private | 2031 | b_first | last_active | 0.1054 | 0.1054 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.6727 |
| banking | private | 2031 | b_first | uniform_probability | 0.1296 | 0.1296 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 49.6727 |
| banking | private | 2031 | canonical | frozen_centroid | 0.1539 | 0.1543 | -0.0004 | 80 | 3 | 510 | 510 | 510 | 50.5333 |
| banking | private | 2031 | canonical | last_active | 0.0688 | 0.0688 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.5333 |
| banking | private | 2031 | canonical | uniform_probability | 0.1167 | 0.1167 | 0.0000 | 80 | 3 | 510 | 510 | 510 | 50.5333 |

## Limits

Equal reservoir capacity does not make different adapter pools parameter- or compute-matched. The extension also includes a hard eight-adapter cap and stricter restoration of stale gradients/flags/modes; the no-shrink numeric-equivalence test checks that cleanup leaves action scores unchanged. This sensitivity does not constitute an untouched final evaluation or modern-baseline comparison.
