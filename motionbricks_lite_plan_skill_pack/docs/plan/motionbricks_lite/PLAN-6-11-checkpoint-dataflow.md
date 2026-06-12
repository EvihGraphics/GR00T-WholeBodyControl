# PLAN-6-11 Checkpoint: Runtime Dataflow Trace

## Stage Goal

Produce a human-readable and machine-readable trace of MotionBricks open-source runtime dataflow.

## Trace Points

```text
interactive_demo_g1.py: main loop
navigation_demo._initialize_inference_modles
WASD_controller.generate_control_signals
full_navigation_agent.get_next_frame
full_navigation_agent.get_context_mujoco_qpos
full_navigation_agent.generate_new_frames
full_navigation_agent._process_input_to_joint_transforms
full_navigation_agent._generate_spring_model_position_and_heading
full_navigation_agent._generate_target_joint_transforms
full_navigation_agent._generate_inbetween_frames
motion_inference.predict
motion_inference._predict_root_trajectories
motion_inference._predict_pose_tokens
motion_inference._decode_motions_from_predicted_root_and_pose_tokens
```

## Required Trace Schema

See `templates/runtime_trace_schema.json`.

## Output

```text
output/motionbricks_lite/dataflow/dataflow_trace.jsonl
output/motionbricks_lite/dataflow/dataflow_manifest.json
docs/plan/motionbricks_lite/motionbricks_open_source_dataflow.md
```

## Acceptance

```text
[ ] One complete replan event is traceable.
[ ] Shape values are recorded.
[ ] No behavior-changing instrumentation.
[ ] Dataflow report includes UE5 analogies.
[ ] Trace can be validated as json/jsonl.
```
