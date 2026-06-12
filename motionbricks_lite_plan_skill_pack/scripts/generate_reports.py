import os
import json
import glob
import subprocess
import sys

def check_file_size(path_pattern, min_size_mb):
    files = glob.glob(path_pattern)
    if not files:
        return False, "File not found"
    
    # We take the first matched file
    file_path = files[0]
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    
    if size_mb < min_size_mb:
        return False, f"File size ({size_mb:.2f} MB) is smaller than required {min_size_mb} MB (Likely an LFS pointer)"
    
    return True, f"OK ({size_mb:.2f} MB)"

def check_import(module_name):
    try:
        __import__(module_name)
        return True, "OK"
    except ImportError as e:
        return False, str(e)

def main():
    base_dir = "/root/Project/GR00T-WholeBodyControl/motionbricks"
    output_dir = "/root/Project/GR00T-WholeBodyControl/output/motionbricks_lite"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Environment Report
    env_report = {
        "git_lfs_installed": False,
        "import_torch": False,
        "import_mujoco": False,
        "import_motionbricks": False,
        "blocker": None,
        "motionbricks_env_pass": False
    }
    
    try:
        result = subprocess.run(["git", "lfs", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            env_report["git_lfs_installed"] = True
    except FileNotFoundError:
        env_report["blocker"] = "Git LFS is not installed"
        
    env_report["import_torch"], t_msg = check_import("torch")
    env_report["import_mujoco"], m_msg = check_import("mujoco")
    
    # Check motionbricks (requires setting PYTHONPATH or running inside the dir)
    sys.path.append(base_dir)
    env_report["import_motionbricks"], mb_msg = check_import("motionbricks")
    
    if not env_report["git_lfs_installed"]:
        env_report["blocker"] = "Git LFS missing"
    elif not env_report["import_torch"] or not env_report["import_mujoco"]:
        env_report["blocker"] = f"Import error: Torch({t_msg}), MuJoCo({m_msg})"
    else:
        env_report["motionbricks_env_pass"] = True

    with open(os.path.join(output_dir, "env_report.json"), "w") as f:
        json.dump(env_report, f, indent=4)
        
    # 2. Checkpoint Report
    checkpoint_report = {
        "G1_clip_ckpt": False,
        "vqvae_ckpt": False,
        "pose_ckpt": False,
        "root_ckpt": False,
        "scene_xml_exists": False,
        "g1_xml_exists": False,
        "mesh_dir_exists": False,
        "blocker": None,
        "motionbricks_checkpoint_pass": False
    }
    
    c1, m1 = check_file_size(os.path.join(base_dir, "out/G1-clip.ckpt"), 1.0)
    checkpoint_report["G1_clip_ckpt"] = c1
    
    c2, m2 = check_file_size(os.path.join(base_dir, "out/motionbricks_vqvae/version_1/checkpoints/*.ckpt"), 10.0)
    checkpoint_report["vqvae_ckpt"] = c2
    
    c3, m3 = check_file_size(os.path.join(base_dir, "out/motionbricks_pose/version_1/checkpoints/*.ckpt"), 100.0)
    checkpoint_report["pose_ckpt"] = c3
    
    c4, m4 = check_file_size(os.path.join(base_dir, "out/motionbricks_root/version_1/checkpoints/*.ckpt"), 10.0)
    checkpoint_report["root_ckpt"] = c4
    
    scene_xml = os.path.join(base_dir, "assets/skeletons/g1/scene_29dof.xml")
    checkpoint_report["scene_xml_exists"] = os.path.isfile(scene_xml)
    
    g1_xml = os.path.join(base_dir, "assets/skeletons/g1/g1.xml")
    checkpoint_report["g1_xml_exists"] = os.path.isfile(g1_xml)
    
    mesh_dir = os.path.join(base_dir, "assets/skeletons/g1/meshes")
    checkpoint_report["mesh_dir_exists"] = os.path.isdir(mesh_dir) and len(os.listdir(mesh_dir)) > 0
    
    # Determine pass state
    if not all([c1, c2, c3, c4]):
        checkpoint_report["blocker"] = "Checkpoints missing or too small (LFS issue?)"
    elif not all([checkpoint_report["scene_xml_exists"], checkpoint_report["g1_xml_exists"], checkpoint_report["mesh_dir_exists"]]):
        checkpoint_report["blocker"] = "G1 assets missing"
    else:
        checkpoint_report["motionbricks_checkpoint_pass"] = True
        
    with open(os.path.join(output_dir, "checkpoint_report.json"), "w") as f:
        json.dump(checkpoint_report, f, indent=4)
        
    print("Reports generated at:", output_dir)
    print("Environment Pass:", env_report["motionbricks_env_pass"])
    print("Checkpoint Pass:", checkpoint_report["motionbricks_checkpoint_pass"])
    
if __name__ == "__main__":
    main()
