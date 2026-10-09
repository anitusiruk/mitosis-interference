# Resume instructions (written 2026-10-09)

Active branch: `tmlr-reframe`. Current paper: `paper/main.tex` (results sections pending).
Plan and decisions: `notes/tmlr_reframe_20261009.md`, `notes/tmlr_confirmation_prereg.md`,
`notes/tmlr_exploratory_spec.md`.

Pod was stopped mid-confirmation (240/1200 primary runs saved). On a new pod:

    gh repo clone anitusiruk/mitosis-interference && cd mitosis-interference
    git checkout tmlr-reframe
    pip install transformers==5.18.0 datasets==3.6.0 peft==0.21.0 accelerate==1.15.0 scikit-learn scipy matplotlib
    nohup experiments/tfcl_confirm.sh > results/tfcl/confirm_pipeline.log 2>&1 &
    nohup experiments/tfcl_explore.sh > results/tfcl/explore_pipeline.log 2>&1 &

Both scripts skip every completed output, so they continue where they stopped; interrupted runs
restart from scratch (runs are deterministic given the seed, so this introduces no selection).
Pre-registered code hashes must still match before analysis:
`sha256sum src/tfcl/*.py experiments/tfcl_run.py experiments/tfcl_grid.py`.
When done: `python -m experiments.tfcl_confirm_report` and write Section 6 of the paper.
