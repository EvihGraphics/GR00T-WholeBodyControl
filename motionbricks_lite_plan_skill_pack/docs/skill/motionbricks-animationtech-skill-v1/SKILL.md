---
name: motionbricks-animationtech
summary: Use this skill when reproducing NVIDIA MotionBricks open-source runtime, explaining it through game animation engineering, or bridging its generated motion buffers into EvihAnimation / later UE5 pipelines.
---

# MotionBricks AnimationTech Skill v1

## Mission

Use the current open-source MotionBricks project as a learning and reproduction target for real-time neural motion generation.

The stable base target is **G1 MuJoCo pretrained runtime parity**:

```text
GR00T-WholeBodyControl/motionbricks
  -> pretrained checkpoints in motionbricks/out/**
  -> G1 MuJoCo skeleton/assets
  -> scripts/interactive_demo_g1.py
  -> control_signals + context qpos
  -> Root Model + Pose Model + VQVAE Decoder
  -> generated motion buffer
  -> MuJoCo qpos playback
```

The next target is **EvihAnimation replay parity**:

```text
MotionBricks generated qpos / motion features
  -> export replay sidecars
  -> convert to EvihAnimation skeleton sequence
  -> render PNG sequence + MP4
  -> produce manifest + metric/review report
```

Do not claim UE5 parity until a native UE5 plugin or a reproduced equivalent plugin exists.

## Source Truth

Primary source repo:

```text
https://github.com/NVlabs/GR00T-WholeBodyControl
subdir: motionbricks/
```

Known open-source facts:

```text
- current public MotionBricks release is a preview
- includes interactive G1 demo
- includes pretrained checkpoints
- includes synthetic training scripts
- includes motion-representation docs
- does not include official UE5 plugin source
- synthetic training data is random tensor sanity data, not real mocap
```

## Non-Negotiables

1. **Keep open-source scope precise.**
   - Pretrained G1 MuJoCo demo is available.
   - Synthetic training scripts are available.
   - Full production training pipeline and official UE5 plugin are not assumed available.

2. **Separate runtime reproduction from training reproduction.**
   - Runtime reproduction uses pretrained checkpoints.
   - Training sanity uses synthetic data only.
   - Do not describe synthetic sanity results as learned locomotion.

3. **Never treat MotionBricks as a physical controller.**
   - MotionBricks outputs kinematic motion buffer / qpos / motion features.
   - It does not output Chaos torque, PD gains, or FBodyInstance motor commands.

4. **Always record representation boundaries.**
   - Motion features: G1 dual representation, currently 418 dims.
   - MuJoCo qpos: 36 dims.
   - Context/target constraints: 4 frames per token.
   - Generated output: motion buffer, not a single frame.

5. **For EvihAnimation reproduction, use sidecars as the stable interface.**
   - Do not infer motion from rendered pixels.
   - Export qpos, root transforms, joint transforms, motion feature shape, frame index, fps, coordinate system, and skeleton mapping.

## UE5 / Game Engine Analogy

```text
MotionBricks Controller Layer
    ~= Enhanced Input + CharacterMovement intent parser

clip_holder_G1
    ~= Motion Matching database / Smart Object target pose provider

Spring Model
    ~= trajectory predictor / motion warping target generator

Root Model
    ~= Root Motion Planner

Pose Model
    ~= Pose Token Predictor

VQVAE Decoder
    ~= Pose Decoder

Generated qpos buffer
    ~= AnimSequence / PoseSnapshot buffer

MuJoCo qpos converter
    ~= Retargeter / Skeleton Adapter
```

## Required Output Convention

Any reproduction stage that visualizes motion must output:

```text
PNG sequence
MP4
runtime_trace.json or jsonl
manifest.json
human-readable report.md
```

PPM-only is never sufficient.

## Response Style

When helping with this skill:

- state whether the task is runtime, training sanity, dataflow analysis, or EvihAnimation replay;
- state whether pretrained checkpoints or synthetic data are being used;
- state exact input/output paths;
- report PNG count, MP4 status, qpos shape, motion feature shape, generated buffer length, and blocker;
- do not overclaim open-source availability.
