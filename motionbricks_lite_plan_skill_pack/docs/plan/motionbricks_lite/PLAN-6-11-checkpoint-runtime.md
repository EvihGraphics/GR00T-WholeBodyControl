# PLAN-6-11 Checkpoint: G1 Runtime Demo

## Stage Goal

Run pretrained MotionBricks G1 demo and produce proof artifacts.

## Inputs

```text
GR00T-WholeBodyControl/motionbricks/out/**
GR00T-WholeBodyControl/motionbricks/assets/skeletons/g1/**
scripts/interactive_demo_g1.py
```

## Commands

Viewer mode:

```bash
DISPLAY=:1 python scripts/interactive_demo_g1.py --has_viewer 1 --max_steps 1000
```

Headless mode:

```bash
python scripts/interactive_demo_g1.py --has_viewer 0 --max_steps 300
```

## Required Artifacts

```text
output/motionbricks_lite/runtime/runtime_manifest.json
output/motionbricks_lite/runtime/runtime_trace.jsonl
output/motionbricks_lite/runtime/control_sequence.json
output/motionbricks_lite/runtime/png/frame_000000.png
output/motionbricks_lite/runtime/motionbricks_g1_demo.mp4
output/motionbricks_lite/runtime/runtime_report.md
```

## Required Observations

```text
mode changes
movement_direction changes
facing_direction changes
context qpos shape
pred_num_tokens
pred_num_frames
generated qpos shape
current frame index increments
```

## Acceptance

```text
[ ] demo process runs
[ ] qpos finite
[ ] generated qpos buffer finite
[ ] idle visible
[ ] locomotion visible
[ ] style change visible or scripted mode change recorded
[ ] PNG sequence exists
[ ] MP4 decodable
[ ] manifest pass is true only if all gates pass
```
