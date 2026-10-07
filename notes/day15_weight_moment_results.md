# Separate weight and AdamW-state audit

Development-stage matched interventions. Positive contrasts mean lower post-update query loss, lower initial query loss, or more local improvement when resetting the named factor. All conditional cells and interactions are retained. Intervals are descriptive and are not multiplicity-adjusted hypothesis tests.

Verified trajectories: 4/20. Incomplete or unverified attempts: [].

## All marginal effects

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

## All conditional post-update effects

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0062 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0025 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0100 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0018 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0072 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0022 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0066 | nan | nan |
| amazon | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0023 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.2184 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1038 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.2156 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1052 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.2049 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1085 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.1990 | nan | nan |
| amazon | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.1093 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0019 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0014 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0000 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0057 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0008 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0003 | nan | nan |
| amazon | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0000 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1172 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1139 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0026 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0034 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1085 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1021 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0121 | nan | nan |
| amazon | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0124 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0011 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0025 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0017 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0027 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0008 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0007 | nan | nan |
| banking | conditional | reset_head_optimizer | {"reset_head_weights": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.0005 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9113 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.7981 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9142 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": false, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.8032 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9094 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.7961 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.9118 | nan | nan |
| banking | conditional | reset_head_weights | {"reset_head_optimizer": true, "reset_lora_optimizer": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | -0.8010 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0029 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0056 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0006 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": false} | post_update_loss_decrease | 1 | 0.0023 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0055 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": false} | post_update_loss_decrease | 1 | -0.0001 | nan | nan |
| banking | conditional | reset_lora_optimizer | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_weights": true} | post_update_loss_decrease | 1 | 0.0005 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1511 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1484 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0378 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": false, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0374 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.1525 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": false, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.1494 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": false} | post_update_loss_decrease | 1 | -0.0392 | nan | nan |
| banking | conditional | reset_lora_weights | {"reset_head_optimizer": true, "reset_head_weights": true, "reset_lora_optimizer": true} | post_update_loss_decrease | 1 | -0.0386 | nan | nan |

## All marginal two-factor interactions

| regime | kind | factor | condition | metric | n_seeds | mean | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

## Interpretation limits

The probe source is the actual active package, not the best feasible reuse selected retrospectively. This is one-step causal attribution of that probe, not a closed-loop effectiveness study or proof of future plasticity. Resetting a classifier can be a legitimate prediction objective. Five training seeds and fixed development examples do not establish population-level generalization. Broader architectures, source-faithful comparators and stronger natural same-label regimes remain open.
