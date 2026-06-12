---
name: motionbricks-training-sanity
summary: Run MotionBricks open-source synthetic training scripts only as a pipeline sanity check, not as semantic locomotion training.
---

# MotionBricks Training Sanity Skill

## Goal

Verify that the open-source training entrypoints run through dataset, dataloader, forward, backward, and checkpoint save using synthetic random tensor data.

```text
SyntheticMotionDataset
  -> train_vqvae.py
  -> train_pose.py
  -> train_root.py
  -> finite loss / checkpoint / report
```

## Critical Boundary

Synthetic training is not real motion training.

It proves:

```text
dataset interface works
collate works
model forward works
loss is finite
backward works
checkpoint can save
```

It does not prove:

```text
walk learned
crawl learned
stealth learned
object interaction learned
style control learned
```

## Commands

Prefer short debug runs. If the existing scripts do not expose fast-dev options, add minimally invasive flags such as:

```text
--max_steps
--fast_dev_run
--num_samples
--batch_size
--save_every
```

Run:

```bash
python scripts/train_vqvae.py
python scripts/train_pose.py
python scripts/train_root.py
```

## Required Report Fields

```json
{
  "script": "train_vqvae.py",
  "dataset": "SyntheticMotionDataset",
  "num_samples": 1000,
  "feat_dim": 418,
  "batch_motion_shape": [B, T, D],
  "loss_first": 0.0,
  "loss_last": 0.0,
  "loss_finite": true,
  "nan_detected": false,
  "checkpoint_written": true,
  "semantic_motion_model": false
}
```

## Acceptance

```text
[ ] train_vqvae.py reaches at least one optimizer step.
[ ] train_pose.py reaches at least one optimizer step.
[ ] train_root.py reaches at least one optimizer step.
[ ] loss is finite.
[ ] batch shape is recorded.
[ ] checkpoint path is recorded.
[ ] report explicitly says synthetic data cannot produce usable motion semantics.
```
