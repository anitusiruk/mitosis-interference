# Auxiliary learned routing diagnostic

Introduced after the Day-5 routing failure and frozen before these outcomes. A standardized linear gate learns past adapter assignments from reservoir texts only. Neither gold class labels nor true genre/concept identities are router fitting targets. Both hard selection and probability mixture are reported; no development winner is selected. Every included checkpoint first passed equality of nine aggregate sample counts and accuracies. Original per-example predictions were not stored; the provenance field original_prediction_agreement records this weaker aggregate check. Official tests remain unused.

Completed learner checkpoints: 110.

## Day-5 development checkpoints

| run | rule | macro_accuracy |
| --- | --- | --- |
| day5_amazon_head_only_cau_seed2026 | linear_hard | 0.8255 |
| day5_amazon_head_only_cau_seed2026 | linear_probability_mixture | 0.8255 |
| day5_amazon_private_cau_seed2026 | linear_hard | 0.8542 |
| day5_amazon_private_cau_seed2026 | linear_probability_mixture | 0.8542 |
| day5_amazon_private_single_seed2026 | linear_hard | 0.8516 |
| day5_amazon_private_single_seed2026 | linear_probability_mixture | 0.8516 |
| day5_banking_head_only_cau_seed2026 | linear_hard | 0.1789 |
| day5_banking_head_only_cau_seed2026 | linear_probability_mixture | 0.1715 |
| day5_banking_private_cau_seed2026 | linear_hard | 0.2328 |
| day5_banking_private_cau_seed2026 | linear_probability_mixture | 0.2193 |
| day5_banking_private_single_seed2026 | linear_hard | 0.1693 |
| day5_banking_private_single_seed2026 | linear_probability_mixture | 0.1693 |

## Auxiliary seed-cluster differences

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

Descriptive intervals average both paired orders within each seed, with maximum five independent seed clusters. This added routing rule was not a primary outcome of the earlier frozen seed batch.

## Full results and added resources

