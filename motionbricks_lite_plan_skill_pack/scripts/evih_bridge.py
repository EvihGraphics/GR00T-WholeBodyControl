import os
import json
import numpy as np

def export_to_evih_format(qpos_sequence, output_dir, run_id):
    """
    Export the generated MotionBricks qpos sequence to a format
    ready for EvihAnimation replay.
    """
    export_dir = os.path.join(output_dir, f"exports/{run_id}")
    os.makedirs(export_dir, exist_ok=True)
    
    # 1. Save raw qpos sequence
    qpos_file = os.path.join(export_dir, "qpos.npy")
    np.save(qpos_file, qpos_sequence)
    print(f"Saved qpos sequence of shape {qpos_sequence.shape} to {qpos_file}")
    
    # 2. Write coordinate contract (MuJoCo to EvihAnimation)
    coordinate_contract = {
        "source": "MotionBricks G1 MuJoCo",
        "source_space": {"up": "Z", "forward": "X", "handedness": "RH"},
        "motion_space": {"up": "Y", "forward": "Z", "handedness": "RH"},
        "target": "EvihAnimation",
        "target_space": {"up": "Y", "forward": "Z", "handedness": "RH"},
        "quaternion_order": "wxyz",
        "basis_transform_required": True
    }
    contract_file = os.path.join(export_dir, "coordinate_contract.json")
    with open(contract_file, "w") as f:
        json.dump(coordinate_contract, f, indent=4)
        
    # 3. Write replay manifest
    manifest = {
        "run_id": run_id,
        "num_frames": qpos_sequence.shape[0],
        "qpos_dim": qpos_sequence.shape[1] if len(qpos_sequence.shape) > 1 else 0,
        "fps": 30, # assuming 30fps simulation step recording
        "replay_pass": False # Needs to be verified in EvihAnimation
    }
    manifest_file = os.path.join(export_dir, "motionbricks_replay_manifest.json")
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"Exported replay package to {export_dir}")

# Example usage:
if __name__ == "__main__":
    # Dummy data: 100 frames, 36 dof
    dummy_qpos = np.zeros((100, 36))
    export_to_evih_format(
        dummy_qpos, 
        "/root/Project/GR00T-WholeBodyControl/motionbricks_lite_plan_skill_pack/output/motionbricks_lite",
        "demo_run_01"
    )
