# Train-only MultiNLI stress-test results

Fixed three-class genre recurrence, grouped premise holdout, with sharp and gradual boundaries. Official matched/mismatched validation and test data were not evaluated. The short-context, 1440-example protocol is a development stress test, not a competitive NLI benchmark.

Completed trajectories 24/24; incomplete folders: [].

| seed | condition | architecture | policy | rule | macro_accuracy | steps | updates | adapters | spawns | live_training_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | blurry | head_only | cau | frozen_centroid | 0.3281 | 90 | 90 | 4 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"},{"step":83,"segment":"B2"}] | 49.9361 |
| 2026 | blurry | head_only | cau | last_active | 0.3351 | 90 | 90 | 4 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"},{"step":83,"segment":"B2"}] | 49.9361 |
| 2026 | blurry | head_only | cau | uniform_probability | 0.3542 | 90 | 90 | 4 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"},{"step":83,"segment":"B2"}] | 49.9361 |
| 2026 | sharp | head_only | cau | frozen_centroid | 0.3333 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 52.0832 |
| 2026 | sharp | head_only | cau | last_active | 0.3316 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 52.0832 |
| 2026 | sharp | head_only | cau | uniform_probability | 0.3958 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 52.0832 |
| 2027 | blurry | head_only | cau | frozen_centroid | 0.3333 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":66,"segment":"C1"},{"step":87,"segment":"B2"}] | 58.4889 |
| 2027 | blurry | head_only | cau | last_active | 0.3351 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":66,"segment":"C1"},{"step":87,"segment":"B2"}] | 58.4889 |
| 2027 | blurry | head_only | cau | uniform_probability | 0.3420 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":66,"segment":"C1"},{"step":87,"segment":"B2"}] | 58.4889 |
| 2027 | sharp | head_only | cau | frozen_centroid | 0.3333 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":53,"segment":"A2"},{"step":66,"segment":"C1"}] | 66.3264 |
| 2027 | sharp | head_only | cau | last_active | 0.3333 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":53,"segment":"A2"},{"step":66,"segment":"C1"}] | 66.3264 |
| 2027 | sharp | head_only | cau | uniform_probability | 0.3403 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":53,"segment":"A2"},{"step":66,"segment":"C1"}] | 66.3264 |
| 2028 | blurry | head_only | cau | frozen_centroid | 0.3264 | 90 | 90 | 3 | [{"step":9,"segment":"A1"},{"step":72,"segment":"C1"}] | 48.8257 |
| 2028 | blurry | head_only | cau | last_active | 0.3438 | 90 | 90 | 3 | [{"step":9,"segment":"A1"},{"step":72,"segment":"C1"}] | 48.8257 |
| 2028 | blurry | head_only | cau | uniform_probability | 0.3438 | 90 | 90 | 3 | [{"step":9,"segment":"A1"},{"step":72,"segment":"C1"}] | 48.8257 |
| 2028 | sharp | head_only | cau | frozen_centroid | 0.3455 | 90 | 90 | 4 | [{"step":9,"segment":"A1"},{"step":20,"segment":"B1"},{"step":48,"segment":"A2"}] | 63.8117 |
| 2028 | sharp | head_only | cau | last_active | 0.3333 | 90 | 90 | 4 | [{"step":9,"segment":"A1"},{"step":20,"segment":"B1"},{"step":48,"segment":"A2"}] | 63.8117 |
| 2028 | sharp | head_only | cau | uniform_probability | 0.3438 | 90 | 90 | 4 | [{"step":9,"segment":"A1"},{"step":20,"segment":"B1"},{"step":48,"segment":"A2"}] | 63.8117 |
| 2026 | blurry | head_only | single | frozen_centroid | 0.3646 | 90 | 90 | 1 | [] | 1.4264 |
| 2026 | blurry | head_only | single | last_active | 0.3646 | 90 | 90 | 1 | [] | 1.4264 |
| 2026 | blurry | head_only | single | uniform_probability | 0.3646 | 90 | 90 | 1 | [] | 1.4264 |
| 2026 | sharp | head_only | single | frozen_centroid | 0.3611 | 90 | 90 | 1 | [] | 1.4536 |
| 2026 | sharp | head_only | single | last_active | 0.3611 | 90 | 90 | 1 | [] | 1.4536 |
| 2026 | sharp | head_only | single | uniform_probability | 0.3611 | 90 | 90 | 1 | [] | 1.4536 |
| 2027 | blurry | head_only | single | frozen_centroid | 0.3542 | 90 | 90 | 1 | [] | 1.4596 |
| 2027 | blurry | head_only | single | last_active | 0.3542 | 90 | 90 | 1 | [] | 1.4596 |
| 2027 | blurry | head_only | single | uniform_probability | 0.3542 | 90 | 90 | 1 | [] | 1.4596 |
| 2027 | sharp | head_only | single | frozen_centroid | 0.3524 | 90 | 90 | 1 | [] | 1.4454 |
| 2027 | sharp | head_only | single | last_active | 0.3524 | 90 | 90 | 1 | [] | 1.4454 |
| 2027 | sharp | head_only | single | uniform_probability | 0.3524 | 90 | 90 | 1 | [] | 1.4454 |
| 2028 | blurry | head_only | single | frozen_centroid | 0.3872 | 90 | 90 | 1 | [] | 1.6442 |
| 2028 | blurry | head_only | single | last_active | 0.3872 | 90 | 90 | 1 | [] | 1.6442 |
| 2028 | blurry | head_only | single | uniform_probability | 0.3872 | 90 | 90 | 1 | [] | 1.6442 |
| 2028 | sharp | head_only | single | frozen_centroid | 0.3802 | 90 | 90 | 1 | [] | 1.5550 |
| 2028 | sharp | head_only | single | last_active | 0.3802 | 90 | 90 | 1 | [] | 1.5550 |
| 2028 | sharp | head_only | single | uniform_probability | 0.3802 | 90 | 90 | 1 | [] | 1.5550 |
| 2026 | blurry | private | cau | frozen_centroid | 0.3299 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 57.3291 |
| 2026 | blurry | private | cau | last_active | 0.3333 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 57.3291 |
| 2026 | blurry | private | cau | uniform_probability | 0.3212 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 57.3291 |
| 2026 | sharp | private | cau | frozen_centroid | 0.3333 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 57.6935 |
| 2026 | sharp | private | cau | last_active | 0.3316 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 57.6935 |
| 2026 | sharp | private | cau | uniform_probability | 0.3941 | 90 | 90 | 3 | [{"step":11,"segment":"A1"},{"step":46,"segment":"A2"}] | 57.6935 |
| 2027 | blurry | private | cau | frozen_centroid | 0.3333 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":66,"segment":"C1"},{"step":87,"segment":"B2"}] | 64.7949 |
| 2027 | blurry | private | cau | last_active | 0.3351 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":66,"segment":"C1"},{"step":87,"segment":"B2"}] | 64.7949 |
| 2027 | blurry | private | cau | uniform_probability | 0.3403 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":66,"segment":"C1"},{"step":87,"segment":"B2"}] | 64.7949 |
| 2027 | sharp | private | cau | frozen_centroid | 0.3385 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":53,"segment":"A2"},{"step":66,"segment":"C1"}] | 72.8004 |
| 2027 | sharp | private | cau | last_active | 0.3333 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":53,"segment":"A2"},{"step":66,"segment":"C1"}] | 72.8004 |
| 2027 | sharp | private | cau | uniform_probability | 0.3316 | 90 | 90 | 5 | [{"step":6,"segment":"A1"},{"step":15,"segment":"A1"},{"step":53,"segment":"A2"},{"step":66,"segment":"C1"}] | 72.8004 |
| 2028 | blurry | private | cau | frozen_centroid | 0.3264 | 90 | 90 | 3 | [{"step":9,"segment":"A1"},{"step":72,"segment":"C1"}] | 53.4697 |
| 2028 | blurry | private | cau | last_active | 0.3420 | 90 | 90 | 3 | [{"step":9,"segment":"A1"},{"step":72,"segment":"C1"}] | 53.4697 |
| 2028 | blurry | private | cau | uniform_probability | 0.3490 | 90 | 90 | 3 | [{"step":9,"segment":"A1"},{"step":72,"segment":"C1"}] | 53.4697 |
| 2028 | sharp | private | cau | frozen_centroid | 0.3438 | 90 | 90 | 4 | [{"step":9,"segment":"A1"},{"step":20,"segment":"B1"},{"step":48,"segment":"A2"}] | 68.5135 |
| 2028 | sharp | private | cau | last_active | 0.3333 | 90 | 90 | 4 | [{"step":9,"segment":"A1"},{"step":20,"segment":"B1"},{"step":48,"segment":"A2"}] | 68.5135 |
| 2028 | sharp | private | cau | uniform_probability | 0.3385 | 90 | 90 | 4 | [{"step":9,"segment":"A1"},{"step":20,"segment":"B1"},{"step":48,"segment":"A2"}] | 68.5135 |
| 2026 | blurry | private | single | frozen_centroid | 0.3750 | 90 | 90 | 1 | [] | 2.2508 |
| 2026 | blurry | private | single | last_active | 0.3750 | 90 | 90 | 1 | [] | 2.2508 |
| 2026 | blurry | private | single | uniform_probability | 0.3750 | 90 | 90 | 1 | [] | 2.2508 |
| 2026 | sharp | private | single | frozen_centroid | 0.3767 | 90 | 90 | 1 | [] | 2.2986 |
| 2026 | sharp | private | single | last_active | 0.3767 | 90 | 90 | 1 | [] | 2.2986 |
| 2026 | sharp | private | single | uniform_probability | 0.3767 | 90 | 90 | 1 | [] | 2.2986 |
| 2027 | blurry | private | single | frozen_centroid | 0.3715 | 90 | 90 | 1 | [] | 2.4189 |
| 2027 | blurry | private | single | last_active | 0.3715 | 90 | 90 | 1 | [] | 2.4189 |
| 2027 | blurry | private | single | uniform_probability | 0.3715 | 90 | 90 | 1 | [] | 2.4189 |
| 2027 | sharp | private | single | frozen_centroid | 0.3559 | 90 | 90 | 1 | [] | 2.4060 |
| 2027 | sharp | private | single | last_active | 0.3559 | 90 | 90 | 1 | [] | 2.4060 |
| 2027 | sharp | private | single | uniform_probability | 0.3559 | 90 | 90 | 1 | [] | 2.4060 |
| 2028 | blurry | private | single | frozen_centroid | 0.3924 | 90 | 90 | 1 | [] | 2.2893 |
| 2028 | blurry | private | single | last_active | 0.3924 | 90 | 90 | 1 | [] | 2.2893 |
| 2028 | blurry | private | single | uniform_probability | 0.3924 | 90 | 90 | 1 | [] | 2.2893 |
| 2028 | sharp | private | single | frozen_centroid | 0.3767 | 90 | 90 | 1 | [] | 2.3092 |
| 2028 | sharp | private | single | last_active | 0.3767 | 90 | 90 | 1 | [] | 2.3092 |
| 2028 | sharp | private | single | uniform_probability | 0.3767 | 90 | 90 | 1 | [] | 2.3092 |

Chance under these balanced development subsets is 1/3. Low accuracy must be interpreted with the fixed single baselines; expansion or retention by itself does not demonstrate useful learning. Seed 2026 is a development pilot; 2027/2028 are transfer checks. Two fresh seeds and one genre schedule do not establish statistical confirmation. No confidence intervals over dependent windows or sharp/blurry variants are reported.
