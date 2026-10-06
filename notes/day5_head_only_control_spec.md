# Day-5 head-only closed-loop control

Declared before any head-only live outcomes. Motivation: the initial architecture
allocates a fresh pre-classifier/classifier with every new LoRA; the component
factorial audit explicitly anticipates a classifier-reset explanation.

Run the unchanged private-package CAU-v1 selection rules and original recurrence
data while freezing every LoRA parameter throughout real and virtual training.
Initialize LoRA B=0 as usual and assert it stays exactly zero: every adapter then
has the same frozen encoder function, and only its private pre-classifier and
classifier can adapt. Keep learning rate, optimizer type, memory, probe size,
two-window evidence, lower-bound gate and rank configuration unchanged. The
unused LoRA tensors remain implementation scaffolding; separately report the
minimal deployable adaptation parameter count obtained by deleting zero-output
LoRA branches. Do not present this as a parameter-matched control.

This tests whether live allocation/recurrence usefulness survives without any
learned representation adaptation. It is a control, not a proposed new method.
Evaluate the same full-label-space label-free rules and oracle diagnostics.
Run BANKING and Amazon if time allows; no official tests, threshold changes or
new model-selection decisions from this control. If it accounts for the main
result, narrow LoRA-specific claims rather than concealing the outcome.
