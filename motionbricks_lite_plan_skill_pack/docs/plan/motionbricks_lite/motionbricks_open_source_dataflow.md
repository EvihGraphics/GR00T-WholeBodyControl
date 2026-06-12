# MotionBricks Open-Source Runtime Dataflow

## One-Line Summary

Current open-source MotionBricks is best understood as a **real-time kinematic motion buffer generator**:

```text
control intent + recent context frames + target style/keyframes
  -> root/pose/token inference
  -> generated future motion buffer
  -> MuJoCo qpos playback
```

## Dataflow

```mermaid
flowchart TD
    A[Keyboard / Random Controller] --> B[control_signals]
    B --> B1[mode]
    B --> B2[movement_direction]
    B --> B3[facing_direction]
    B --> B4[allowed_pred_num_tokens]

    C[Current frames['mujoco_qpos']] --> D[get_next_frame]
    D --> E[mj_data.qpos]
    E --> F[MuJoCo Viewer]

    C --> G[get_context_mujoco_qpos: 4 frames]
    G --> H[canonicalize qpos]
    H --> I[qpos -> joint positions/rotations]

    B --> J[Spring Model]
    I --> J
    J --> K[target root positions/headings]

    B --> L[clip_holder_G1]
    L --> M[target style clip 4 frames]
    K --> N[realign target transforms]
    M --> N

    I --> O[context constraints]
    N --> P[target constraints]
    O --> Q[global_root_values/local_root_values/local_poses]
    P --> Q

    Q --> R[Root Model]
    R --> R1[pred_num_tokens]
    R --> R2[pred_global_root_values]

    R2 --> S[Pose Model]
    Q --> S
    S --> S1[pred_pose_tokens]

    S1 --> T[VQVAE Decoder]
    R2 --> T
    T --> U[pred_global_motion_features]
    U --> V[motion features -> MuJoCo qpos]
    V --> W[uncanonicalize + blend]
    W --> X[update frames['mujoco_qpos']]
    X --> D
```

## Key Files

```text
scripts/interactive_demo_g1.py
motionbricks/motion_backbone/demo/utils.py
motionbricks/motion_backbone/demo/controllers.py
motionbricks/motion_backbone/demo/full_agent.py
motionbricks/motion_backbone/inference/motion_inference.py
motionbricks/motion_backbone/demo/clips.py
motionbricks/helper/mujoco_helper.py
```

## UE5 Analogy

```text
WASD_controller
  ~= Enhanced Input -> GameplayTag/Movement Intent

clip_holder_G1
  ~= Target Pose Provider / Smart Object pose source

Spring Model
  ~= trajectory predictor / motion warping target

Root Model
  ~= root-motion planner

Pose Model
  ~= pose-token predictor

VQVAE Decoder
  ~= pose decoder

frames['mujoco_qpos']
  ~= generated animation buffer
```

## Critical Observation

The system does not generate and play a single frame every tick. It periodically generates a **future buffer** and then consumes it frame by frame.
