# Secondary deployed-retention development analysis

Added after primary development outcomes. Uses saved full-output-space predictions, all three original deployment rules, both orders, both available regimes and both pilot-selected static ranks. No new training, rate selection, or official-test access. The learned routers have only final fixed-memory reload measurements; temporal retention is unavailable for those rules and is not imputed.

Definitions: final concept-macro accuracy; the mean of five seen-concept checkpoint accuracies; the maximum accuracy at checkpoints after a concept first finishes training minus its final accuracy, averaged over concepts; and final minus first-exposure accuracy, averaged over concepts. The last statistic includes recurrence learning and is not standard nonrecurring-task backward transfer. Positive maximum-checkpoint drop means more loss from the observed peak; positive final-minus-first means improvement. The peak is a defined evaluation summary, not a selected predictor. Checkpoints do not constitute independent samples.

## All paired comparisons

| regime | comparison | rule | metric | seed_clusters | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | adaptive_minus_static_rank8_frozen | frozen_centroid | final_macro_accuracy | 5 | -0.0182 | -0.0449 | 0.0085 |
| amazon | adaptive_minus_static_rank8_frozen | frozen_centroid | final_minus_first_exposure | 5 | -0.0161 | -0.0447 | 0.0124 |
| amazon | adaptive_minus_static_rank8_frozen | frozen_centroid | maximum_seen_checkpoint_drop | 5 | 0.0094 | -0.0146 | 0.0333 |
| amazon | adaptive_minus_static_rank8_frozen | frozen_centroid | mean_seen_checkpoint_accuracy | 5 | -0.0044 | -0.0099 | 0.0011 |
| amazon | adaptive_minus_static_rank8_frozen | last_active | final_macro_accuracy | 5 | -0.0427 | -0.1350 | 0.0496 |
| amazon | adaptive_minus_static_rank8_frozen | last_active | final_minus_first_exposure | 5 | -0.0406 | -0.1365 | 0.0553 |
| amazon | adaptive_minus_static_rank8_frozen | last_active | maximum_seen_checkpoint_drop | 5 | 0.0339 | -0.0576 | 0.1253 |
| amazon | adaptive_minus_static_rank8_frozen | last_active | mean_seen_checkpoint_accuracy | 5 | -0.0093 | -0.0259 | 0.0073 |
| amazon | adaptive_minus_static_rank8_frozen | uniform_probability | final_macro_accuracy | 5 | -0.0117 | -0.0255 | 0.0020 |
| amazon | adaptive_minus_static_rank8_frozen | uniform_probability | final_minus_first_exposure | 5 | -0.0096 | -0.0215 | 0.0023 |
| amazon | adaptive_minus_static_rank8_frozen | uniform_probability | maximum_seen_checkpoint_drop | 5 | 0.0029 | -0.0047 | 0.0104 |
| amazon | adaptive_minus_static_rank8_frozen | uniform_probability | mean_seen_checkpoint_accuracy | 5 | -0.0031 | -0.0083 | 0.0021 |
| banking | adaptive_minus_static_rank8_frozen | frozen_centroid | final_macro_accuracy | 5 | -0.0016 | -0.0341 | 0.0308 |
| banking | adaptive_minus_static_rank8_frozen | frozen_centroid | final_minus_first_exposure | 5 | -0.0738 | -0.1021 | -0.0455 |
| banking | adaptive_minus_static_rank8_frozen | frozen_centroid | maximum_seen_checkpoint_drop | 5 | -0.0551 | -0.0957 | -0.0145 |
| banking | adaptive_minus_static_rank8_frozen | frozen_centroid | mean_seen_checkpoint_accuracy | 5 | -0.0056 | -0.0290 | 0.0177 |
| banking | adaptive_minus_static_rank8_frozen | last_active | final_macro_accuracy | 5 | -0.0601 | -0.1060 | -0.0142 |
| banking | adaptive_minus_static_rank8_frozen | last_active | final_minus_first_exposure | 5 | -0.1772 | -0.2414 | -0.1130 |
| banking | adaptive_minus_static_rank8_frozen | last_active | maximum_seen_checkpoint_drop | 5 | 0.0979 | 0.0416 | 0.1542 |
| banking | adaptive_minus_static_rank8_frozen | last_active | mean_seen_checkpoint_accuracy | 5 | -0.0379 | -0.0586 | -0.0171 |
| banking | adaptive_minus_static_rank8_frozen | uniform_probability | final_macro_accuracy | 5 | -0.0335 | -0.0835 | 0.0166 |
| banking | adaptive_minus_static_rank8_frozen | uniform_probability | final_minus_first_exposure | 5 | -0.0391 | -0.0889 | 0.0108 |
| banking | adaptive_minus_static_rank8_frozen | uniform_probability | maximum_seen_checkpoint_drop | 5 | -0.0403 | -0.0804 | -0.0001 |
| banking | adaptive_minus_static_rank8_frozen | uniform_probability | mean_seen_checkpoint_accuracy | 5 | -0.0271 | -0.0515 | -0.0026 |
| banking | adaptive_minus_static_rank8_tuned | frozen_centroid | final_macro_accuracy | 5 | -0.0016 | -0.0341 | 0.0308 |
| banking | adaptive_minus_static_rank8_tuned | frozen_centroid | final_minus_first_exposure | 5 | -0.0738 | -0.1021 | -0.0455 |
| banking | adaptive_minus_static_rank8_tuned | frozen_centroid | maximum_seen_checkpoint_drop | 5 | -0.0551 | -0.0957 | -0.0145 |
| banking | adaptive_minus_static_rank8_tuned | frozen_centroid | mean_seen_checkpoint_accuracy | 5 | -0.0056 | -0.0290 | 0.0177 |
| banking | adaptive_minus_static_rank8_tuned | last_active | final_macro_accuracy | 5 | -0.0601 | -0.1060 | -0.0142 |
| banking | adaptive_minus_static_rank8_tuned | last_active | final_minus_first_exposure | 5 | -0.1772 | -0.2414 | -0.1130 |
| banking | adaptive_minus_static_rank8_tuned | last_active | maximum_seen_checkpoint_drop | 5 | 0.0979 | 0.0416 | 0.1542 |
| banking | adaptive_minus_static_rank8_tuned | last_active | mean_seen_checkpoint_accuracy | 5 | -0.0379 | -0.0586 | -0.0171 |
| banking | adaptive_minus_static_rank8_tuned | uniform_probability | final_macro_accuracy | 5 | -0.0335 | -0.0835 | 0.0166 |
| banking | adaptive_minus_static_rank8_tuned | uniform_probability | final_minus_first_exposure | 5 | -0.0391 | -0.0889 | 0.0108 |
| banking | adaptive_minus_static_rank8_tuned | uniform_probability | maximum_seen_checkpoint_drop | 5 | -0.0403 | -0.0804 | -0.0001 |
| banking | adaptive_minus_static_rank8_tuned | uniform_probability | mean_seen_checkpoint_accuracy | 5 | -0.0271 | -0.0515 | -0.0026 |
| banking | adaptive_minus_static_rank96_tuned | frozen_centroid | final_macro_accuracy | 5 | 0.0812 | 0.0441 | 0.1184 |
| banking | adaptive_minus_static_rank96_tuned | frozen_centroid | final_minus_first_exposure | 5 | 0.0329 | -0.0204 | 0.0862 |
| banking | adaptive_minus_static_rank96_tuned | frozen_centroid | maximum_seen_checkpoint_drop | 5 | -0.0413 | -0.0659 | -0.0168 |
| banking | adaptive_minus_static_rank96_tuned | frozen_centroid | mean_seen_checkpoint_accuracy | 5 | 0.0542 | 0.0341 | 0.0742 |
| banking | adaptive_minus_static_rank96_tuned | last_active | final_macro_accuracy | 5 | 0.0227 | -0.0116 | 0.0570 |
| banking | adaptive_minus_static_rank96_tuned | last_active | final_minus_first_exposure | 5 | -0.0705 | -0.1355 | -0.0055 |
| banking | adaptive_minus_static_rank96_tuned | last_active | maximum_seen_checkpoint_drop | 5 | 0.1117 | 0.0623 | 0.1610 |
| banking | adaptive_minus_static_rank96_tuned | last_active | mean_seen_checkpoint_accuracy | 5 | 0.0219 | 0.0105 | 0.0334 |
| banking | adaptive_minus_static_rank96_tuned | uniform_probability | final_macro_accuracy | 5 | 0.0494 | -0.0274 | 0.1262 |
| banking | adaptive_minus_static_rank96_tuned | uniform_probability | final_minus_first_exposure | 5 | 0.0677 | -0.0100 | 0.1453 |
| banking | adaptive_minus_static_rank96_tuned | uniform_probability | maximum_seen_checkpoint_drop | 5 | -0.0265 | -0.0547 | 0.0016 |
| banking | adaptive_minus_static_rank96_tuned | uniform_probability | mean_seen_checkpoint_accuracy | 5 | 0.0327 | -0.0057 | 0.0712 |

All intervals are descriptive over training seeds with orders averaged first. Fixed development examples were repeatedly examined. These secondary summaries neither establish a formal protected-memory guarantee nor change the primary final-accuracy selection objective.

