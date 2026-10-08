# Separate weight and AdamW-state audit

Development-stage matched interventions. Positive contrasts mean lower post-update query loss, lower initial query loss, or more local improvement when resetting the named factor. All conditional cells and interactions are retained. Intervals are descriptive and are not multiplicity-adjusted hypothesis tests.

Verified trajectories: 12/20. Incomplete or unverified attempts: [].

## All marginal effects

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

## All conditional post-update effects

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0007 | -0.0142 | 0.0155 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0072 | -0.0042 | 0.0186 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0036 | -0.0176 | 0.0104 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0065 | -0.0045 | 0.0175 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0072 | 0.0052 | 0.0092 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0012 | -0.0034 | 0.0009 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0067 | 0.0050 | 0.0085 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0013 | -0.0035 | 0.0008 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.1996 | -0.2581 | -0.1412 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0933 | -0.1169 | -0.0696 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.2017 | -0.2557 | -0.1477 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0951 | -0.1174 | -0.0728 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.1931 | -0.2399 | -0.1462 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.1017 | -0.1164 | -0.0870 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.1914 | -0.2356 | -0.1472 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.1029 | -0.1167 | -0.0891 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0026 | -0.0074 | 0.0125 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0019 | 0.0002 | 0.0036 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0005 | -0.0003 | 0.0013 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0000 | -0.0000 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0017 | -0.0104 | 0.0071 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0012 | -0.0001 | 0.0024 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0000 | -0.0006 | 0.0006 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0000 | -0.0001 | 0.0000 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1161 | -0.1595 | -0.0727 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1168 | -0.1620 | -0.0716 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0097 | -0.0261 | 0.0066 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0102 | -0.0257 | 0.0054 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1096 | -0.1469 | -0.0723 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1067 | -0.1460 | -0.0675 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0182 | -0.0320 | -0.0045 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0182 | -0.0315 | -0.0050 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0031 | -0.0117 | 0.0056 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0039 | -0.0081 | 0.0003 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0037 | -0.0123 | 0.0050 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0041 | -0.0084 | 0.0002 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0017 | -0.0081 | 0.0048 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0022 | -0.0063 | 0.0019 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.0018 | -0.0081 | 0.0045 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.0022 | -0.0063 | 0.0019 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9099 | -0.9152 | -0.9046 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.7981 | -0.8107 | -0.7855 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9125 | -0.9177 | -0.9073 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.8033 | -0.8146 | -0.7919 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9085 | -0.9169 | -0.9000 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.7964 | -0.8103 | -0.7825 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | -0.9106 | -0.9187 | -0.9024 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | -0.8014 | -0.8141 | -0.7887 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0027 | 0.0023 | 0.0032 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0056 | 0.0043 | 0.0069 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0002 | -0.0006 | 0.0009 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0005 | 0.0002 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0021 | 0.0017 | 0.0025 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0054 | 0.0042 | 0.0067 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 3 | 0.0001 | -0.0006 | 0.0007 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 3 | 0.0004 | 0.0002 | 0.0007 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1382 | -0.1703 | -0.1061 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1353 | -0.1670 | -0.1037 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0264 | -0.0522 | -0.0006 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0261 | -0.0514 | -0.0009 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.1390 | -0.1703 | -0.1077 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.1357 | -0.1669 | -0.1046 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 3 | -0.0270 | -0.0539 | -0.0000 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 3 | -0.0266 | -0.0529 | -0.0003 |

## All marginal two-factor interactions

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

## Interpretation limits

The probe source is the actual active package, not the best feasible reuse selected retrospectively. This is one-step causal attribution of that probe, not a closed-loop effectiveness study or proof of future plasticity. Resetting a classifier can be a legitimate prediction objective. Five training seeds and fixed development examples do not establish population-level generalization. Broader architectures, source-faithful comparators and stronger natural same-label regimes remain open.
