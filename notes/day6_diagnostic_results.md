# Frozen seed and order diagnostic results

This batch evaluates the unchanged private-package CAU-v1 and a zero-LoRA head-only control, each against its fixed-single learner. Official tests remain unused. These are diagnostics conditional on fixed development data, not a submission-readiness or resource-matched superiority claim.

Completed trajectories: 80/80. Partial or unfinished folders: [].

## amazon / frozen_centroid

Paired accuracy differences; both orders are averaged inside each seed before the interval.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | frozen_centroid | LoRA minus head-only / CAU | 5 | 0.0299 | 0.0130 | 0.0469 |
| amazon | frozen_centroid | LoRA minus head-only / single | 5 | 0.0440 | 0.0265 | 0.0615 |
| amazon | frozen_centroid | CAU minus single / private | 5 | -0.0169 | -0.0405 | 0.0066 |
| amazon | frozen_centroid | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |

## amazon / last_active

Paired accuracy differences; both orders are averaged inside each seed before the interval.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | last_active | LoRA minus head-only / CAU | 5 | 0.0036 | -0.0850 | 0.0923 |
| amazon | last_active | LoRA minus head-only / single | 5 | 0.0440 | 0.0265 | 0.0615 |
| amazon | last_active | CAU minus single / private | 5 | -0.0432 | -0.1370 | 0.0505 |
| amazon | last_active | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |

## amazon / uniform_probability

Paired accuracy differences; both orders are averaged inside each seed before the interval.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| amazon | uniform_probability | LoRA minus head-only / CAU | 5 | 0.0354 | 0.0282 | 0.0426 |
| amazon | uniform_probability | LoRA minus head-only / single | 5 | 0.0440 | 0.0265 | 0.0615 |
| amazon | uniform_probability | CAU minus single / private | 5 | -0.0115 | -0.0250 | 0.0020 |
| amazon | uniform_probability | CAU minus single / head-only | 5 | -0.0029 | -0.0242 | 0.0184 |

## banking / frozen_centroid

Paired accuracy differences; both orders are averaged inside each seed before the interval.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| banking | frozen_centroid | LoRA minus head-only / CAU | 5 | 0.0489 | 0.0172 | 0.0805 |
| banking | frozen_centroid | LoRA minus head-only / single | 5 | 0.0409 | -0.0005 | 0.0823 |
| banking | frozen_centroid | CAU minus single / private | 5 | -0.0054 | -0.0399 | 0.0291 |
| banking | frozen_centroid | CAU minus single / head-only | 5 | -0.0134 | -0.0363 | 0.0096 |

## banking / last_active

Paired accuracy differences; both orders are averaged inside each seed before the interval.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| banking | last_active | LoRA minus head-only / CAU | 5 | 0.0361 | 0.0136 | 0.0586 |
| banking | last_active | LoRA minus head-only / single | 5 | 0.0409 | -0.0005 | 0.0823 |
| banking | last_active | CAU minus single / private | 5 | -0.0601 | -0.1060 | -0.0142 |
| banking | last_active | CAU minus single / head-only | 5 | -0.0553 | -0.0694 | -0.0413 |

## banking / uniform_probability

Paired accuracy differences; both orders are averaged inside each seed before the interval.

| regime | rule | contrast | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| banking | uniform_probability | LoRA minus head-only / CAU | 5 | 0.0555 | 0.0042 | 0.1068 |
| banking | uniform_probability | LoRA minus head-only / single | 5 | 0.0409 | -0.0005 | 0.0823 |
| banking | uniform_probability | CAU minus single / private | 5 | -0.0335 | -0.0835 | 0.0166 |
| banking | uniform_probability | CAU minus single / head-only | 5 | -0.0481 | -0.0870 | -0.0091 |

## Full run table

