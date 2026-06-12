# Custom Dataset Bridge Notes

## Current Public Dataset Situation

The built-in `SyntheticMotionDataset` is random tensor data. It is useful for training pipeline sanity checks, not for meaningful locomotion training.

## Required Dataset Interface

A minimal dataset item should return:

```python
{
    "keyid": int,
    "motion": Tensor[T, feature_dim]
}
```

If reusing MotionBricks representation, `motion` should already be computed and normalized.

## Real Data Pipeline

```text
BVH / FBX / GLB / mocap
  -> skeleton retarget
  -> compute global joint positions
  -> compute global joint rotations
  -> compute root features
  -> compute velocities
  -> compute foot contacts
  -> pack feature vector
  -> compute normalization stats
  -> PyTorch Dataset
```

## G1 vs Game Character

Do not blindly use G1Skeleton34 for UE5 characters.

For UE5 or MimicKit characters:

```text
new skeleton definition
new joint order
new feature packing
new normalization stats
new retargeter
new decoder output mapping
```

## Small Meaningful Dataset Option

For a real minimal meaningful dataset, prepare:

```text
idle loop
walk forward
walk left/right
turn in place
crouch/stealth optional
fall/recover optional
```

Each should be processed into the same feature representation and validated by a frame-by-frame replay before training.
