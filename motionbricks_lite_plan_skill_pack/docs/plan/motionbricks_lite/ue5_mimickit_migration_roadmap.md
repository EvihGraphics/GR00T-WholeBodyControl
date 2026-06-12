# MotionBricks -> UE5 / MimicKit Migration Roadmap

## Kinematic Route

```text
MotionBricks runtime
  -> export ONNX/TorchScript/TensorRT candidate
  -> UE5 C++ wrapper, preferably ONNX Runtime first for operator visibility
  -> AnimNode Pose Generator
  -> IK Retargeter / Control Rig
  -> SkeletalMeshComponent playback
```

## Physical Route

```text
MotionBricks target motion buffer
  -> target pose/root trajectory
  -> MimicKit / ASE / SONIC-like tracking policy
  -> PD targets or torque commands
  -> UE5 Chaos active ragdoll
```

## Do Not Confuse

```text
MotionBricks = upper-level motion planner / generator
MimicKit/ASE/SONIC-style policy = physical tracking controller
Chaos/PhysicsAsset = final physics backend
```

## Coordinate System Warning

MotionBricks motion space and MuJoCo space differ. UE5 introduces a left-handed convention. Use basis matrix conversion and recalculate quaternions.

```text
R_target = B * R_source * B^-1
```

## Suggested UE5 Runtime Components

```text
FMotionBricksFrame
FMotionBricksSequenceBuffer
UMotionBricksModelAsset
FAnimNode_MotionBricksPoseGenerator
AMotionBricksTaskActor
UMotionBricksRetargetBridge
```

## Minimum UE5 Demo Goal

```text
Load exported MotionBricks qpos/motion buffer
  -> convert to UE skeleton pose
  -> play as generated AnimSequence or AnimNode buffer
  -> export PNG/MP4 from UE viewport or Movie Render Queue
```

Only after this kinematic demo works should physical tracking be attempted.
