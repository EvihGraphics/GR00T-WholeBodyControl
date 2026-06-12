# PLAN-6-11 Checkpoint: Environment And Checkpoints

## Stage Goal

Prepare the MotionBricks repository, dependencies, Git LFS assets, pretrained checkpoints, and baseline environment report.

## Commands

```bash
git clone https://github.com/NVlabs/GR00T-WholeBodyControl.git
cd GR00T-WholeBodyControl
git lfs install
git lfs pull --include="motionbricks/out/**" --exclude=""
git lfs pull --include="motionbricks/assets/skeletons/g1/meshes/**" --exclude=""
cd motionbricks
conda create -n motionbricks python=3.10 -y
conda activate motionbricks
pip install -e .
pip install pynput python-xlib
```

## Required Checks

```text
[ ] Git LFS installed
[ ] out/G1-clip.ckpt exists and size > 1MB
[ ] VQVAE ckpt exists and size > 10MB
[ ] pose ckpt exists and size > 100MB
[ ] root ckpt exists and size > 10MB
[ ] assets/skeletons/g1/scene_29dof.xml exists
[ ] assets/skeletons/g1/g1.xml exists
[ ] G1 mesh directory exists
[ ] Python imports torch/mujoco/motionbricks
```

## Output

```text
output/motionbricks_lite/env_report.json
output/motionbricks_lite/checkpoint_report.json
```

## Blockers

```text
Git LFS pointer files
CUDA/PyTorch mismatch
MuJoCo import failure
X11/DISPLAY unavailable
missing G1 XML or meshes
```

## Pass Field

```json
{"motionbricks_env_pass": true, "blocker": null}
```
