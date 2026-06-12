# PLAN-6-11 Checkpoint: MotionBricks -> EvihAnimation Replay

## Stage Goal

Bridge MotionBricks generated motion buffer into EvihAnimation for visual replay.

## Inputs

```text
output/motionbricks_lite/exports/<run_id>/qpos.npy
output/motionbricks_lite/exports/<run_id>/motion_features.npy optional
output/motionbricks_lite/exports/<run_id>/joint_transforms.npz
output/motionbricks_lite/exports/<run_id>/motionbricks_replay_manifest.json
output/motionbricks_lite/exports/<run_id>/coordinate_contract.json
```

## Implementation Steps

```text
1. Export qpos sequence from MotionBricks runtime.
2. Convert qpos to root transforms and joint transforms.
3. Write G1 joint order and skeleton map.
4. Build EvihAnimation replay loader.
5. Render skeleton-only replay.
6. Optional: bind G1 mesh or simplified geom.
7. Output PNG sequence.
8. Encode MP4.
9. Build manifest and comparison sheet.
```

## Outputs

```text
output/motionbricks_lite/evih_replay/<run_id>/frames/frame_000000.png
output/motionbricks_lite/evih_replay/<run_id>/motionbricks_evih_replay.mp4
output/motionbricks_lite/evih_replay/<run_id>/motionbricks_evih_replay_manifest.json
output/motionbricks_lite/evih_replay/<run_id>/motionbricks_evih_metric_report.json
output/motionbricks_lite/evih_replay/<run_id>/motionbricks_evih_contact_sheet.png
output/motionbricks_lite/evih_replay/<run_id>/comparison_sheet.md
```

## Acceptance

```text
[ ] qpos frame count matches manifest
[ ] all qpos finite
[ ] skeleton mapping loaded
[ ] coordinate conversion documented
[ ] PNG sequence exists
[ ] MP4 decodable
[ ] replay manifest exists
[ ] no PPM-only output
[ ] skeleton-only vs mesh/geom scope is explicit
```
