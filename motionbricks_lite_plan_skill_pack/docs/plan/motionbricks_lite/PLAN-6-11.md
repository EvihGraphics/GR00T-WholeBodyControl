# PLAN-6-11: MotionBricks Lite 开源复现与 EvihAnimation 可视化桥接

## Summary

本计划参考 `arc_radier_lite` 的 gate/checkpoint/skill 组织方式，但目标完全重写为 **MotionBricks Lite**。

当前真实目标不是训练论文级 MotionBricks，也不是复现官方 UE5 插件，而是建立一条可验证的学习复现链：

```text
MotionBricks open-source environment
  -> pretrained G1 MuJoCo runtime demo
  -> runtime dataflow trace
  -> synthetic training sanity check
  -> generated motion buffer export
  -> EvihAnimation skeleton/mesh replay
  -> PNG/MP4/manifest/report
  -> UE5/MimicKit migration roadmap
```

## Current Known State

Public MotionBricks currently provides:

```text
- interactive G1 MuJoCo demo
- pretrained checkpoints under motionbricks/out/** via Git LFS
- VQVAE / pose / root model components
- synthetic training scripts
- motion representation docs
- custom dataset notes
```

Public MotionBricks currently does not provide, or should not be assumed to provide:

```text
- official UE5 plugin source
- official UE5 demo project
- built-in real mocap mini dataset for meaningful retraining
- complete paper-scale training reproducibility pipeline
- direct Chaos active-ragdoll physical controller
```

## Interfaces And Implementation

### A. Runtime Interface

Create a stable runtime trace layer around:

```text
scripts/interactive_demo_g1.py
motionbricks/motion_backbone/demo/utils.py
motionbricks/motion_backbone/demo/controllers.py
motionbricks/motion_backbone/demo/full_agent.py
motionbricks/motion_backbone/inference/motion_inference.py
```

The trace must capture:

```text
control_signals
context_mujoco_qpos
context_motion_features
spring target root/heading
target joint transforms
global_root_values
local_root_values
local_poses
pred_num_tokens
pred_pose_tokens
pred_global_motion_features
generated_mujoco_qpos
```

### B. Export Interface

Add or document a non-invasive exporter:

```text
MotionBricks runtime buffer
  -> qpos sequence
  -> motion feature sequence
  -> root transform sequence
  -> joint transform sequence
  -> replay sidecars
```

Suggested package:

```text
output/motionbricks_lite/exports/<run_id>/
  motionbricks_replay_manifest.json
  qpos.npy
  motion_features.npy
  joint_transforms.npz
  g1_joint_order.json
  coordinate_contract.json
  render_contract.json
```

### C. EvihAnimation Replay Interface

EvihAnimation must consume exported sidecars, not rendered pixels:

```text
MotionBricks qpos/features
  -> Evih skeleton sequence
  -> deterministic FK
  -> PNG sequence
  -> MP4
  -> manifest/report/contact sheet
```

## Delivery Gates

### G0 Repository / Documentation Setup

- Create MotionBricks-specific skill set.
- Create MotionBricks-specific plan/checkpoint set.
- Do not reuse ARC Raiders target semantics.

### G1 Environment And Checkpoint Gate

- Clone repository.
- Install Git LFS.
- Pull `motionbricks/out/**`.
- Pull G1 mesh assets.
- Verify checkpoint file sizes and XML/mesh existence.
- Produce `env_report.json` and `checkpoint_report.json`.

### G2 Pretrained Runtime Smoke Gate

- Run `interactive_demo_g1.py` with viewer if available.
- Run headless mode if viewer unavailable.
- Verify idle/walk and at least three style keys or scripted control modes.
- Produce PNG sequence and MP4.
- Produce `runtime_trace.jsonl`.

### G3 Runtime Dataflow Gate

- Instrument or wrap key functions without changing model behavior.
- Produce a dataflow report that can reconstruct:

```text
keyboard/control
  -> control_signals
  -> context qpos
  -> target pose/root
  -> root model
  -> pose model
  -> VQVAE decoder
  -> motion features
  -> qpos
  -> viewer
```

### G4 Synthetic Training Sanity Gate

- Run VQVAE / pose / root training scripts for minimal finite steps.
- Record batch shapes, loss finite status, NaN status, checkpoint status.
- Explicitly mark `semantic_motion_model=false`.

### G5 EvihAnimation Replay Gate

- Export MotionBricks replay sidecars.
- Implement or document EvihAnimation loader/replay.
- Output skeleton-only replay first.
- Optional: bind G1 mesh/geom if assets can be mapped.
- Produce PNG sequence, MP4, manifest, report, contact sheet.

### G6 Migration Roadmap Gate

- Produce UE5/MimicKit migration roadmap.
- Distinguish kinematic route vs physical route.
- State what is blocked by absence of official UE plugin and true physical tracking controller.

## Visual Acceptance

For any visual replay stage:

```text
png_count > 0
mp4_ok=true
all_rows_finite=true
motion_visible=true
source_was_ppm_only=false
manifest_driven_pass=true
```

If a reference sequence exists, add:

```text
mean silhouette IoU >= configured threshold
bbox centroid drift <= configured threshold
frame count and fps match
```

If no reference exists, produce qualitative contact sheet and mark metric scope as `no_reference`.

## Test Plan

- Smoke environment without viewer.
- Smoke runtime with viewer.
- Trace one replan event.
- Export 100 frames qpos.
- Load qpos in EvihAnimation skeleton replay.
- Render PNG sequence.
- Encode MP4.
- Validate manifests.
- Run synthetic training sanity for each model script.

## Assumptions

- G1 MuJoCo is the first reproduction target.
- MotionBricks generated qpos is the first stable bridge payload.
- EvihAnimation does not need to reproduce MuJoCo physics; it replays generated kinematic results.
- UE5 migration is planning-only until runtime export and Evih replay are stable.