| run | rule | macro_accuracy | router_training_examples | fit_and_training_feature_seconds | classifier_and_route_inference_seconds | learned_router_coefficients | normalization_statistics |
| --- | --- | --- | --- | --- | --- | --- | --- |
| day5_amazon_head_only_cau_seed2026 | linear_hard | 0.8255 | 512 | 0.1978 | 0.1522 | 0 | 0 |
| day5_amazon_head_only_cau_seed2026 | linear_probability_mixture | 0.8255 | 512 | 0.1978 | 0.1522 | 0 | 0 |
| day5_amazon_private_cau_seed2026 | linear_hard | 0.8542 | 512 | 0.1980 | 0.1458 | 0 | 0 |
| day5_amazon_private_cau_seed2026 | linear_probability_mixture | 0.8542 | 512 | 0.1980 | 0.1458 | 0 | 0 |
| day5_amazon_private_single_seed2026 | linear_hard | 0.8516 | 512 | 0.1930 | 0.1454 | 0 | 0 |
| day5_amazon_private_single_seed2026 | linear_probability_mixture | 0.8516 | 512 | 0.1930 | 0.1454 | 0 | 0 |
| day5_banking_head_only_cau_seed2026 | linear_hard | 0.1789 | 1255 | 0.5664 | 0.4794 | 2307 | 1536 |
| day5_banking_head_only_cau_seed2026 | linear_probability_mixture | 0.1715 | 1255 | 0.5664 | 0.4794 | 2307 | 1536 |
| day5_banking_private_cau_seed2026 | linear_hard | 0.2328 | 1255 | 0.6135 | 0.5552 | 2307 | 1536 |
| day5_banking_private_cau_seed2026 | linear_probability_mixture | 0.2193 | 1255 | 0.6135 | 0.5552 | 2307 | 1536 |
| day5_banking_private_single_seed2026 | linear_hard | 0.1693 | 512 | 0.1494 | 0.2512 | 0 | 0 |
| day5_banking_private_single_seed2026 | linear_probability_mixture | 0.1693 | 512 | 0.1494 | 0.2512 | 0 | 0 |
| day6_amazon_head_only_cau_seed2027_b_first | linear_hard | 0.8307 | 512 | 0.1975 | 0.1455 | 0 | 0 |
| day6_amazon_head_only_cau_seed2027_b_first | linear_probability_mixture | 0.8307 | 512 | 0.1975 | 0.1455 | 0 | 0 |
| day6_amazon_head_only_cau_seed2027_canonical | linear_hard | 0.7943 | 512 | 0.1907 | 0.1515 | 0 | 0 |
| day6_amazon_head_only_cau_seed2027_canonical | linear_probability_mixture | 0.7943 | 512 | 0.1907 | 0.1515 | 0 | 0 |
| day6_amazon_head_only_cau_seed2028_b_first | linear_hard | 0.8099 | 512 | 0.2086 | 0.1540 | 0 | 0 |
| day6_amazon_head_only_cau_seed2028_b_first | linear_probability_mixture | 0.8099 | 512 | 0.2086 | 0.1540 | 0 | 0 |
| day6_amazon_head_only_cau_seed2028_canonical | linear_hard | 0.7995 | 512 | 0.2064 | 0.1532 | 0 | 0 |
| day6_amazon_head_only_cau_seed2028_canonical | linear_probability_mixture | 0.7995 | 512 | 0.2064 | 0.1532 | 0 | 0 |
| day6_amazon_head_only_cau_seed2029_b_first | linear_hard | 0.8099 | 512 | 0.1960 | 0.1453 | 0 | 0 |
| day6_amazon_head_only_cau_seed2029_b_first | linear_probability_mixture | 0.8099 | 512 | 0.1960 | 0.1453 | 0 | 0 |
| day6_amazon_head_only_cau_seed2029_canonical | linear_hard | 0.7812 | 512 | 0.2018 | 0.1466 | 0 | 0 |
| day6_amazon_head_only_cau_seed2029_canonical | linear_probability_mixture | 0.7812 | 512 | 0.2018 | 0.1466 | 0 | 0 |
| day6_amazon_head_only_cau_seed2030_b_first | linear_hard | 0.8047 | 512 | 0.2021 | 0.1455 | 0 | 0 |
| day6_amazon_head_only_cau_seed2030_b_first | linear_probability_mixture | 0.8047 | 512 | 0.2021 | 0.1455 | 0 | 0 |
| day6_amazon_head_only_cau_seed2030_canonical | linear_hard | 0.8021 | 512 | 0.2074 | 0.1471 | 0 | 0 |
| day6_amazon_head_only_cau_seed2030_canonical | linear_probability_mixture | 0.8021 | 512 | 0.2074 | 0.1471 | 0 | 0 |
| day6_amazon_head_only_cau_seed2031_b_first | linear_hard | 0.8125 | 512 | 0.1923 | 0.1403 | 0 | 0 |
| day6_amazon_head_only_cau_seed2031_b_first | linear_probability_mixture | 0.8125 | 512 | 0.1923 | 0.1403 | 0 | 0 |
| day6_amazon_head_only_cau_seed2031_canonical | linear_hard | 0.7969 | 512 | 0.2020 | 0.1441 | 0 | 0 |
| day6_amazon_head_only_cau_seed2031_canonical | linear_probability_mixture | 0.7969 | 512 | 0.2020 | 0.1441 | 0 | 0 |
| day6_amazon_head_only_single_seed2027_b_first | linear_hard | 0.8281 | 512 | 0.1901 | 0.1408 | 0 | 0 |
| day6_amazon_head_only_single_seed2027_b_first | linear_probability_mixture | 0.8281 | 512 | 0.1901 | 0.1408 | 0 | 0 |
| day6_amazon_head_only_single_seed2027_canonical | linear_hard | 0.7943 | 512 | 0.1921 | 0.1404 | 0 | 0 |
| day6_amazon_head_only_single_seed2027_canonical | linear_probability_mixture | 0.7943 | 512 | 0.1921 | 0.1404 | 0 | 0 |
| day6_amazon_head_only_single_seed2028_b_first | linear_hard | 0.8151 | 512 | 0.2118 | 0.1573 | 0 | 0 |
| day6_amazon_head_only_single_seed2028_b_first | linear_probability_mixture | 0.8151 | 512 | 0.2118 | 0.1573 | 0 | 0 |
| day6_amazon_head_only_single_seed2028_canonical | linear_hard | 0.8125 | 512 | 0.2000 | 0.1458 | 0 | 0 |
| day6_amazon_head_only_single_seed2028_canonical | linear_probability_mixture | 0.8125 | 512 | 0.2000 | 0.1458 | 0 | 0 |
| day6_amazon_head_only_single_seed2029_b_first | linear_hard | 0.8203 | 512 | 0.2009 | 0.1478 | 0 | 0 |
| day6_amazon_head_only_single_seed2029_b_first | linear_probability_mixture | 0.8203 | 512 | 0.2009 | 0.1478 | 0 | 0 |
| day6_amazon_head_only_single_seed2029_canonical | linear_hard | 0.8281 | 512 | 0.2059 | 0.1501 | 0 | 0 |
| day6_amazon_head_only_single_seed2029_canonical | linear_probability_mixture | 0.8281 | 512 | 0.2059 | 0.1501 | 0 | 0 |
| day6_amazon_head_only_single_seed2030_b_first | linear_hard | 0.7812 | 512 | 0.2118 | 0.1555 | 0 | 0 |
| day6_amazon_head_only_single_seed2030_b_first | linear_probability_mixture | 0.7812 | 512 | 0.2118 | 0.1555 | 0 | 0 |
| day6_amazon_head_only_single_seed2030_canonical | linear_hard | 0.7917 | 512 | 0.2132 | 0.1516 | 0 | 0 |
| day6_amazon_head_only_single_seed2030_canonical | linear_probability_mixture | 0.7917 | 512 | 0.2132 | 0.1516 | 0 | 0 |
| day6_amazon_head_only_single_seed2031_b_first | linear_hard | 0.8177 | 512 | 0.2050 | 0.1437 | 0 | 0 |
| day6_amazon_head_only_single_seed2031_b_first | linear_probability_mixture | 0.8177 | 512 | 0.2050 | 0.1437 | 0 | 0 |
| day6_amazon_head_only_single_seed2031_canonical | linear_hard | 0.7812 | 512 | 0.2062 | 0.1557 | 0 | 0 |
| day6_amazon_head_only_single_seed2031_canonical | linear_probability_mixture | 0.7812 | 512 | 0.2062 | 0.1557 | 0 | 0 |
| day6_amazon_private_cau_seed2027_b_first | linear_hard | 0.8594 | 512 | 0.1981 | 0.1524 | 0 | 0 |
| day6_amazon_private_cau_seed2027_b_first | linear_probability_mixture | 0.8594 | 512 | 0.1981 | 0.1524 | 0 | 0 |
| day6_amazon_private_cau_seed2027_canonical | linear_hard | 0.8516 | 512 | 0.1992 | 0.1423 | 0 | 0 |
| day6_amazon_private_cau_seed2027_canonical | linear_probability_mixture | 0.8516 | 512 | 0.1992 | 0.1423 | 0 | 0 |
| day6_amazon_private_cau_seed2028_b_first | linear_hard | 0.8385 | 512 | 0.1952 | 0.1421 | 0 | 0 |
| day6_amazon_private_cau_seed2028_b_first | linear_probability_mixture | 0.8385 | 512 | 0.1952 | 0.1421 | 0 | 0 |
| day6_amazon_private_cau_seed2028_canonical | linear_hard | 0.8333 | 512 | 0.1944 | 0.1385 | 0 | 0 |
| day6_amazon_private_cau_seed2028_canonical | linear_probability_mixture | 0.8333 | 512 | 0.1944 | 0.1385 | 0 | 0 |
| day6_amazon_private_cau_seed2029_b_first | linear_hard | 0.8438 | 512 | 0.1923 | 0.1442 | 0 | 0 |
| day6_amazon_private_cau_seed2029_b_first | linear_probability_mixture | 0.8438 | 512 | 0.1923 | 0.1442 | 0 | 0 |
| day6_amazon_private_cau_seed2029_canonical | linear_hard | 0.7344 | 736 | 0.3871 | 0.2538 | 769 | 1536 |
| day6_amazon_private_cau_seed2029_canonical | linear_probability_mixture | 0.7604 | 736 | 0.3871 | 0.2538 | 769 | 1536 |
| day6_amazon_private_cau_seed2030_b_first | linear_hard | 0.8620 | 512 | 0.2083 | 0.1562 | 0 | 0 |
| day6_amazon_private_cau_seed2030_b_first | linear_probability_mixture | 0.8620 | 512 | 0.2083 | 0.1562 | 0 | 0 |
| day6_amazon_private_cau_seed2030_canonical | linear_hard | 0.8021 | 512 | 0.2040 | 0.1467 | 0 | 0 |
| day6_amazon_private_cau_seed2030_canonical | linear_probability_mixture | 0.8021 | 512 | 0.2040 | 0.1467 | 0 | 0 |
| day6_amazon_private_cau_seed2031_b_first | linear_hard | 0.8385 | 512 | 0.2082 | 0.1476 | 0 | 0 |
| day6_amazon_private_cau_seed2031_b_first | linear_probability_mixture | 0.8385 | 512 | 0.2082 | 0.1476 | 0 | 0 |
| day6_amazon_private_cau_seed2031_canonical | linear_hard | 0.8490 | 512 | 0.1975 | 0.1498 | 0 | 0 |
| day6_amazon_private_cau_seed2031_canonical | linear_probability_mixture | 0.8490 | 512 | 0.1975 | 0.1498 | 0 | 0 |
| day6_amazon_private_single_seed2027_b_first | linear_hard | 0.8568 | 512 | 0.1996 | 0.1454 | 0 | 0 |
| day6_amazon_private_single_seed2027_b_first | linear_probability_mixture | 0.8568 | 512 | 0.1996 | 0.1454 | 0 | 0 |
| day6_amazon_private_single_seed2027_canonical | linear_hard | 0.8464 | 512 | 0.2035 | 0.1506 | 0 | 0 |
| day6_amazon_private_single_seed2027_canonical | linear_probability_mixture | 0.8464 | 512 | 0.2035 | 0.1506 | 0 | 0 |
| day6_amazon_private_single_seed2028_b_first | linear_hard | 0.8542 | 512 | 0.2090 | 0.1488 | 0 | 0 |
| day6_amazon_private_single_seed2028_b_first | linear_probability_mixture | 0.8542 | 512 | 0.2090 | 0.1488 | 0 | 0 |
| day6_amazon_private_single_seed2028_canonical | linear_hard | 0.8594 | 512 | 0.1961 | 0.1408 | 0 | 0 |
| day6_amazon_private_single_seed2028_canonical | linear_probability_mixture | 0.8594 | 512 | 0.1961 | 0.1408 | 0 | 0 |
| day6_amazon_private_single_seed2029_b_first | linear_hard | 0.8438 | 512 | 0.1888 | 0.1397 | 0 | 0 |
| day6_amazon_private_single_seed2029_b_first | linear_probability_mixture | 0.8438 | 512 | 0.1888 | 0.1397 | 0 | 0 |
| day6_amazon_private_single_seed2029_canonical | linear_hard | 0.8542 | 512 | 0.1880 | 0.1397 | 0 | 0 |
| day6_amazon_private_single_seed2029_canonical | linear_probability_mixture | 0.8542 | 512 | 0.1880 | 0.1397 | 0 | 0 |
| day6_amazon_private_single_seed2030_b_first | linear_hard | 0.8568 | 512 | 0.1915 | 0.1381 | 0 | 0 |
| day6_amazon_private_single_seed2030_b_first | linear_probability_mixture | 0.8568 | 512 | 0.1915 | 0.1381 | 0 | 0 |
| day6_amazon_private_single_seed2030_canonical | linear_hard | 0.8438 | 512 | 0.2162 | 0.1494 | 0 | 0 |
| day6_amazon_private_single_seed2030_canonical | linear_probability_mixture | 0.8438 | 512 | 0.2162 | 0.1494 | 0 | 0 |
| day6_amazon_private_single_seed2031_b_first | linear_hard | 0.8542 | 512 | 0.1969 | 0.1495 | 0 | 0 |
| day6_amazon_private_single_seed2031_b_first | linear_probability_mixture | 0.8542 | 512 | 0.1969 | 0.1495 | 0 | 0 |
| day6_amazon_private_single_seed2031_canonical | linear_hard | 0.8411 | 512 | 0.2041 | 0.1464 | 0 | 0 |
| day6_amazon_private_single_seed2031_canonical | linear_probability_mixture | 0.8411 | 512 | 0.2041 | 0.1464 | 0 | 0 |
| day6_banking_head_only_cau_seed2027_b_first | linear_hard | 0.1281 | 1255 | 0.6087 | 0.5005 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2027_b_first | linear_probability_mixture | 0.1146 | 1255 | 0.6087 | 0.5005 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2027_canonical | linear_hard | 0.1534 | 1255 | 0.5471 | 0.5483 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2027_canonical | linear_probability_mixture | 0.1474 | 1255 | 0.5471 | 0.5483 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2028_b_first | linear_hard | 0.1228 | 1255 | 0.4772 | 0.5069 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2028_b_first | linear_probability_mixture | 0.1203 | 1255 | 0.4772 | 0.5069 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2028_canonical | linear_hard | 0.1862 | 1255 | 0.5611 | 0.5078 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2028_canonical | linear_probability_mixture | 0.1814 | 1255 | 0.5611 | 0.5078 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2029_b_first | linear_hard | 0.2056 | 1255 | 0.4816 | 0.5207 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2029_b_first | linear_probability_mixture | 0.2064 | 1255 | 0.4816 | 0.5207 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2029_canonical | linear_hard | 0.2396 | 1255 | 0.5393 | 0.5487 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2029_canonical | linear_probability_mixture | 0.2242 | 1255 | 0.5393 | 0.5487 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2030_b_first | linear_hard | 0.1205 | 1255 | 0.5612 | 0.5511 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2030_b_first | linear_probability_mixture | 0.1180 | 1255 | 0.5612 | 0.5511 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2030_canonical | linear_hard | 0.1251 | 1255 | 0.5415 | 0.5533 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2030_canonical | linear_probability_mixture | 0.1249 | 1255 | 0.5415 | 0.5533 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2031_b_first | linear_hard | 0.1735 | 1255 | 0.5428 | 0.5460 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2031_b_first | linear_probability_mixture | 0.1684 | 1255 | 0.5428 | 0.5460 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2031_canonical | linear_hard | 0.1770 | 1255 | 0.5133 | 0.5147 | 2307 | 1536 |
| day6_banking_head_only_cau_seed2031_canonical | linear_probability_mixture | 0.1764 | 1255 | 0.5133 | 0.5147 | 2307 | 1536 |
| day6_banking_head_only_single_seed2027_b_first | linear_hard | 0.0744 | 512 | 0.1389 | 0.2257 | 0 | 0 |
| day6_banking_head_only_single_seed2027_b_first | linear_probability_mixture | 0.0744 | 512 | 0.1389 | 0.2257 | 0 | 0 |
| day6_banking_head_only_single_seed2027_canonical | linear_hard | 0.1435 | 512 | 0.1478 | 0.2256 | 0 | 0 |
| day6_banking_head_only_single_seed2027_canonical | linear_probability_mixture | 0.1435 | 512 | 0.1478 | 0.2256 | 0 | 0 |
| day6_banking_head_only_single_seed2028_b_first | linear_hard | 0.1839 | 512 | 0.1347 | 0.2246 | 0 | 0 |
| day6_banking_head_only_single_seed2028_b_first | linear_probability_mixture | 0.1839 | 512 | 0.1347 | 0.2246 | 0 | 0 |
| day6_banking_head_only_single_seed2028_canonical | linear_hard | 0.0633 | 512 | 0.1511 | 0.2565 | 0 | 0 |
| day6_banking_head_only_single_seed2028_canonical | linear_probability_mixture | 0.0633 | 512 | 0.1511 | 0.2565 | 0 | 0 |
| day6_banking_head_only_single_seed2029_b_first | linear_hard | 0.1121 | 512 | 0.1514 | 0.2468 | 0 | 0 |
| day6_banking_head_only_single_seed2029_b_first | linear_probability_mixture | 0.1121 | 512 | 0.1514 | 0.2468 | 0 | 0 |
| day6_banking_head_only_single_seed2029_canonical | linear_hard | 0.1548 | 512 | 0.1430 | 0.2431 | 0 | 0 |
| day6_banking_head_only_single_seed2029_canonical | linear_probability_mixture | 0.1548 | 512 | 0.1430 | 0.2431 | 0 | 0 |
| day6_banking_head_only_single_seed2030_b_first | linear_hard | 0.1352 | 512 | 0.1365 | 0.2457 | 0 | 0 |
| day6_banking_head_only_single_seed2030_b_first | linear_probability_mixture | 0.1352 | 512 | 0.1365 | 0.2457 | 0 | 0 |
| day6_banking_head_only_single_seed2030_canonical | linear_hard | 0.1046 | 512 | 0.1418 | 0.2391 | 0 | 0 |
| day6_banking_head_only_single_seed2030_canonical | linear_probability_mixture | 0.1046 | 512 | 0.1418 | 0.2391 | 0 | 0 |
| day6_banking_head_only_single_seed2031_b_first | linear_hard | 0.0885 | 512 | 0.1456 | 0.2392 | 0 | 0 |
| day6_banking_head_only_single_seed2031_b_first | linear_probability_mixture | 0.0885 | 512 | 0.1456 | 0.2392 | 0 | 0 |
| day6_banking_head_only_single_seed2031_canonical | linear_hard | 0.1750 | 512 | 0.1449 | 0.2393 | 0 | 0 |
| day6_banking_head_only_single_seed2031_canonical | linear_probability_mixture | 0.1750 | 512 | 0.1449 | 0.2393 | 0 | 0 |
| day6_banking_private_cau_seed2027_b_first | linear_hard | 0.1987 | 1255 | 0.5531 | 0.5218 | 2307 | 1536 |
| day6_banking_private_cau_seed2027_b_first | linear_probability_mixture | 0.1887 | 1255 | 0.5531 | 0.5218 | 2307 | 1536 |
| day6_banking_private_cau_seed2027_canonical | linear_hard | 0.2618 | 1255 | 0.5163 | 0.5131 | 2307 | 1536 |
| day6_banking_private_cau_seed2027_canonical | linear_probability_mixture | 0.2576 | 1255 | 0.5163 | 0.5131 | 2307 | 1536 |
| day6_banking_private_cau_seed2028_b_first | linear_hard | 0.1451 | 1255 | 0.5377 | 0.5460 | 2307 | 1536 |
| day6_banking_private_cau_seed2028_b_first | linear_probability_mixture | 0.1471 | 1255 | 0.5377 | 0.5460 | 2307 | 1536 |
| day6_banking_private_cau_seed2028_canonical | linear_hard | 0.2419 | 1255 | 0.5988 | 0.5371 | 2307 | 1536 |
| day6_banking_private_cau_seed2028_canonical | linear_probability_mixture | 0.2383 | 1255 | 0.5988 | 0.5371 | 2307 | 1536 |
| day6_banking_private_cau_seed2029_b_first | linear_hard | 0.2259 | 1255 | 0.5445 | 0.5490 | 2307 | 1536 |
| day6_banking_private_cau_seed2029_b_first | linear_probability_mixture | 0.2256 | 1255 | 0.5445 | 0.5490 | 2307 | 1536 |
| day6_banking_private_cau_seed2029_canonical | linear_hard | 0.2731 | 1255 | 0.5372 | 0.5490 | 2307 | 1536 |
| day6_banking_private_cau_seed2029_canonical | linear_probability_mixture | 0.2666 | 1255 | 0.5372 | 0.5490 | 2307 | 1536 |
| day6_banking_private_cau_seed2030_b_first | linear_hard | 0.2526 | 1255 | 0.5060 | 0.5319 | 2307 | 1536 |
| day6_banking_private_cau_seed2030_b_first | linear_probability_mixture | 0.2559 | 1255 | 0.5060 | 0.5319 | 2307 | 1536 |
| day6_banking_private_cau_seed2030_canonical | linear_hard | 0.2398 | 1255 | 0.4860 | 0.5335 | 2307 | 1536 |
| day6_banking_private_cau_seed2030_canonical | linear_probability_mixture | 0.2407 | 1255 | 0.4860 | 0.5335 | 2307 | 1536 |
| day6_banking_private_cau_seed2031_b_first | linear_hard | 0.2188 | 1255 | 0.4937 | 0.5170 | 2307 | 1536 |
| day6_banking_private_cau_seed2031_b_first | linear_probability_mixture | 0.2111 | 1255 | 0.4937 | 0.5170 | 2307 | 1536 |
| day6_banking_private_cau_seed2031_canonical | linear_hard | 0.1811 | 1255 | 0.5535 | 0.5468 | 2307 | 1536 |
| day6_banking_private_cau_seed2031_canonical | linear_probability_mixture | 0.1726 | 1255 | 0.5535 | 0.5468 | 2307 | 1536 |
| day6_banking_private_single_seed2027_b_first | linear_hard | 0.1136 | 512 | 0.1533 | 0.2472 | 0 | 0 |
| day6_banking_private_single_seed2027_b_first | linear_probability_mixture | 0.1136 | 512 | 0.1533 | 0.2472 | 0 | 0 |
| day6_banking_private_single_seed2027_canonical | linear_hard | 0.2131 | 512 | 0.1508 | 0.2379 | 0 | 0 |
| day6_banking_private_single_seed2027_canonical | linear_probability_mixture | 0.2131 | 512 | 0.1508 | 0.2379 | 0 | 0 |
| day6_banking_private_single_seed2028_b_first | linear_hard | 0.1550 | 512 | 0.1457 | 0.2359 | 0 | 0 |
| day6_banking_private_single_seed2028_b_first | linear_probability_mixture | 0.1550 | 512 | 0.1457 | 0.2359 | 0 | 0 |
| day6_banking_private_single_seed2028_canonical | linear_hard | 0.0820 | 512 | 0.1517 | 0.2359 | 0 | 0 |
| day6_banking_private_single_seed2028_canonical | linear_probability_mixture | 0.0820 | 512 | 0.1517 | 0.2359 | 0 | 0 |
| day6_banking_private_single_seed2029_b_first | linear_hard | 0.0820 | 512 | 0.1584 | 0.2407 | 0 | 0 |
| day6_banking_private_single_seed2029_b_first | linear_probability_mixture | 0.0820 | 512 | 0.1584 | 0.2407 | 0 | 0 |
| day6_banking_private_single_seed2029_canonical | linear_hard | 0.2200 | 512 | 0.1457 | 0.2397 | 0 | 0 |
| day6_banking_private_single_seed2029_canonical | linear_probability_mixture | 0.2200 | 512 | 0.1457 | 0.2397 | 0 | 0 |
| day6_banking_private_single_seed2030_b_first | linear_hard | 0.1513 | 512 | 0.1357 | 0.2281 | 0 | 0 |
| day6_banking_private_single_seed2030_b_first | linear_probability_mixture | 0.1513 | 512 | 0.1357 | 0.2281 | 0 | 0 |
| day6_banking_private_single_seed2030_canonical | linear_hard | 0.2359 | 512 | 0.1335 | 0.2261 | 0 | 0 |
| day6_banking_private_single_seed2030_canonical | linear_probability_mixture | 0.2359 | 512 | 0.1335 | 0.2261 | 0 | 0 |
| day6_banking_private_single_seed2031_b_first | linear_hard | 0.1616 | 512 | 0.1304 | 0.2261 | 0 | 0 |
| day6_banking_private_single_seed2031_b_first | linear_probability_mixture | 0.1616 | 512 | 0.1304 | 0.2261 | 0 | 0 |
| day6_banking_private_single_seed2031_canonical | linear_hard | 0.2298 | 512 | 0.1311 | 0.2257 | 0 | 0 |
| day6_banking_private_single_seed2031_canonical | linear_probability_mixture | 0.2298 | 512 | 0.1311 | 0.2257 | 0 | 0 |
| day7_multinli_head_only_cau_seed2026_blurry | linear_hard | 0.3490 | 1312 | 1.1936 | 0.5394 | 3076 | 1536 |
| day7_multinli_head_only_cau_seed2026_blurry | linear_probability_mixture | 0.3507 | 1312 | 1.1936 | 0.5394 | 3076 | 1536 |
| day7_multinli_head_only_cau_seed2026_sharp | linear_hard | 0.3472 | 1264 | 0.9256 | 0.4819 | 2307 | 1536 |
| day7_multinli_head_only_cau_seed2026_sharp | linear_probability_mixture | 0.3646 | 1264 | 0.9256 | 0.4819 | 2307 | 1536 |
| day7_multinli_head_only_cau_seed2027_blurry | linear_hard | 0.3333 | 1424 | 1.2247 | 0.6645 | 3845 | 1536 |
| day7_multinli_head_only_cau_seed2027_blurry | linear_probability_mixture | 0.3420 | 1424 | 1.2247 | 0.6645 | 3845 | 1536 |
| day7_multinli_head_only_cau_seed2027_sharp | linear_hard | 0.3316 | 1440 | 1.1047 | 0.6493 | 3845 | 1536 |
| day7_multinli_head_only_cau_seed2027_sharp | linear_probability_mixture | 0.3281 | 1440 | 1.1047 | 0.6493 | 3845 | 1536 |
| day7_multinli_head_only_cau_seed2028_blurry | linear_hard | 0.3663 | 1152 | 0.8719 | 0.4601 | 2307 | 1536 |
| day7_multinli_head_only_cau_seed2028_blurry | linear_probability_mixture | 0.3594 | 1152 | 0.8719 | 0.4601 | 2307 | 1536 |
| day7_multinli_head_only_cau_seed2028_sharp | linear_hard | 0.3559 | 1440 | 1.1656 | 0.5765 | 3076 | 1536 |
| day7_multinli_head_only_cau_seed2028_sharp | linear_probability_mixture | 0.3750 | 1440 | 1.1656 | 0.5765 | 3076 | 1536 |
| day7_multinli_head_only_single_seed2026_blurry | linear_hard | 0.3646 | 512 | 0.2005 | 0.2311 | 0 | 0 |
| day7_multinli_head_only_single_seed2026_blurry | linear_probability_mixture | 0.3646 | 512 | 0.2005 | 0.2311 | 0 | 0 |
| day7_multinli_head_only_single_seed2026_sharp | linear_hard | 0.3611 | 512 | 0.2053 | 0.2250 | 0 | 0 |
| day7_multinli_head_only_single_seed2026_sharp | linear_probability_mixture | 0.3611 | 512 | 0.2053 | 0.2250 | 0 | 0 |
| day7_multinli_head_only_single_seed2027_blurry | linear_hard | 0.3542 | 512 | 0.2006 | 0.2283 | 0 | 0 |
| day7_multinli_head_only_single_seed2027_blurry | linear_probability_mixture | 0.3542 | 512 | 0.2006 | 0.2283 | 0 | 0 |
| day7_multinli_head_only_single_seed2027_sharp | linear_hard | 0.3524 | 512 | 0.2024 | 0.2300 | 0 | 0 |
| day7_multinli_head_only_single_seed2027_sharp | linear_probability_mixture | 0.3524 | 512 | 0.2024 | 0.2300 | 0 | 0 |
| day7_multinli_head_only_single_seed2028_blurry | linear_hard | 0.3872 | 512 | 0.2086 | 0.2280 | 0 | 0 |
| day7_multinli_head_only_single_seed2028_blurry | linear_probability_mixture | 0.3872 | 512 | 0.2086 | 0.2280 | 0 | 0 |
| day7_multinli_head_only_single_seed2028_sharp | linear_hard | 0.3802 | 512 | 0.2115 | 0.2218 | 0 | 0 |
| day7_multinli_head_only_single_seed2028_sharp | linear_probability_mixture | 0.3802 | 512 | 0.2115 | 0.2218 | 0 | 0 |
| day7_multinli_private_cau_seed2026_blurry | linear_hard | 0.3576 | 1232 | 0.9707 | 0.4687 | 2307 | 1536 |
| day7_multinli_private_cau_seed2026_blurry | linear_probability_mixture | 0.3403 | 1232 | 0.9707 | 0.4687 | 2307 | 1536 |
| day7_multinli_private_cau_seed2026_sharp | linear_hard | 0.3542 | 1248 | 0.8168 | 0.4681 | 2307 | 1536 |
| day7_multinli_private_cau_seed2026_sharp | linear_probability_mixture | 0.3594 | 1248 | 0.8168 | 0.4681 | 2307 | 1536 |
| day7_multinli_private_cau_seed2027_blurry | linear_hard | 0.3333 | 1424 | 1.1895 | 0.6671 | 3845 | 1536 |
| day7_multinli_private_cau_seed2027_blurry | linear_probability_mixture | 0.3385 | 1424 | 1.1895 | 0.6671 | 3845 | 1536 |
| day7_multinli_private_cau_seed2027_sharp | linear_hard | 0.3299 | 1440 | 1.1667 | 0.6814 | 3845 | 1536 |
| day7_multinli_private_cau_seed2027_sharp | linear_probability_mixture | 0.3385 | 1440 | 1.1667 | 0.6814 | 3845 | 1536 |
| day7_multinli_private_cau_seed2028_blurry | linear_hard | 0.3698 | 1168 | 0.9017 | 0.4803 | 2307 | 1536 |
| day7_multinli_private_cau_seed2028_blurry | linear_probability_mixture | 0.3733 | 1168 | 0.9017 | 0.4803 | 2307 | 1536 |
| day7_multinli_private_cau_seed2028_sharp | linear_hard | 0.3524 | 1440 | 1.1006 | 0.5658 | 3076 | 1536 |
| day7_multinli_private_cau_seed2028_sharp | linear_probability_mixture | 0.3611 | 1440 | 1.1006 | 0.5658 | 3076 | 1536 |
| day7_multinli_private_single_seed2026_blurry | linear_hard | 0.3750 | 512 | 0.1970 | 0.2178 | 0 | 0 |
| day7_multinli_private_single_seed2026_blurry | linear_probability_mixture | 0.3750 | 512 | 0.1970 | 0.2178 | 0 | 0 |
| day7_multinli_private_single_seed2026_sharp | linear_hard | 0.3767 | 512 | 0.1940 | 0.2287 | 0 | 0 |
| day7_multinli_private_single_seed2026_sharp | linear_probability_mixture | 0.3767 | 512 | 0.1940 | 0.2287 | 0 | 0 |
| day7_multinli_private_single_seed2027_blurry | linear_hard | 0.3715 | 512 | 0.1965 | 0.2238 | 0 | 0 |
| day7_multinli_private_single_seed2027_blurry | linear_probability_mixture | 0.3715 | 512 | 0.1965 | 0.2238 | 0 | 0 |
| day7_multinli_private_single_seed2027_sharp | linear_hard | 0.3559 | 512 | 0.1906 | 0.2137 | 0 | 0 |
| day7_multinli_private_single_seed2027_sharp | linear_probability_mixture | 0.3559 | 512 | 0.1906 | 0.2137 | 0 | 0 |
| day7_multinli_private_single_seed2028_blurry | linear_hard | 0.3924 | 512 | 0.2073 | 0.2350 | 0 | 0 |
| day7_multinli_private_single_seed2028_blurry | linear_probability_mixture | 0.3924 | 512 | 0.2073 | 0.2350 | 0 | 0 |
| day7_multinli_private_single_seed2028_sharp | linear_hard | 0.3767 | 512 | 0.2010 | 0.2295 | 0 | 0 |
| day7_multinli_private_single_seed2028_sharp | linear_probability_mixture | 0.3767 | 512 | 0.2010 | 0.2295 | 0 | 0 |

## Limitations

This standard learned gate does not establish novel task-free routing, reproduce L2R or HESTIA, or eliminate growth in total training memory. Router labels inherit the learner's own allocation errors. Development improvements require later untouched confirmation of the complete learner-plus-router.
