---
name: motionbricks-g1-runtime-repro
summary: Reproduce the current open-source MotionBricks pretrained G1 MuJoCo interactive demo, verify assets/checkpoints, instrument runtime dataflow, and export PNG/MP4/reports.
---

# MotionBricks G1 Runtime Reproduction Skill

## Goal

Run and inspect the open-source MotionBricks pretrained runtime demo:

```text
motionbricks/out pretrained checkpoints
  -> scripts/interactive_demo_g1.py
  -> MuJoCo G1 viewer
  -> WASD/style control
  -> generated qpos motion buffer
  -> PNG/MP4/report artifacts
```

## Required Preparation

```bash
cd <workspace>
git clone https://github.com/NVlabs/GR00T-WholeBodyControl.git
cd GR00T-WholeBodyControl

git lfs install
git lfs pull --include="motionbricks/out/**" --exclude=""
git lfs pull --include="motionbricks/assets/skeletons/g1/meshes/**" --exclude=""
cd motionbricks
```

Verify that these are not tiny LFS pointer files:

```text
out/G1-clip.ckpt
out/motionbricks_vqvae/version_1/checkpoints/*.ckpt
out/motionbricks_pose/version_1/checkpoints/*.ckpt
out/motionbricks_root/version_1/checkpoints/*.ckpt
assets/skeletons/g1/scene_29dof.xml
assets/skeletons/g1/g1.xml
```

## Environment

Use Python 3.10+ and CUDA GPU.

```bash
conda create -n motionbricks python=3.10 -y
conda activate motionbricks
pip install -e .
pip install pynput python-xlib
```

On Windows/WSL/Linux viewer setups, record:

```text
OS
GPU
CUDA version
Python version
MuJoCo version
DISPLAY / X11 availability
checkpoint file sizes
```

## Smoke Commands

```bash
cd GR00T-WholeBodyControl/motionbricks
DISPLAY=:1 python scripts/interactive_demo_g1.py --has_viewer 1 --max_steps 1000
```

Headless trace mode:

```bash
python scripts/interactive_demo_g1.py --has_viewer 0 --max_steps 300
```

## Runtime Data To Record

For every replan event, record:

```json
{
  "frame": 0,
  "mode": "walk",
  "movement_direction": [0, 1, 0],
  "facing_direction": [0, 1, 0],
  "allowed_pred_num_tokens": [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
  "context_mujoco_qpos_shape": [1, 4, 36],
  "context_motion_features_shape": [1, 4, 418],
  "global_root_values_shape": [1, 8, 5],
  "local_root_values_shape": [1, 8, 4],
  "local_poses_shape": [1, 8, 303],
  "pred_num_tokens": 6,
  "pred_num_frames": 24,
  "generated_mujoco_qpos_shape": [1, 24, 36]
}
```

Exact feature dimensions must be measured from the running code; do not hardcode values in reports if the runtime exposes a different value.

## Acceptance

```text
[ ] G1 MuJoCo viewer starts.
[ ] idle works.
[ ] walk works.
[ ] at least 3 style keys work.
[ ] generated qpos has finite values.
[ ] motion buffer refreshes periodically.
[ ] runtime_trace.jsonl exists.
[ ] PNG sequence exists.
[ ] MP4 exists and is decodable.
[ ] report states whether viewer/headless mode was used.
```

## Troubleshooting

```text
Tiny checkpoint files:
- Git LFS did not pull real checkpoint blobs.

Keyboard conflicts:
- On Linux/X11, the demo tries to disable MuJoCo keyboard shortcuts.
- On Wayland/macOS/Windows, terminal focus may be required.

No viewer:
- Use --has_viewer 0 for dataflow trace first.

Black or frozen visual:
- Check qpos values and whether get_next_frame increments current_frame_idx.
```