| regime | seed | order | architecture | policy | rule | macro_accuracy | updates | adapters | live_training_seconds | replay_items |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | 2027 | b_first | head_only | cau | frozen_centroid | 0.8307 | 73 | 1 | 25.3714 | 512 |
| amazon | 2027 | b_first | head_only | cau | last_active | 0.8307 | 73 | 1 | 25.3714 | 512 |
| amazon | 2027 | b_first | head_only | cau | uniform_probability | 0.8307 | 73 | 1 | 25.3714 | 512 |
| amazon | 2027 | canonical | head_only | cau | frozen_centroid | 0.7943 | 80 | 1 | 25.4713 | 512 |
| amazon | 2027 | canonical | head_only | cau | last_active | 0.7943 | 80 | 1 | 25.4713 | 512 |
| amazon | 2027 | canonical | head_only | cau | uniform_probability | 0.7943 | 80 | 1 | 25.4713 | 512 |
| amazon | 2028 | b_first | head_only | cau | frozen_centroid | 0.8099 | 79 | 1 | 25.9283 | 512 |
| amazon | 2028 | b_first | head_only | cau | last_active | 0.8099 | 79 | 1 | 25.9283 | 512 |
| amazon | 2028 | b_first | head_only | cau | uniform_probability | 0.8099 | 79 | 1 | 25.9283 | 512 |
| amazon | 2028 | canonical | head_only | cau | frozen_centroid | 0.7995 | 66 | 1 | 25.4236 | 512 |
| amazon | 2028 | canonical | head_only | cau | last_active | 0.7995 | 66 | 1 | 25.4236 | 512 |
| amazon | 2028 | canonical | head_only | cau | uniform_probability | 0.7995 | 66 | 1 | 25.4236 | 512 |
| amazon | 2029 | b_first | head_only | cau | frozen_centroid | 0.8099 | 73 | 1 | 25.3135 | 512 |
| amazon | 2029 | b_first | head_only | cau | last_active | 0.8099 | 73 | 1 | 25.3135 | 512 |
| amazon | 2029 | b_first | head_only | cau | uniform_probability | 0.8099 | 73 | 1 | 25.3135 | 512 |
| amazon | 2029 | canonical | head_only | cau | frozen_centroid | 0.7812 | 63 | 1 | 24.6899 | 512 |
| amazon | 2029 | canonical | head_only | cau | last_active | 0.7812 | 63 | 1 | 24.6899 | 512 |
| amazon | 2029 | canonical | head_only | cau | uniform_probability | 0.7812 | 63 | 1 | 24.6899 | 512 |
| amazon | 2030 | b_first | head_only | cau | frozen_centroid | 0.8047 | 79 | 1 | 25.9882 | 512 |
| amazon | 2030 | b_first | head_only | cau | last_active | 0.8047 | 79 | 1 | 25.9882 | 512 |
| amazon | 2030 | b_first | head_only | cau | uniform_probability | 0.8047 | 79 | 1 | 25.9882 | 512 |
| amazon | 2030 | canonical | head_only | cau | frozen_centroid | 0.8021 | 72 | 1 | 25.9704 | 512 |
| amazon | 2030 | canonical | head_only | cau | last_active | 0.8021 | 72 | 1 | 25.9704 | 512 |
| amazon | 2030 | canonical | head_only | cau | uniform_probability | 0.8021 | 72 | 1 | 25.9704 | 512 |
| amazon | 2031 | b_first | head_only | cau | frozen_centroid | 0.8125 | 63 | 1 | 25.5129 | 512 |
| amazon | 2031 | b_first | head_only | cau | last_active | 0.8125 | 63 | 1 | 25.5129 | 512 |
| amazon | 2031 | b_first | head_only | cau | uniform_probability | 0.8125 | 63 | 1 | 25.5129 | 512 |
| amazon | 2031 | canonical | head_only | cau | frozen_centroid | 0.7969 | 78 | 1 | 30.2442 | 512 |
| amazon | 2031 | canonical | head_only | cau | last_active | 0.7969 | 78 | 1 | 30.2442 | 512 |
| amazon | 2031 | canonical | head_only | cau | uniform_probability | 0.7969 | 78 | 1 | 30.2442 | 512 |
| amazon | 2027 | b_first | head_only | single | frozen_centroid | 0.8281 | 80 | 1 | 1.3314 | 512 |
| amazon | 2027 | b_first | head_only | single | last_active | 0.8281 | 80 | 1 | 1.3314 | 512 |
| amazon | 2027 | b_first | head_only | single | uniform_probability | 0.8281 | 80 | 1 | 1.3314 | 512 |
| amazon | 2027 | canonical | head_only | single | frozen_centroid | 0.7943 | 80 | 1 | 1.3134 | 512 |
| amazon | 2027 | canonical | head_only | single | last_active | 0.7943 | 80 | 1 | 1.3134 | 512 |
| amazon | 2027 | canonical | head_only | single | uniform_probability | 0.7943 | 80 | 1 | 1.3134 | 512 |
| amazon | 2028 | b_first | head_only | single | frozen_centroid | 0.8151 | 80 | 1 | 1.3890 | 512 |
| amazon | 2028 | b_first | head_only | single | last_active | 0.8151 | 80 | 1 | 1.3890 | 512 |
| amazon | 2028 | b_first | head_only | single | uniform_probability | 0.8151 | 80 | 1 | 1.3890 | 512 |
| amazon | 2028 | canonical | head_only | single | frozen_centroid | 0.8125 | 80 | 1 | 1.3424 | 512 |
| amazon | 2028 | canonical | head_only | single | last_active | 0.8125 | 80 | 1 | 1.3424 | 512 |
| amazon | 2028 | canonical | head_only | single | uniform_probability | 0.8125 | 80 | 1 | 1.3424 | 512 |
| amazon | 2029 | b_first | head_only | single | frozen_centroid | 0.8203 | 80 | 1 | 1.3278 | 512 |
| amazon | 2029 | b_first | head_only | single | last_active | 0.8203 | 80 | 1 | 1.3278 | 512 |
| amazon | 2029 | b_first | head_only | single | uniform_probability | 0.8203 | 80 | 1 | 1.3278 | 512 |
| amazon | 2029 | canonical | head_only | single | frozen_centroid | 0.8281 | 80 | 1 | 1.3162 | 512 |
| amazon | 2029 | canonical | head_only | single | last_active | 0.8281 | 80 | 1 | 1.3162 | 512 |
| amazon | 2029 | canonical | head_only | single | uniform_probability | 0.8281 | 80 | 1 | 1.3162 | 512 |
| amazon | 2030 | b_first | head_only | single | frozen_centroid | 0.7812 | 80 | 1 | 1.5811 | 512 |
| amazon | 2030 | b_first | head_only | single | last_active | 0.7812 | 80 | 1 | 1.5811 | 512 |
| amazon | 2030 | b_first | head_only | single | uniform_probability | 0.7812 | 80 | 1 | 1.5811 | 512 |
| amazon | 2030 | canonical | head_only | single | frozen_centroid | 0.7917 | 80 | 1 | 1.3368 | 512 |
| amazon | 2030 | canonical | head_only | single | last_active | 0.7917 | 80 | 1 | 1.3368 | 512 |
| amazon | 2030 | canonical | head_only | single | uniform_probability | 0.7917 | 80 | 1 | 1.3368 | 512 |
| amazon | 2031 | b_first | head_only | single | frozen_centroid | 0.8177 | 80 | 1 | 1.4044 | 512 |
| amazon | 2031 | b_first | head_only | single | last_active | 0.8177 | 80 | 1 | 1.4044 | 512 |
| amazon | 2031 | b_first | head_only | single | uniform_probability | 0.8177 | 80 | 1 | 1.4044 | 512 |
| amazon | 2031 | canonical | head_only | single | frozen_centroid | 0.7812 | 80 | 1 | 2.1237 | 512 |
| amazon | 2031 | canonical | head_only | single | last_active | 0.7812 | 80 | 1 | 2.1237 | 512 |
| amazon | 2031 | canonical | head_only | single | uniform_probability | 0.7812 | 80 | 1 | 2.1237 | 512 |
| amazon | 2027 | b_first | private | cau | frozen_centroid | 0.8594 | 77 | 1 | 30.2306 | 512 |
| amazon | 2027 | b_first | private | cau | last_active | 0.8594 | 77 | 1 | 30.2306 | 512 |
| amazon | 2027 | b_first | private | cau | uniform_probability | 0.8594 | 77 | 1 | 30.2306 | 512 |
| amazon | 2027 | canonical | private | cau | frozen_centroid | 0.8516 | 72 | 1 | 30.1522 | 512 |
| amazon | 2027 | canonical | private | cau | last_active | 0.8516 | 72 | 1 | 30.1522 | 512 |
| amazon | 2027 | canonical | private | cau | uniform_probability | 0.8516 | 72 | 1 | 30.1522 | 512 |
| amazon | 2028 | b_first | private | cau | frozen_centroid | 0.8385 | 69 | 1 | 28.8557 | 512 |
| amazon | 2028 | b_first | private | cau | last_active | 0.8385 | 69 | 1 | 28.8557 | 512 |
| amazon | 2028 | b_first | private | cau | uniform_probability | 0.8385 | 69 | 1 | 28.8557 | 512 |
| amazon | 2028 | canonical | private | cau | frozen_centroid | 0.8333 | 57 | 1 | 28.2440 | 512 |
| amazon | 2028 | canonical | private | cau | last_active | 0.8333 | 57 | 1 | 28.2440 | 512 |
| amazon | 2028 | canonical | private | cau | uniform_probability | 0.8333 | 57 | 1 | 28.2440 | 512 |
| amazon | 2029 | b_first | private | cau | frozen_centroid | 0.8438 | 80 | 1 | 29.6864 | 512 |
| amazon | 2029 | b_first | private | cau | last_active | 0.8438 | 80 | 1 | 29.6864 | 512 |
| amazon | 2029 | b_first | private | cau | uniform_probability | 0.8438 | 80 | 1 | 29.6864 | 512 |
| amazon | 2029 | canonical | private | cau | frozen_centroid | 0.7630 | 75 | 2 | 29.5587 | 736 |
| amazon | 2029 | canonical | private | cau | last_active | 0.5000 | 75 | 2 | 29.5587 | 736 |
| amazon | 2029 | canonical | private | cau | uniform_probability | 0.8177 | 75 | 2 | 29.5587 | 736 |
| amazon | 2030 | b_first | private | cau | frozen_centroid | 0.8620 | 77 | 1 | 29.7227 | 512 |
| amazon | 2030 | b_first | private | cau | last_active | 0.8620 | 77 | 1 | 29.7227 | 512 |
| amazon | 2030 | b_first | private | cau | uniform_probability | 0.8620 | 77 | 1 | 29.7227 | 512 |
| amazon | 2030 | canonical | private | cau | frozen_centroid | 0.8021 | 53 | 1 | 27.8837 | 512 |
| amazon | 2030 | canonical | private | cau | last_active | 0.8021 | 53 | 1 | 27.8837 | 512 |
| amazon | 2030 | canonical | private | cau | uniform_probability | 0.8021 | 53 | 1 | 27.8837 | 512 |
| amazon | 2031 | b_first | private | cau | frozen_centroid | 0.8385 | 51 | 1 | 28.1333 | 512 |
| amazon | 2031 | b_first | private | cau | last_active | 0.8385 | 51 | 1 | 28.1333 | 512 |
| amazon | 2031 | b_first | private | cau | uniform_probability | 0.8385 | 51 | 1 | 28.1333 | 512 |
| amazon | 2031 | canonical | private | cau | frozen_centroid | 0.8490 | 74 | 1 | 33.1162 | 512 |
| amazon | 2031 | canonical | private | cau | last_active | 0.8490 | 74 | 1 | 33.1162 | 512 |
| amazon | 2031 | canonical | private | cau | uniform_probability | 0.8490 | 74 | 1 | 33.1162 | 512 |
| amazon | 2027 | b_first | private | single | frozen_centroid | 0.8568 | 80 | 1 | 2.2285 | 512 |
| amazon | 2027 | b_first | private | single | last_active | 0.8568 | 80 | 1 | 2.2285 | 512 |
| amazon | 2027 | b_first | private | single | uniform_probability | 0.8568 | 80 | 1 | 2.2285 | 512 |
| amazon | 2027 | canonical | private | single | frozen_centroid | 0.8464 | 80 | 1 | 2.3614 | 512 |
| amazon | 2027 | canonical | private | single | last_active | 0.8464 | 80 | 1 | 2.3614 | 512 |
| amazon | 2027 | canonical | private | single | uniform_probability | 0.8464 | 80 | 1 | 2.3614 | 512 |
| amazon | 2028 | b_first | private | single | frozen_centroid | 0.8542 | 80 | 1 | 2.0871 | 512 |
| amazon | 2028 | b_first | private | single | last_active | 0.8542 | 80 | 1 | 2.0871 | 512 |
| amazon | 2028 | b_first | private | single | uniform_probability | 0.8542 | 80 | 1 | 2.0871 | 512 |
| amazon | 2028 | canonical | private | single | frozen_centroid | 0.8594 | 80 | 1 | 2.1823 | 512 |
| amazon | 2028 | canonical | private | single | last_active | 0.8594 | 80 | 1 | 2.1823 | 512 |
| amazon | 2028 | canonical | private | single | uniform_probability | 0.8594 | 80 | 1 | 2.1823 | 512 |
| amazon | 2029 | b_first | private | single | frozen_centroid | 0.8438 | 80 | 1 | 2.0231 | 512 |
| amazon | 2029 | b_first | private | single | last_active | 0.8438 | 80 | 1 | 2.0231 | 512 |
| amazon | 2029 | b_first | private | single | uniform_probability | 0.8438 | 80 | 1 | 2.0231 | 512 |
| amazon | 2029 | canonical | private | single | frozen_centroid | 0.8542 | 80 | 1 | 2.0488 | 512 |
| amazon | 2029 | canonical | private | single | last_active | 0.8542 | 80 | 1 | 2.0488 | 512 |
| amazon | 2029 | canonical | private | single | uniform_probability | 0.8542 | 80 | 1 | 2.0488 | 512 |
| amazon | 2030 | b_first | private | single | frozen_centroid | 0.8568 | 80 | 1 | 2.1064 | 512 |
| amazon | 2030 | b_first | private | single | last_active | 0.8568 | 80 | 1 | 2.1064 | 512 |
| amazon | 2030 | b_first | private | single | uniform_probability | 0.8568 | 80 | 1 | 2.1064 | 512 |
| amazon | 2030 | canonical | private | single | frozen_centroid | 0.8438 | 80 | 1 | 2.0476 | 512 |
| amazon | 2030 | canonical | private | single | last_active | 0.8438 | 80 | 1 | 2.0476 | 512 |
| amazon | 2030 | canonical | private | single | uniform_probability | 0.8438 | 80 | 1 | 2.0476 | 512 |
| amazon | 2031 | b_first | private | single | frozen_centroid | 0.8542 | 80 | 1 | 2.2141 | 512 |
| amazon | 2031 | b_first | private | single | last_active | 0.8542 | 80 | 1 | 2.2141 | 512 |
| amazon | 2031 | b_first | private | single | uniform_probability | 0.8542 | 80 | 1 | 2.2141 | 512 |
| amazon | 2031 | canonical | private | single | frozen_centroid | 0.8411 | 80 | 1 | 2.1306 | 512 |
| amazon | 2031 | canonical | private | single | last_active | 0.8411 | 80 | 1 | 2.1306 | 512 |
| amazon | 2031 | canonical | private | single | uniform_probability | 0.8411 | 80 | 1 | 2.1306 | 512 |
| banking | 2027 | b_first | head_only | cau | frozen_centroid | 0.0833 | 80 | 3 | 35.6625 | 1255 |
| banking | 2027 | b_first | head_only | cau | last_active | 0.0137 | 80 | 3 | 35.6625 | 1255 |
| banking | 2027 | b_first | head_only | cau | uniform_probability | 0.0137 | 80 | 3 | 35.6625 | 1255 |
| banking | 2027 | canonical | head_only | cau | frozen_centroid | 0.1129 | 80 | 3 | 35.4548 | 1255 |
| banking | 2027 | canonical | head_only | cau | last_active | 0.0978 | 80 | 3 | 35.4548 | 1255 |
| banking | 2027 | canonical | head_only | cau | uniform_probability | 0.0137 | 80 | 3 | 35.4548 | 1255 |
| banking | 2028 | b_first | head_only | cau | frozen_centroid | 0.0972 | 80 | 3 | 36.3163 | 1255 |
| banking | 2028 | b_first | head_only | cau | last_active | 0.0722 | 80 | 3 | 36.3163 | 1255 |
| banking | 2028 | b_first | head_only | cau | uniform_probability | 0.0864 | 80 | 3 | 36.3163 | 1255 |
| banking | 2028 | canonical | head_only | cau | frozen_centroid | 0.1309 | 80 | 3 | 35.5949 | 1255 |
| banking | 2028 | canonical | head_only | cau | last_active | 0.0591 | 80 | 3 | 35.5949 | 1255 |
| banking | 2028 | canonical | head_only | cau | uniform_probability | 0.1219 | 80 | 3 | 35.5949 | 1255 |
| banking | 2029 | b_first | head_only | cau | frozen_centroid | 0.1281 | 80 | 3 | 36.2424 | 1255 |
| banking | 2029 | b_first | head_only | cau | last_active | 0.0825 | 80 | 3 | 36.2424 | 1255 |
| banking | 2029 | b_first | head_only | cau | uniform_probability | 0.1340 | 80 | 3 | 36.2424 | 1255 |
| banking | 2029 | canonical | head_only | cau | frozen_centroid | 0.1554 | 80 | 3 | 37.5767 | 1255 |
| banking | 2029 | canonical | head_only | cau | last_active | 0.1086 | 80 | 3 | 37.5767 | 1255 |
| banking | 2029 | canonical | head_only | cau | uniform_probability | 0.0933 | 80 | 3 | 37.5767 | 1255 |
| banking | 2030 | b_first | head_only | cau | frozen_centroid | 0.0781 | 80 | 3 | 35.6015 | 1255 |
| banking | 2030 | b_first | head_only | cau | last_active | 0.0641 | 80 | 3 | 35.6015 | 1255 |
| banking | 2030 | b_first | head_only | cau | uniform_probability | 0.0658 | 80 | 3 | 35.6015 | 1255 |
| banking | 2030 | canonical | head_only | cau | frozen_centroid | 0.0758 | 80 | 3 | 35.8988 | 1255 |
| banking | 2030 | canonical | head_only | cau | last_active | 0.0376 | 80 | 3 | 35.8988 | 1255 |
| banking | 2030 | canonical | head_only | cau | uniform_probability | 0.0777 | 80 | 3 | 35.8988 | 1255 |
| banking | 2031 | b_first | head_only | cau | frozen_centroid | 0.1063 | 80 | 3 | 36.5570 | 1255 |
| banking | 2031 | b_first | head_only | cau | last_active | 0.0905 | 80 | 3 | 36.5570 | 1255 |
| banking | 2031 | b_first | head_only | cau | uniform_probability | 0.0682 | 80 | 3 | 36.5570 | 1255 |
| banking | 2031 | canonical | head_only | cau | frozen_centroid | 0.1336 | 80 | 3 | 40.6286 | 1255 |
| banking | 2031 | canonical | head_only | cau | last_active | 0.0559 | 80 | 3 | 40.6286 | 1255 |
| banking | 2031 | canonical | head_only | cau | uniform_probability | 0.0798 | 80 | 3 | 40.6286 | 1255 |
| banking | 2027 | b_first | head_only | single | frozen_centroid | 0.0744 | 80 | 1 | 1.2311 | 512 |
| banking | 2027 | b_first | head_only | single | last_active | 0.0744 | 80 | 1 | 1.2311 | 512 |
| banking | 2027 | b_first | head_only | single | uniform_probability | 0.0744 | 80 | 1 | 1.2311 | 512 |
| banking | 2027 | canonical | head_only | single | frozen_centroid | 0.1435 | 80 | 1 | 1.3147 | 512 |
| banking | 2027 | canonical | head_only | single | last_active | 0.1435 | 80 | 1 | 1.3147 | 512 |
| banking | 2027 | canonical | head_only | single | uniform_probability | 0.1435 | 80 | 1 | 1.3147 | 512 |
| banking | 2028 | b_first | head_only | single | frozen_centroid | 0.1839 | 80 | 1 | 1.2375 | 512 |
| banking | 2028 | b_first | head_only | single | last_active | 0.1839 | 80 | 1 | 1.2375 | 512 |
| banking | 2028 | b_first | head_only | single | uniform_probability | 0.1839 | 80 | 1 | 1.2375 | 512 |
| banking | 2028 | canonical | head_only | single | frozen_centroid | 0.0633 | 80 | 1 | 1.2425 | 512 |
| banking | 2028 | canonical | head_only | single | last_active | 0.0633 | 80 | 1 | 1.2425 | 512 |
| banking | 2028 | canonical | head_only | single | uniform_probability | 0.0633 | 80 | 1 | 1.2425 | 512 |
| banking | 2029 | b_first | head_only | single | frozen_centroid | 0.1121 | 80 | 1 | 1.2414 | 512 |
| banking | 2029 | b_first | head_only | single | last_active | 0.1121 | 80 | 1 | 1.2414 | 512 |
| banking | 2029 | b_first | head_only | single | uniform_probability | 0.1121 | 80 | 1 | 1.2414 | 512 |
| banking | 2029 | canonical | head_only | single | frozen_centroid | 0.1548 | 80 | 1 | 1.2300 | 512 |
| banking | 2029 | canonical | head_only | single | last_active | 0.1548 | 80 | 1 | 1.2300 | 512 |
| banking | 2029 | canonical | head_only | single | uniform_probability | 0.1548 | 80 | 1 | 1.2300 | 512 |
| banking | 2030 | b_first | head_only | single | frozen_centroid | 0.1352 | 80 | 1 | 1.2663 | 512 |
| banking | 2030 | b_first | head_only | single | last_active | 0.1352 | 80 | 1 | 1.2663 | 512 |
| banking | 2030 | b_first | head_only | single | uniform_probability | 0.1352 | 80 | 1 | 1.2663 | 512 |
| banking | 2030 | canonical | head_only | single | frozen_centroid | 0.1046 | 80 | 1 | 1.2642 | 512 |
| banking | 2030 | canonical | head_only | single | last_active | 0.1046 | 80 | 1 | 1.2642 | 512 |
| banking | 2030 | canonical | head_only | single | uniform_probability | 0.1046 | 80 | 1 | 1.2642 | 512 |
| banking | 2031 | b_first | head_only | single | frozen_centroid | 0.0885 | 80 | 1 | 1.3383 | 512 |
| banking | 2031 | b_first | head_only | single | last_active | 0.0885 | 80 | 1 | 1.3383 | 512 |
| banking | 2031 | b_first | head_only | single | uniform_probability | 0.0885 | 80 | 1 | 1.3383 | 512 |
| banking | 2031 | canonical | head_only | single | frozen_centroid | 0.1750 | 80 | 1 | 1.5518 | 512 |
| banking | 2031 | canonical | head_only | single | last_active | 0.1750 | 80 | 1 | 1.5518 | 512 |
| banking | 2031 | canonical | head_only | single | uniform_probability | 0.1750 | 80 | 1 | 1.5518 | 512 |
| banking | 2027 | b_first | private | cau | frozen_centroid | 0.1423 | 80 | 3 | 41.1537 | 1255 |
| banking | 2027 | b_first | private | cau | last_active | 0.0641 | 80 | 3 | 41.1537 | 1255 |
| banking | 2027 | b_first | private | cau | uniform_probability | 0.0778 | 80 | 3 | 41.1537 | 1255 |
| banking | 2027 | canonical | private | cau | frozen_centroid | 0.1584 | 80 | 3 | 41.9313 | 1255 |
| banking | 2027 | canonical | private | cau | last_active | 0.1462 | 80 | 3 | 41.9313 | 1255 |
| banking | 2027 | canonical | private | cau | uniform_probability | 0.0860 | 80 | 3 | 41.9313 | 1255 |
| banking | 2028 | b_first | private | cau | frozen_centroid | 0.1043 | 80 | 3 | 41.5341 | 1255 |
| banking | 2028 | b_first | private | cau | last_active | 0.0733 | 80 | 3 | 41.5341 | 1255 |
| banking | 2028 | b_first | private | cau | uniform_probability | 0.0972 | 80 | 3 | 41.5341 | 1255 |
| banking | 2028 | canonical | private | cau | frozen_centroid | 0.1750 | 80 | 3 | 40.9061 | 1255 |
| banking | 2028 | canonical | private | cau | last_active | 0.1247 | 80 | 3 | 40.9061 | 1255 |
| banking | 2028 | canonical | private | cau | uniform_probability | 0.1442 | 80 | 3 | 40.9061 | 1255 |
| banking | 2029 | b_first | private | cau | frozen_centroid | 0.1602 | 80 | 3 | 40.9787 | 1255 |
| banking | 2029 | b_first | private | cau | last_active | 0.1283 | 80 | 3 | 40.9787 | 1255 |
| banking | 2029 | b_first | private | cau | uniform_probability | 0.1142 | 80 | 3 | 40.9787 | 1255 |
| banking | 2029 | canonical | private | cau | frozen_centroid | 0.1942 | 80 | 3 | 42.1141 | 1255 |
| banking | 2029 | canonical | private | cau | last_active | 0.1129 | 80 | 3 | 42.1141 | 1255 |
| banking | 2029 | canonical | private | cau | uniform_probability | 0.1612 | 80 | 3 | 42.1141 | 1255 |
| banking | 2030 | b_first | private | cau | frozen_centroid | 0.1772 | 80 | 3 | 40.7848 | 1255 |
| banking | 2030 | b_first | private | cau | last_active | 0.1397 | 80 | 3 | 40.7848 | 1255 |
| banking | 2030 | b_first | private | cau | uniform_probability | 0.2052 | 80 | 3 | 40.7848 | 1255 |
| banking | 2030 | canonical | private | cau | frozen_centroid | 0.1589 | 80 | 3 | 40.4897 | 1255 |
| banking | 2030 | canonical | private | cau | last_active | 0.0796 | 80 | 3 | 40.4897 | 1255 |
| banking | 2030 | canonical | private | cau | uniform_probability | 0.1776 | 80 | 3 | 40.4897 | 1255 |
| banking | 2031 | b_first | private | cau | frozen_centroid | 0.1656 | 80 | 3 | 42.1435 | 1255 |
| banking | 2031 | b_first | private | cau | last_active | 0.1054 | 80 | 3 | 42.1435 | 1255 |
| banking | 2031 | b_first | private | cau | uniform_probability | 0.1296 | 80 | 3 | 42.1435 | 1255 |
| banking | 2031 | canonical | private | cau | frozen_centroid | 0.1543 | 80 | 3 | 44.2594 | 1255 |
| banking | 2031 | canonical | private | cau | last_active | 0.0688 | 80 | 3 | 44.2594 | 1255 |
| banking | 2031 | canonical | private | cau | uniform_probability | 0.1167 | 80 | 3 | 44.2594 | 1255 |
| banking | 2027 | b_first | private | single | frozen_centroid | 0.1136 | 80 | 1 | 2.3381 | 512 |
| banking | 2027 | b_first | private | single | last_active | 0.1136 | 80 | 1 | 2.3381 | 512 |
| banking | 2027 | b_first | private | single | uniform_probability | 0.1136 | 80 | 1 | 2.3381 | 512 |
| banking | 2027 | canonical | private | single | frozen_centroid | 0.2131 | 80 | 1 | 2.2377 | 512 |
| banking | 2027 | canonical | private | single | last_active | 0.2131 | 80 | 1 | 2.2377 | 512 |
| banking | 2027 | canonical | private | single | uniform_probability | 0.2131 | 80 | 1 | 2.2377 | 512 |
| banking | 2028 | b_first | private | single | frozen_centroid | 0.1550 | 80 | 1 | 2.0014 | 512 |
| banking | 2028 | b_first | private | single | last_active | 0.1550 | 80 | 1 | 2.0014 | 512 |
| banking | 2028 | b_first | private | single | uniform_probability | 0.1550 | 80 | 1 | 2.0014 | 512 |
| banking | 2028 | canonical | private | single | frozen_centroid | 0.0820 | 80 | 1 | 2.1252 | 512 |
| banking | 2028 | canonical | private | single | last_active | 0.0820 | 80 | 1 | 2.1252 | 512 |
| banking | 2028 | canonical | private | single | uniform_probability | 0.0820 | 80 | 1 | 2.1252 | 512 |
| banking | 2029 | b_first | private | single | frozen_centroid | 0.0820 | 80 | 1 | 1.9906 | 512 |
| banking | 2029 | b_first | private | single | last_active | 0.0820 | 80 | 1 | 1.9906 | 512 |
| banking | 2029 | b_first | private | single | uniform_probability | 0.0820 | 80 | 1 | 1.9906 | 512 |
| banking | 2029 | canonical | private | single | frozen_centroid | 0.2200 | 80 | 1 | 2.0616 | 512 |
| banking | 2029 | canonical | private | single | last_active | 0.2200 | 80 | 1 | 2.0616 | 512 |
| banking | 2029 | canonical | private | single | uniform_probability | 0.2200 | 80 | 1 | 2.0616 | 512 |
| banking | 2030 | b_first | private | single | frozen_centroid | 0.1513 | 80 | 1 | 2.0797 | 512 |
| banking | 2030 | b_first | private | single | last_active | 0.1513 | 80 | 1 | 2.0797 | 512 |
| banking | 2030 | b_first | private | single | uniform_probability | 0.1513 | 80 | 1 | 2.0797 | 512 |
| banking | 2030 | canonical | private | single | frozen_centroid | 0.2359 | 80 | 1 | 1.8613 | 512 |
| banking | 2030 | canonical | private | single | last_active | 0.2359 | 80 | 1 | 1.8613 | 512 |
| banking | 2030 | canonical | private | single | uniform_probability | 0.2359 | 80 | 1 | 1.8613 | 512 |
| banking | 2031 | b_first | private | single | frozen_centroid | 0.1616 | 80 | 1 | 2.0875 | 512 |
| banking | 2031 | b_first | private | single | last_active | 0.1616 | 80 | 1 | 2.0875 | 512 |
| banking | 2031 | b_first | private | single | uniform_probability | 0.1616 | 80 | 1 | 2.0875 | 512 |
| banking | 2031 | canonical | private | single | frozen_centroid | 0.2298 | 80 | 1 | 2.0486 | 512 |
| banking | 2031 | canonical | private | single | last_active | 0.2298 | 80 | 1 | 2.0486 | 512 |
| banking | 2031 | canonical | private | single | uniform_probability | 0.2298 | 80 | 1 | 2.0486 | 512 |

## Interpretation limits

Intervals are descriptive 95% Student-t intervals over independent seed clusters (maximum five), averaging the two paired orders within a seed. They condition on fixed evaluation examples and do not capture dataset sampling uncertainty. No window-level tests, oracle selection, post-outcome routing-rule choice, or multiplicity-adjusted winner claim is made.

Pool growth increases total reservoir and private-head storage. Head-only stores unused zero-LoRA scaffolding; parameter columns report it explicitly. The primary experimental manipulation is training LoRA together with each classifier package versus training only classifier packages. Modern method baselines, fixed-total-resource runs and an untouched final evaluation are pending.
