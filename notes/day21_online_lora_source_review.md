# Pinned Online-LoRA source-path review and CPU probe

Author repository: [Online-LoRA official](https://github.com/Christina200/Online-LoRA-official). Inspected commit: `59b9fd42ea9ca701cb36978709d5bc0e25938d81`. The 56-file source SHA256 receipt is `day21_online_lora_author_source_receipt.json`. Public source was reviewed in a separate temporary checkout; no unmodified third-party repository was added to this project.

## Inspected path

`Disjoint/main.py` constructs `LoRA_ViT_timm` and one `torch.optim.Adam(model.module.parameters(), lr=args.lr)`. It passes that optimizer into `train_and_evaluate`. In `Disjoint/engine.py`, the plateau branch calls `model.update_and_reset_lora_parameters()` when `args.new_lora` is enabled. That branch retains the existing parameter objects and optimizer. The ViT reset method in `Disjoint/lora.py` adds fresh A and B factors into their respective frozen accumulated factors, then sets **both** fresh factors to zero. The commented Kaiming initialization is not executed by this pinned reset path. The classifier remains trainable.

For the inspected two-branch linear residual, factorwise consolidation changes

`B_old A_old + B_new A_new` into `(B_old + B_new)(A_old + A_new)`.

The difference is `B_old A_new + B_new A_old`. This elementary bilinear identity is existing mathematics, not a theoretical contribution. The first consolidation has zero old factors in the constructed probe and therefore preserves the Q/V result; subsequent consolidations can contain cross terms. Whether this path affects the published benchmark requires the complete training/evaluation loop, which was not run.

## Declared diagnostic and actual result

`day21_online_lora_reset_probe_spec.md` and `experiments/day21_online_lora_reset_probe.py` were committed before this probe's outcomes. The script SHA and author-file SHA are stored with the result at `results/day21_online_lora_reset_probe/reset_probe.json`; the complete log is `logs/day21_online_lora_reset_probe.txt`.

The probe executes unchanged AST-extracted `_LoRA_qkv_timm` and `LoRA_ViT_timm` classes in a synthetic 8-dimensional QKV/classifier enclosure. It uses five declared seeds (17, 31, 47, 61, 79) and float32/float64, keeping all ten checks. Synthetic inputs, rank two, eight preparatory Adam updates and a common post-reset model are fixed. It compares an inherited optimizer with an empty optimizer while holding parameters identical, then checks a second consolidation after the declared three further updates. It does not execute timm ViT attention, the image data, the full author training loop, plateau detection, MAS or hard-buffer logic.

All ten checks passed on CPU in approximately 0.93 seconds of probe compute. Immediately after both fresh factors are zeroed, their gradients are zero in both arms. Retained Adam state nevertheless moves these fresh factors; empty state leaves them at zero in that step. The second consolidation's measured local Q/V change matches the bilinear cross terms within the declared absolute tolerances (float32 1e-6, float64 1e-12). Full numerical rows and state counts remain in the JSON rather than selecting the largest example.

This is evidence about a specific local source path under a synthetic enclosure. It is **not** a reproduction of Online-LoRA accuracy, proof that the complete model cannot learn, a benchmark seed sample, a published-method comparison or a general defect finding. The learned classifier supplies another learning path. LoRA-the-Explorer already ablates optimizer resets, and the September 2026 Bilinear Optimization Divergence preprint analyzes bilinear anchors and optimizer displacement; both must receive credit in a paper using this diagnostic.

## Reproduction gate still pending

The official README provides a one-epoch Split CIFAR-100/10-task ViT configuration with learning rate 2e-4, batch 64, loss window 5, variance threshold 0.03, mean threshold 2.6, MAS weight 2000 and hard buffer 4. Preserve its declared environment separately from this project's frozen text-training environment. Record the exact model and dataset revisions, class order, source SHA, preprocessing and measured time/memory before launching. A short unmodified timing and reset-reachability pilot should precede any complete benchmark. If that pilot predicts hours, stop under the user's compute constraint and record the comparator as incomplete. Subsequent source-path interventions need matched initialization, data, optimizer, update counts and all performance/resource outcomes.
