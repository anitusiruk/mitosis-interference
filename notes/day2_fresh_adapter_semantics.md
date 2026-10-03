# Fresh Adapter Semantics Audit

PEFT multi-adapter initialization was audited after the balanced
recurrence diagnostics.

A newly added adapter's `modules_to_save` classifier and
pre-classifier are copied from the untouched `original_module`,
not from the currently trained active adapter.

Artificial mutation test:

- classifier default mutation: ~0.123456
- fresh classifier vs original module: 0
- fresh classifier vs initial default: 0
- fresh classifier vs mutated default: ~0.123456

- pre-classifier default mutation: ~0.234567
- fresh pre-classifier vs original module: 0
- fresh pre-classifier vs initial default: 0
- fresh pre-classifier vs mutated default: ~0.234567

PEFT supports `delete_adapter`.

Adding and deleting a temporary adapter changed neither the
default classifier nor the default pre-classifier (max diff 0).

Therefore, in the current architecture, "fresh capacity" means:

- fresh LoRA parameters
- fresh pre-classifier copy
- fresh classifier copy

It does NOT mean LoRA-only isolation.

Any later fresh-vs-reuse result must be interpreted accordingly,
and a head-isolation versus LoRA-isolation ablation is required
before attributing gains specifically to LoRA capacity.
