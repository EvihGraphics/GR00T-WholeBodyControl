# PLAN-6-11 Checkpoint: Synthetic Training Sanity

## Stage Goal

Run the available MotionBricks training scripts as sanity checks only.

## Inputs

```text
motionbricks/data/synthetic_dataset.py
scripts/train_vqvae.py
scripts/train_pose.py
scripts/train_root.py
```

## Commands

```bash
python scripts/train_vqvae.py
python scripts/train_pose.py
python scripts/train_root.py
```

If needed, add debug args without breaking default behavior:

```text
--fast_dev_run
--max_steps
--num_samples
--batch_size
```

## Output

```text
output/motionbricks_lite/training/train_vqvae_sanity.json
output/motionbricks_lite/training/train_pose_sanity.json
output/motionbricks_lite/training/train_root_sanity.json
output/motionbricks_lite/training/training_sanity_manifest.json
```

## Acceptance

```text
[ ] Dataset returns {keyid, motion}
[ ] Batch shape recorded
[ ] Forward pass works
[ ] Loss finite
[ ] Backward pass works
[ ] Checkpoint save path recorded
[ ] semantic_motion_model=false
```
