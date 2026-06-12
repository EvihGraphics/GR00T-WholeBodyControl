# MotionBricks Motion Representation Notes

## Known Public Representation

Current G1 config uses a dual motion representation:

```text
Full dual representation: 418 dims
Global subset: 414 dims
Local subset: 413 dims
Shared body features: 409 dims
MuJoCo qpos: 36 dims
```

## Body Features

The 409-dim shared body features include roughly:

```text
global joint positions relative/projected root
6D global joint rotations
per-joint velocities
foot contacts
```

## Root Features

```text
Global root: 5 dims
  - global_root_pos: 3
  - global_root_heading: cos/sin: 2

Local root: 4 dims
  - angular velocity around up axis
  - root planar velocity
  - root height
```

## MuJoCo qpos

```text
0-2: root translation
3-6: root quaternion, wxyz
7-35: 29 hinge joint angles
```

## Context / Target Layout

Runtime inference builds constraints from:

```text
4 context frames
4 target frames
```

These become:

```text
global_root_values: [B, 8, 5]
local_root_values:  [B, 8, 4]
local_poses:        [B, 8, D_pose]
```

## Token To Frame

Current code uses:

```text
NUM_FRAMES_PER_TOKEN = 4
num_pred_frames = pred_num_tokens * 4
```

## UE5 Analogy

```text
Motion feature
  ~= FCompactPose + RootMotion + foot contact state packed into a tensor

qpos
  ~= robot/skeleton pose snapshot for playback

generated buffer
  ~= transient AnimSequence generated at runtime
```
