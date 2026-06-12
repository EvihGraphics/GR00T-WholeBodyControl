import torch
try:
    data = torch.load('/root/Project/GR00T-WholeBodyControl/motionbricks/out/motionbricks_pose/version_1/checkpoints/model-step=2000000.ckpt')
    print("Checkpoint loaded successfully!")
except Exception as e:
    print("Error loading checkpoint:", e)
