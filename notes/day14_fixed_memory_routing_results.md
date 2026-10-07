# Learned routing with fixed total training memory

Auxiliary development sensitivity with at most 512 total retained training texts. Both fixed learned rules are reported; no accuracy-selected rule or novel-router claim follows. Reload verification compares nine aggregate sample counts, accuracies and losses, not previously saved per-example prediction vectors.

Completed checkpoints 44/44.

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

| run | regime | architecture | seed | order | rule | fixed_memory_accuracy | per_adapter_memory_accuracy | fixed_minus_per_adapter | fixed_single_accuracy | fixed_minus_single | rank96_accuracy | fixed_minus_rank96 | adaptation_parameters | rank96_parameters | router_training_examples | router_coefficients | normalization_statistics | optimizer_state_bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| day8_amazon_head_only_cau_seed2026_canonical_fixed512 | amazon | head_only | 2026 | canonical | linear_hard | 0.8255 | 0.8255 | 0.0000 | nan | nan | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2026_canonical_fixed512 | amazon | head_only | 2026 | canonical | linear_probability_mixture | 0.8255 | 0.8255 | 0.0000 | nan | nan | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2027_b_first_fixed512 | amazon | head_only | 2027 | b_first | linear_hard | 0.8307 | 0.8307 | 0.0000 | 0.8281 | 0.0026 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2027_b_first_fixed512 | amazon | head_only | 2027 | b_first | linear_probability_mixture | 0.8307 | 0.8307 | 0.0000 | 0.8281 | 0.0026 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2027_canonical_fixed512 | amazon | head_only | 2027 | canonical | linear_hard | 0.7943 | 0.7943 | 0.0000 | 0.7943 | 0.0000 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2027_canonical_fixed512 | amazon | head_only | 2027 | canonical | linear_probability_mixture | 0.7943 | 0.7943 | 0.0000 | 0.7943 | 0.0000 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2028_b_first_fixed512 | amazon | head_only | 2028 | b_first | linear_hard | 0.8099 | 0.8099 | 0.0000 | 0.8151 | -0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2028_b_first_fixed512 | amazon | head_only | 2028 | b_first | linear_probability_mixture | 0.8099 | 0.8099 | 0.0000 | 0.8151 | -0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2028_canonical_fixed512 | amazon | head_only | 2028 | canonical | linear_hard | 0.7995 | 0.7995 | 0.0000 | 0.8125 | -0.0130 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2028_canonical_fixed512 | amazon | head_only | 2028 | canonical | linear_probability_mixture | 0.7995 | 0.7995 | 0.0000 | 0.8125 | -0.0130 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2029_b_first_fixed512 | amazon | head_only | 2029 | b_first | linear_hard | 0.8099 | 0.8099 | 0.0000 | 0.8203 | -0.0104 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2029_b_first_fixed512 | amazon | head_only | 2029 | b_first | linear_probability_mixture | 0.8099 | 0.8099 | 0.0000 | 0.8203 | -0.0104 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2029_canonical_fixed512 | amazon | head_only | 2029 | canonical | linear_hard | 0.7812 | 0.7812 | 0.0000 | 0.8281 | -0.0469 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2029_canonical_fixed512 | amazon | head_only | 2029 | canonical | linear_probability_mixture | 0.7812 | 0.7812 | 0.0000 | 0.8281 | -0.0469 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2030_b_first_fixed512 | amazon | head_only | 2030 | b_first | linear_hard | 0.8047 | 0.8047 | 0.0000 | 0.7812 | 0.0234 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2030_b_first_fixed512 | amazon | head_only | 2030 | b_first | linear_probability_mixture | 0.8047 | 0.8047 | 0.0000 | 0.7812 | 0.0234 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2030_canonical_fixed512 | amazon | head_only | 2030 | canonical | linear_hard | 0.8021 | 0.8021 | 0.0000 | 0.7917 | 0.0104 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2030_canonical_fixed512 | amazon | head_only | 2030 | canonical | linear_probability_mixture | 0.8021 | 0.8021 | 0.0000 | 0.7917 | 0.0104 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2031_b_first_fixed512 | amazon | head_only | 2031 | b_first | linear_hard | 0.8125 | 0.8125 | 0.0000 | 0.8177 | -0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2031_b_first_fixed512 | amazon | head_only | 2031 | b_first | linear_probability_mixture | 0.8125 | 0.8125 | 0.0000 | 0.8177 | -0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2031_canonical_fixed512 | amazon | head_only | 2031 | canonical | linear_hard | 0.7969 | 0.7969 | 0.0000 | 0.7812 | 0.0156 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_head_only_cau_seed2031_canonical_fixed512 | amazon | head_only | 2031 | canonical | linear_probability_mixture | 0.7969 | 0.7969 | 0.0000 | 0.7812 | 0.0156 | nan | nan | 739586 | nan | 512 | 0 | 0 | 4737056 |
| day8_amazon_private_cau_seed2026_canonical_fixed512 | amazon | private | 2026 | canonical | linear_hard | 0.8542 | 0.8542 | 0.0000 | 0.8516 | 0.0026 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2026_canonical_fixed512 | amazon | private | 2026 | canonical | linear_probability_mixture | 0.8542 | 0.8542 | 0.0000 | 0.8516 | 0.0026 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2027_b_first_fixed512 | amazon | private | 2027 | b_first | linear_hard | 0.8594 | 0.8594 | 0.0000 | 0.8568 | 0.0026 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2027_b_first_fixed512 | amazon | private | 2027 | b_first | linear_probability_mixture | 0.8594 | 0.8594 | 0.0000 | 0.8568 | 0.0026 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2027_canonical_fixed512 | amazon | private | 2027 | canonical | linear_hard | 0.8516 | 0.8516 | 0.0000 | 0.8464 | 0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2027_canonical_fixed512 | amazon | private | 2027 | canonical | linear_probability_mixture | 0.8516 | 0.8516 | 0.0000 | 0.8464 | 0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2028_b_first_fixed512 | amazon | private | 2028 | b_first | linear_hard | 0.8385 | 0.8385 | 0.0000 | 0.8542 | -0.0156 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2028_b_first_fixed512 | amazon | private | 2028 | b_first | linear_probability_mixture | 0.8385 | 0.8385 | 0.0000 | 0.8542 | -0.0156 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2028_canonical_fixed512 | amazon | private | 2028 | canonical | linear_hard | 0.8333 | 0.8333 | 0.0000 | 0.8594 | -0.0260 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2028_canonical_fixed512 | amazon | private | 2028 | canonical | linear_probability_mixture | 0.8333 | 0.8333 | 0.0000 | 0.8594 | -0.0260 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2029_b_first_fixed512 | amazon | private | 2029 | b_first | linear_hard | 0.8438 | 0.8438 | 0.0000 | 0.8438 | 0.0000 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2029_b_first_fixed512 | amazon | private | 2029 | b_first | linear_probability_mixture | 0.8438 | 0.8438 | 0.0000 | 0.8438 | 0.0000 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2029_canonical_fixed512 | amazon | private | 2029 | canonical | linear_hard | 0.7083 | 0.7344 | -0.0260 | 0.8542 | -0.1458 | nan | nan | 1479172 | nan | 464 | 769 | 1536 | 11833600 |
| day8_amazon_private_cau_seed2029_canonical_fixed512 | amazon | private | 2029 | canonical | linear_probability_mixture | 0.7526 | 0.7604 | -0.0078 | 0.8542 | -0.1016 | nan | nan | 1479172 | nan | 464 | 769 | 1536 | 11833600 |
| day8_amazon_private_cau_seed2030_b_first_fixed512 | amazon | private | 2030 | b_first | linear_hard | 0.8620 | 0.8620 | 0.0000 | 0.8568 | 0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2030_b_first_fixed512 | amazon | private | 2030 | b_first | linear_probability_mixture | 0.8620 | 0.8620 | 0.0000 | 0.8568 | 0.0052 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2030_canonical_fixed512 | amazon | private | 2030 | canonical | linear_hard | 0.8021 | 0.8021 | 0.0000 | 0.8438 | -0.0417 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2030_canonical_fixed512 | amazon | private | 2030 | canonical | linear_probability_mixture | 0.8021 | 0.8021 | 0.0000 | 0.8438 | -0.0417 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2031_b_first_fixed512 | amazon | private | 2031 | b_first | linear_hard | 0.8385 | 0.8385 | 0.0000 | 0.8542 | -0.0156 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2031_b_first_fixed512 | amazon | private | 2031 | b_first | linear_probability_mixture | 0.8385 | 0.8385 | 0.0000 | 0.8542 | -0.0156 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2031_canonical_fixed512 | amazon | private | 2031 | canonical | linear_hard | 0.8490 | 0.8490 | 0.0000 | 0.8411 | 0.0078 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_amazon_private_cau_seed2031_canonical_fixed512 | amazon | private | 2031 | canonical | linear_probability_mixture | 0.8490 | 0.8490 | 0.0000 | 0.8411 | 0.0078 | nan | nan | 739586 | nan | 512 | 0 | 0 | 5916800 |
| day8_banking_head_only_cau_seed2026_canonical_fixed512 | banking | head_only | 2026 | canonical | linear_hard | 0.1650 | 0.1789 | -0.0139 | nan | nan | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2026_canonical_fixed512 | banking | head_only | 2026 | canonical | linear_probability_mixture | 0.1654 | 0.1715 | -0.0062 | nan | nan | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2027_b_first_fixed512 | banking | head_only | 2027 | b_first | linear_hard | 0.1474 | 0.1281 | 0.0193 | 0.0744 | 0.0730 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2027_b_first_fixed512 | banking | head_only | 2027 | b_first | linear_probability_mixture | 0.1323 | 0.1146 | 0.0178 | 0.0744 | 0.0579 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2027_canonical_fixed512 | banking | head_only | 2027 | canonical | linear_hard | 0.1535 | 0.1534 | 0.0002 | 0.1435 | 0.0100 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2027_canonical_fixed512 | banking | head_only | 2027 | canonical | linear_probability_mixture | 0.1584 | 0.1474 | 0.0110 | 0.1435 | 0.0149 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2028_b_first_fixed512 | banking | head_only | 2028 | b_first | linear_hard | 0.1172 | 0.1228 | -0.0056 | 0.1839 | -0.0668 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2028_b_first_fixed512 | banking | head_only | 2028 | b_first | linear_probability_mixture | 0.1218 | 0.1203 | 0.0015 | 0.1839 | -0.0622 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2028_canonical_fixed512 | banking | head_only | 2028 | canonical | linear_hard | 0.1743 | 0.1862 | -0.0119 | 0.0633 | 0.1110 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2028_canonical_fixed512 | banking | head_only | 2028 | canonical | linear_probability_mixture | 0.1799 | 0.1814 | -0.0015 | 0.0633 | 0.1166 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2029_b_first_fixed512 | banking | head_only | 2029 | b_first | linear_hard | 0.2068 | 0.2056 | 0.0012 | 0.1121 | 0.0947 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2029_b_first_fixed512 | banking | head_only | 2029 | b_first | linear_probability_mixture | 0.2014 | 0.2064 | -0.0050 | 0.1121 | 0.0893 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2029_canonical_fixed512 | banking | head_only | 2029 | canonical | linear_hard | 0.2256 | 0.2396 | -0.0140 | 0.1548 | 0.0708 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2029_canonical_fixed512 | banking | head_only | 2029 | canonical | linear_probability_mixture | 0.2197 | 0.2242 | -0.0046 | 0.1548 | 0.0649 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2030_b_first_fixed512 | banking | head_only | 2030 | b_first | linear_hard | 0.1141 | 0.1205 | -0.0064 | 0.1352 | -0.0211 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2030_b_first_fixed512 | banking | head_only | 2030 | b_first | linear_probability_mixture | 0.1162 | 0.1180 | -0.0018 | 0.1352 | -0.0190 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2030_canonical_fixed512 | banking | head_only | 2030 | canonical | linear_hard | 0.1113 | 0.1251 | -0.0138 | 0.1046 | 0.0067 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2030_canonical_fixed512 | banking | head_only | 2030 | canonical | linear_probability_mixture | 0.1131 | 0.1249 | -0.0118 | 0.1046 | 0.0085 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2031_b_first_fixed512 | banking | head_only | 2031 | b_first | linear_hard | 0.1648 | 0.1735 | -0.0087 | 0.0885 | 0.0763 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2031_b_first_fixed512 | banking | head_only | 2031 | b_first | linear_probability_mixture | 0.1638 | 0.1684 | -0.0046 | 0.0885 | 0.0753 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2031_canonical_fixed512 | banking | head_only | 2031 | canonical | linear_hard | 0.1658 | 0.1770 | -0.0112 | 0.1750 | -0.0093 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_head_only_cau_seed2031_canonical_fixed512 | banking | head_only | 2031 | canonical | linear_probability_mixture | 0.1666 | 0.1764 | -0.0098 | 0.1750 | -0.0084 | nan | nan | 2391783 | nan | 510 | 2307 | 1536 | 15595368 |
| day8_banking_private_cau_seed2026_canonical_fixed512 | banking | private | 2026 | canonical | linear_hard | 0.2189 | 0.2328 | -0.0139 | 0.1693 | 0.0496 | 0.0679 | 0.1510 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2026_canonical_fixed512 | banking | private | 2026 | canonical | linear_probability_mixture | 0.2163 | 0.2193 | -0.0029 | 0.1693 | 0.0470 | 0.0679 | 0.1484 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2027_b_first_fixed512 | banking | private | 2027 | b_first | linear_hard | 0.2180 | 0.1987 | 0.0193 | 0.1136 | 0.1044 | 0.0183 | 0.1997 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2027_b_first_fixed512 | banking | private | 2027 | b_first | linear_probability_mixture | 0.2114 | 0.1887 | 0.0226 | 0.1136 | 0.0978 | 0.0183 | 0.1930 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2027_canonical_fixed512 | banking | private | 2027 | canonical | linear_hard | 0.2542 | 0.2618 | -0.0076 | 0.2131 | 0.0411 | 0.0677 | 0.1865 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2027_canonical_fixed512 | banking | private | 2027 | canonical | linear_probability_mixture | 0.2532 | 0.2576 | -0.0044 | 0.2131 | 0.0401 | 0.0677 | 0.1855 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2028_b_first_fixed512 | banking | private | 2028 | b_first | linear_hard | 0.1354 | 0.1451 | -0.0097 | 0.1550 | -0.0196 | 0.0355 | 0.0999 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2028_b_first_fixed512 | banking | private | 2028 | b_first | linear_probability_mixture | 0.1398 | 0.1471 | -0.0073 | 0.1550 | -0.0151 | 0.0355 | 0.1043 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2028_canonical_fixed512 | banking | private | 2028 | canonical | linear_hard | 0.2264 | 0.2419 | -0.0155 | 0.0820 | 0.1444 | 0.0237 | 0.2027 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2028_canonical_fixed512 | banking | private | 2028 | canonical | linear_probability_mixture | 0.2375 | 0.2383 | -0.0008 | 0.0820 | 0.1555 | 0.0237 | 0.2138 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2029_b_first_fixed512 | banking | private | 2029 | b_first | linear_hard | 0.2313 | 0.2259 | 0.0054 | 0.0820 | 0.1493 | 0.1443 | 0.0869 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2029_b_first_fixed512 | banking | private | 2029 | b_first | linear_probability_mixture | 0.2272 | 0.2256 | 0.0016 | 0.0820 | 0.1452 | 0.1443 | 0.0828 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2029_canonical_fixed512 | banking | private | 2029 | canonical | linear_hard | 0.2568 | 0.2731 | -0.0162 | 0.2200 | 0.0368 | 0.0584 | 0.1984 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2029_canonical_fixed512 | banking | private | 2029 | canonical | linear_probability_mixture | 0.2587 | 0.2666 | -0.0079 | 0.2200 | 0.0386 | 0.0584 | 0.2002 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2030_b_first_fixed512 | banking | private | 2030 | b_first | linear_hard | 0.2418 | 0.2526 | -0.0108 | 0.1513 | 0.0905 | 0.0550 | 0.1868 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2030_b_first_fixed512 | banking | private | 2030 | b_first | linear_probability_mixture | 0.2507 | 0.2559 | -0.0053 | 0.1513 | 0.0994 | 0.0550 | 0.1957 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2030_canonical_fixed512 | banking | private | 2030 | canonical | linear_hard | 0.2298 | 0.2398 | -0.0100 | 0.2359 | -0.0061 | 0.1882 | 0.0416 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2030_canonical_fixed512 | banking | private | 2030 | canonical | linear_probability_mixture | 0.2314 | 0.2407 | -0.0093 | 0.2359 | -0.0045 | 0.1882 | 0.0433 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2031_b_first_fixed512 | banking | private | 2031 | b_first | linear_hard | 0.2112 | 0.2188 | -0.0076 | 0.1616 | 0.0496 | 0.0367 | 0.1745 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2031_b_first_fixed512 | banking | private | 2031 | b_first | linear_probability_mixture | 0.2068 | 0.2111 | -0.0043 | 0.1616 | 0.0453 | 0.0367 | 0.1702 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2031_canonical_fixed512 | banking | private | 2031 | canonical | linear_hard | 0.1745 | 0.1811 | -0.0067 | 0.2298 | -0.0553 | 0.0705 | 0.1040 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |
| day8_banking_private_cau_seed2031_canonical_fixed512 | banking | private | 2031 | canonical | linear_probability_mixture | 0.1684 | 0.1726 | -0.0042 | 0.2298 | -0.0614 | 0.0705 | 0.0979 | 2391783 | 2419277.0000 | 510 | 2307 | 1536 | 19134600 |

Stored model parameters, optimizer state and router coefficients are reported separately from the 512-text budget. Rank 96 controls a declared three-package storage scale; different package counts and classifier multiplicity limit parameter-match claims. All intervals are descriptive over at most five seeds, with paired orders averaged first and fixed development examples. The extension was added after original routing outcomes and requires later frozen complete-method confirmation.
