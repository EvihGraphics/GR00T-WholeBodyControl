# MotionBricks -> EvihAnimation Replay Contract

## Package Layout

```text
motionbricks_replay_package/
  motionbricks_replay_manifest.json
  qpos.npy
  motion_features.npy                  # optional
  joint_transforms.npz                  # recommended
  g1_joint_order.json
  skeleton_map.json
  coordinate_contract.json
  render_contract.json
  camera_contract.json                  # optional for fixed camera
```

## Manifest Required Fields

```json
{
  "source": "MotionBricks",
  "source_repo": "NVlabs/GR00T-WholeBodyControl/motionbricks",
  "run_id": "demo_walk_001",
  "fps": 30,
  "frame_count": 300,
  "qpos_dim": 36,
  "motion_feature_dim": 418,
  "skeleton": "G1Skeleton34",
  "source_space": "MuJoCo Z-up X-forward RH",
  "target": "EvihAnimation",
  "has_qpos": true,
  "has_joint_transforms": true,
  "all_rows_finite": true
}
```

## Evih Replay Output Layout

```text
evih_replay/<run_id>/
  frames/frame_000000.png
  frames/frame_000001.png
  motionbricks_evih_replay.mp4
  motionbricks_evih_replay_manifest.json
  motionbricks_evih_metric_report.json
  motionbricks_evih_contact_sheet.png
  comparison_sheet.md
```

## Pass Conditions

```text
qpos_loaded=true
frame_count_ok=true
coordinate_contract_loaded=true
skeleton_map_loaded=true
all_rows_finite=true
png_count_ok=true
mp4_ok=true
motion_visible=true
source_was_ppm_only=false
```

## Failure Reporting

Every failed manifest must expose:

```json
{
  "replay_pass": false,
  "blocker": "missing_coordinate_contract",
  "failed_stage": "load_contract"
}
```
