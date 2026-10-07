# Separate weight and AdamW-state audit

Development-stage matched interventions. Positive contrasts mean lower post-update query loss, lower initial query loss, or more local improvement when resetting the named factor. All conditional cells and interactions are retained. Intervals are descriptive and are not multiplicity-adjusted hypothesis tests.

Verified trajectories: 8/20. Incomplete or unverified attempts: [].

## All marginal effects

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

## All conditional post-update effects

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0008 | -0.0692 | 0.0675 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0050 | -0.0274 | 0.0374 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0047 | -0.0715 | 0.0621 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0044 | -0.0280 | 0.0368 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0068 | 0.0022 | 0.0114 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0015 | -0.0113 | 0.0083 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0064 | 0.0035 | 0.0093 |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0015 | -0.0114 | 0.0083 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1958 | -0.4824 | 0.0908 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0973 | -0.1803 | -0.0142 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1961 | -0.4435 | 0.0513 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0987 | -0.1809 | -0.0165 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1881 | -0.4017 | 0.0255 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.1037 | -0.1642 | -0.0432 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.1850 | -0.3627 | -0.0074 |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.1046 | -0.1642 | -0.0450 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0009 | -0.0346 | 0.0363 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0015 | 0.0004 | 0.0025 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0005 | -0.0033 | 0.0043 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0000 | -0.0001 | 0.0001 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0030 | -0.0369 | 0.0308 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0009 | -0.0002 | 0.0019 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0001 | -0.0020 | 0.0022 |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0000 | -0.0002 | 0.0001 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1077 | -0.2288 | 0.0135 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.1071 | -0.1938 | -0.0203 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0091 | -0.0915 | 0.0733 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0096 | -0.0881 | 0.0689 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1018 | -0.1870 | -0.0167 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0979 | -0.1503 | -0.0456 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0174 | -0.0854 | 0.0506 |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0175 | -0.0832 | 0.0482 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0041 | -0.0424 | 0.0342 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0042 | -0.0250 | 0.0166 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0047 | -0.0430 | 0.0336 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0044 | -0.0254 | 0.0167 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0018 | -0.0347 | 0.0312 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0021 | -0.0230 | 0.0187 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0019 | -0.0340 | 0.0303 |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.0022 | -0.0231 | 0.0188 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9094 | -0.9342 | -0.8846 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.7956 | -0.8279 | -0.7632 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9121 | -0.9377 | -0.8865 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.8010 | -0.8291 | -0.7728 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9071 | -0.9372 | -0.8769 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.7935 | -0.8258 | -0.7613 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.9093 | -0.9410 | -0.8776 |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | -0.7987 | -0.8271 | -0.7704 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0028 | 0.0007 | 0.0048 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0059 | 0.0027 | 0.0091 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0000 | -0.0012 | 0.0012 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0005 | -0.0005 | 0.0014 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 2 | 0.0022 | 0.0001 | 0.0042 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0057 | 0.0028 | 0.0086 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 2 | -0.0001 | -0.0006 | 0.0004 |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 2 | 0.0005 | -0.0005 | 0.0015 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1447 | -0.2262 | -0.0631 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.1415 | -0.2283 | -0.0548 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0308 | -0.1199 | 0.0582 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0304 | -0.1197 | 0.0590 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.1447 | -0.2438 | -0.0457 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.1412 | -0.2452 | -0.0372 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 2 | -0.0312 | -0.1324 | 0.0700 |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 2 | -0.0306 | -0.1313 | 0.0700 |

## All marginal two-factor interactions

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

## Interpretation limits

The probe source is the actual active package, not the best feasible reuse selected retrospectively. This is one-step causal attribution of that probe, not a closed-loop effectiveness study or proof of future plasticity. Resetting a classifier can be a legitimate prediction objective. Five training seeds and fixed development examples do not establish population-level generalization. Broader architectures, source-faithful comparators and stronger natural same-label regimes remain open.
