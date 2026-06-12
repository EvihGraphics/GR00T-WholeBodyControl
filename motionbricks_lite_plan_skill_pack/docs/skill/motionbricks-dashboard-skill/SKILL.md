---
name: motionbricks-dashboard
summary: Build or update a manifest-driven dashboard for MotionBricks runtime, training sanity, dataflow trace, and EvihAnimation replay artifacts.
---

# MotionBricks Dashboard Skill

## Goal

Provide a manifest-driven overview for MotionBricks Lite reproduction stages:

```text
Environment
Runtime demo
Dataflow trace
Training sanity
EvihAnimation replay
Migration notes
```

Do not mark a stage ready because files merely exist. Read the manifest gate fields.

## Expected Manifest Inputs

```text
output/motionbricks_lite/env_report.json
output/motionbricks_lite/checkpoint_report.json
output/motionbricks_lite/runtime/runtime_manifest.json
output/motionbricks_lite/dataflow/dataflow_manifest.json
output/motionbricks_lite/training/training_sanity_manifest.json
output/motionbricks_lite/evih_replay/evih_replay_manifest.json
```

## Health Labels

```text
env blocked            dependencies or checkpoints missing
checkpoint ready       LFS checkpoints are real and readable
runtime ready          G1 demo runs and exported PNG/MP4/trace
runtime blocked        demo failed with blocker field
trace ready            dataflow trace covers input->model->qpos
training sanity ready  synthetic training completed finite steps
training semantic no   synthetic data only; not a semantic model
evih replay ready      Evih PNG/MP4/reports exist and pass gates
evih replay blocked    contract, coordinate, media, or frame issue
```

## Required Cards

```text
- repository status
- checkpoint status
- environment status
- runtime demo status
- dataflow trace status
- synthetic training sanity status
- EvihAnimation replay status
- next UE5/MimicKit migration status
```

## Acceptance

```text
[ ] dashboard reads manifests, not just file existence.
[ ] failed stages expose blocker.
[ ] synthetic training is visibly labeled as non-semantic.
[ ] runtime links PNG/MP4/trace/report.
[ ] Evih replay links PNG/MP4/contact sheet/manifest.
```
