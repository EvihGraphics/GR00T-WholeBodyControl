---
name: motionbricks-evihanimation-replay
summary: Convert MotionBricks generated qpos/motion buffers into EvihAnimation replay packages and produce visual PNG/MP4/manifest parity artifacts.
---

# MotionBricks -> EvihAnimation Replay Skill

## Mission

Use EvihAnimation as a Python animation-runtime target for reproducing MotionBricks generated motion buffers.

Stable target:

```text
MotionBricks generated qpos / motion features
  -> exported replay sidecars
  -> EvihAnimation skeleton replay
  -> optional mesh/geom replay
  -> PNG sequence + MP4 + report
```

## Source Truth

```text
MotionBricks source:
GR00T-WholeBodyControl/motionbricks

EvihAnimation target:
EvihGraphics/EvihAnimation or local EvihAnimation worktree
```

The EvihAnimation side must consume exported sidecars. It must not infer motion from rendered pixels.

## Required Sidecars

A MotionBricks-to-EvihAnimation replay package must include:

```text
motionbricks_replay_manifest.json
motionbricks_qpos.jsonl or .npy
motionbricks_motion_features.npy optional
motionbricks_joint_transforms.npz
motionbricks_skeleton_map.json
g1_joint_order.json
coordinate_contract.json
camera_contract.json
render_contract.json
```

Minimum `coordinate_contract.json`:

```json
{
  "source": "MotionBricks G1 MuJoCo",
  "source_space": {"up": "Z", "forward": "X", "handedness": "RH"},
  "motion_space": {"up": "Y", "forward": "Z", "handedness": "RH"},
  "target": "EvihAnimation",
  "target_space": {"up": "Y_or_Z_explicit", "forward": "explicit", "handedness": "explicit"},
  "quaternion_order": "wxyz",
  "basis_transform_required": true
}
```

## Visual Output Requirements

Every Evih replay run must output:

```text
frames/frame_000000.png
frames/frame_000001.png
...
motionbricks_evih_replay.mp4
motionbricks_evih_replay_manifest.json
motionbricks_evih_metric_report.json
motionbricks_evih_contact_sheet.png
comparison_sheet.md
```

PPM-only is forbidden.

## Replay Pipeline

```text
1. Load MotionBricks qpos sequence.
2. Convert qpos to root transform + joint values.
3. Map G1 skeleton to EvihAnimation skeleton representation.
4. Apply explicit coordinate conversion.
5. Build deterministic FK.
6. Render skeleton-only replay.
7. Optionally bind G1 mesh/geom if available.
8. Export PNG sequence.
9. Encode MP4.
10. Generate metric/report/manifest.
```

## Acceptance

```text
[ ] qpos frames loaded.
[ ] frame count matches manifest.
[ ] skeleton_map loaded.
[ ] coordinate_contract loaded.
[ ] all rows finite.
[ ] root trajectory visible.
[ ] PNG count matches expected count.
[ ] MP4 decodable.
[ ] no PPM-only output.
[ ] report states skeleton-only or mesh/geom scope.
[ ] replay_pass field is true only when all gates pass.
```

## Troubleshooting

```text
Character rotated 90 degrees:
- Check MuJoCo Z-up/X-forward/RH to Evih target basis.

Quaternion flips:
- Do not manually swap components unless proven by matrix equivalence.
- Prefer basis matrix conversion: R_target = B * R_source * B^-1.

Frozen sequence:
- Check that get_next_frame output was exported after buffer generation, not just initial idle buffer.

Wrong frame count:
- Check FPS, stride, max_steps, and replan horizon.
```
