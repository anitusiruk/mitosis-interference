# Pinned author-loop buffer units and importance-call shape

The inspected [Online-LoRA arXiv v1](https://arxiv.org/html/2411.05663v1), Section 3.3 and Appendix G, describes a four-sample hard buffer. At [author commit 59b9fd42ea9ca701cb36978709d5bc0e25938d81](https://github.com/Christina200/Online-LoRA-official/tree/59b9fd42ea9ca701cb36978709d5bc0e25938d81), the Disjoint path passes entire DataLoader batches to the training loop and stores each batch tensor as one buffer entry. Source review suggested this unit mismatch before the CPU diagnostic.

The unchanged AST-extracted `train_and_evaluate` function was executed in the existing synthetic QKV/three-class enclosure, with unchanged author forward classes and logging utility classes. All nine predeclared cases passed in 1.45 seconds of probe computation. Three seeds are repeated structural checks, not independent benchmark replications. Every case retains twelve buffer-update receipts and every observed importance-loss input shape.

| Incoming batch size | Buffer setting | Entries after filling | Retained examples | Fixture input-tensor bytes | Importance-loss input shape |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 4 | 384 | 1 by 3 |
| 8 | 4 | 4 | 32 | 3072 | 1 by 24 |
| 64 | 4 | 4 | 256 | 24576 | 1 by 192 |

Each row passed for seeds 17, 31 and 47. The fixture uses three token positions and eight hidden values; these byte counts describe the fixture only. Four full 64-image batches of 224-pixel RGB float32 input tensors would contain 154,140,672 bytes (147 MiB), whereas four such individual images would contain 2,408,448 bytes. That calculation is an extrapolation from tensor dimensions, not measured ViT GPU memory. Real final batches can be shorter, so retain actual batch dimensions rather than assuming 256 examples at every step.

The inspected importance branch calls `model.forward(sx).view(1,-1)`. The instrumentation delegated the unchanged numeric `nll_loss` call to PyTorch and observed a single class vector of width batch size times three for this fixture, rather than a separate three-class vector per example. The diagnostic does not estimate the importance error or any downstream accuracy consequence on the author's benchmark.

Scope is deliberately narrow. The synthetic branch fixture uses the author's `new_lora=False` ablation and declared mean/variance thresholds 10 and 1e6 to exercise importance estimation. It substitutes synthetic inputs and a no-metric benchmark-evaluation callback and redirects logging setup. No CIFAR/ImageNet data, actual timm attention, augmentation, distributed launcher or published evaluation was run. This is not a full method reproduction, not an allegation about all author implementations and not evidence that reported paper results are invalid. The reset probe from Day 21 remains a distinct diagnostic.

For a complete source-faithful comparator, record both the configured entry count and actual retained images/bytes, exact forward and replay exposure, all loss terms and the importance-call dimensions. Reproduce the unmodified configuration before comparing any per-example-buffer or importance-shape correction. Such corrections need separately declared matched controls and measured results; this probe supplies no performance claim. It adds a concrete implementation/resource audit to the broader package-attribution project, while the submission still needs complete benchmark evidence.

Specification: `notes/day22_online_lora_buffer_probe_spec.md`. Full receipt: `results/day22_online_lora_buffer_probe/buffer_probe.json`. Native source-file hashes are checked against `notes/day21_online_lora_author_source_receipt.json`. Original author code remains external and pinned; all experimental code and receipts are saved in the authorized project.
