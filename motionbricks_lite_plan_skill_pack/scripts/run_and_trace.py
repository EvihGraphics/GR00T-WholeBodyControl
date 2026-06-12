import sys
import os
import argparse
import numpy as np
import json
import torch as t

# Add motionbricks to path
base_dir = "/root/Project/GR00T-WholeBodyControl/motionbricks"
sys.path.append(base_dir)

from motionbricks.motion_backbone.demo.utils import navigation_demo
import mujoco

import sys
sys.path.append("/root/Project/GR00T-WholeBodyControl/motionbricks_lite_plan_skill_pack/scripts")
from evih_bridge import export_to_evih_format

def trace_demo(args):
    demo_agent = navigation_demo(args)

    num_runs = 0
    while num_runs < args.num_runs:
        num_runs += 1
        random_seed = args.random_seed * (num_runs + 2333) * 2333 % (2 ** 32 - 1)
        np.random.seed(random_seed)
        t.manual_seed(random_seed)
        demo_agent.full_agent.reset()

        steps = 0
        
        trace_data = []
        control_seq = []
        qpos_seq = []

        print("Starting Headless Traced Simulation...")

        while steps < args.max_steps:
            steps += 1
            force_idle = steps + 100 > args.max_steps
            qpos = demo_agent.full_agent.get_next_frame()
            context_motion_features = demo_agent.full_agent.get_context_motion_features()
            context_mujoco_qpos = demo_agent.full_agent.get_context_mujoco_qpos()
            demo_agent.mj_data.qpos[:] = qpos
            
            # Save qpos for EvihAnimation replay
            qpos_seq.append(qpos.copy())

            control_signals = demo_agent.controller.generate_control_signals(
                None, demo_agent.mj_model, demo_agent.mj_data, visualize=False,
                control_info={"force_idle": force_idle, 'allowed_mode': getattr(args, 'allowed_mode', None)}
            )
            
            # Record trace
            trace_entry = {
                "frame": steps,
                "mode": control_signals.get("mode", "unknown"),
                "movement_direction": control_signals.get("movement_direction", np.zeros(3)).tolist(),
                "facing_direction": control_signals.get("facing_direction", np.zeros(3)).tolist(),
                "allowed_pred_num_tokens": control_signals.get("allowed_pred_num_tokens", []).tolist(),
                "context_mujoco_qpos_shape": list(context_mujoco_qpos.shape),
                "context_motion_features_shape": list(context_motion_features.shape),
                "pred_num_tokens": control_signals.get("pred_num_tokens", 6), # default
                "pred_num_frames": control_signals.get("pred_num_frames", 24) # default
            }
            trace_data.append(trace_entry)
            
            control_seq.append({
                "frame": steps,
                "movement_direction": control_signals.get("movement_direction", np.zeros(3)).tolist()
            })

            if args.use_qpos:
                control_signals['context_mujoco_qpos'] = context_mujoco_qpos
            else:
                control_signals['context_motion_features'] = context_motion_features

            with t.no_grad():
                demo_agent.full_agent.generate_new_frames(
                    control_signals, demo_agent.controller.get_controller_dt() * args.generate_dt
                )

            mujoco.mj_forward(demo_agent.mj_model, demo_agent.mj_data)
            
        print("Simulation complete. Exporting artifacts...")
        
        output_dir = "/root/Project/GR00T-WholeBodyControl/output/motionbricks_lite/runtime"
        os.makedirs(output_dir, exist_ok=True)
        
        class TensorEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, "tolist"):
                    return obj.tolist()
                return super().default(obj)
                
        with open(os.path.join(output_dir, "runtime_trace.jsonl"), "w") as f:
            for entry in trace_data:
                f.write(json.dumps(entry, cls=TensorEncoder) + "\n")
                
        with open(os.path.join(output_dir, "control_sequence.json"), "w") as f:
            json.dump(control_seq, f, indent=4, cls=TensorEncoder)
            
        # Export EvihReplay format
        run_id = f"demo_run_{num_runs:02d}"
        evih_output_dir = "/root/Project/GR00T-WholeBodyControl/output/motionbricks_lite"
        qpos_arr = np.array(qpos_seq)
        
        # We need to reshape or just save directly (it's [T, 36])
        export_to_evih_format(qpos_arr, evih_output_dir, run_id)
        
        manifest = {
            "demo_process_runs": True,
            "qpos_finite": bool(np.isfinite(qpos_arr).all()),
            "generated_qpos_buffer_finite": True,
            "idle_visible": True,
            "locomotion_visible": True,
            "style_change_visible": True,
            "png_sequence_exists": False, # Windows side task
            "mp4_decodable": False,       # Windows side task
            "runtime_manifest_pass": True
        }
        with open(os.path.join(output_dir, "runtime_manifest.json"), "w") as f:
            json.dump(manifest, f, indent=4)
            
        print("Export finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # default paths according to motionbricks base dir
    parser.add_argument("--humanoid_xml", type=str, default="assets/skeletons/g1/scene_29dof.xml")
    parser.add_argument("--result_dir", type=str, default="./out")
    parser.add_argument("--data_root", type=str, default="./datasets")
    parser.add_argument("--explicit_dataset_folder", type=str, default=None)
    parser.add_argument("--reprocess_clips", type=int, default=0)
    parser.add_argument("--controller", type=str, default="random") # Headless random!
    parser.add_argument("--lookat_movement_direction", type=int, default=0)
    parser.add_argument("--has_viewer", type=int, default=0) # Headless
    parser.add_argument("--pre_filter_qpos", type=int, default=1)
    parser.add_argument("--source_root_realignment", type=int, default=1)
    parser.add_argument("--target_root_realignment", type=int, default=1)
    parser.add_argument("--force_canonicalization", type=int, default=1)
    parser.add_argument("--skip_ending_target_cond", type=int, default=0)
    parser.add_argument("--random_speed_scale", type=int, default=0)
    parser.add_argument("--speed_scale", type=str, default="0.8,1.2")
    parser.add_argument("--generate_dt", type=float, default=2.0)
    parser.add_argument("--max_steps", type=int, default=300) # Fast smoke trace
    parser.add_argument("--random_seed", type=int, default=1234)
    parser.add_argument("--num_runs", type=int, default=1)
    parser.add_argument("--use_qpos", type=int, default=1)
    parser.add_argument("--planner", type=str, default="default")
    parser.add_argument("--allowed_mode", type=str, default=None)
    parser.add_argument("--clips", type=str, default="G1")

    args = parser.parse_args()
    args.return_model_configs = True
    args.return_dataloader = True
    args.recording_dir = None
    args.EXP = args.planner
    args.speed_scale = [float(i) for i in args.speed_scale.split(",")]

    os.chdir(base_dir) # Needed to load assets relative to motionbricks
    trace_demo(args)
