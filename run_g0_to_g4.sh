#!/bin/bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate motionbricks
export LD_LIBRARY_PATH=/root/miniconda3/envs/motionbricks/lib:$LD_LIBRARY_PATH

echo "Running G0: Environment and Checkpoint Checks..."
python /root/Project/GR00T-WholeBodyControl/motionbricks_lite_plan_skill_pack/scripts/generate_reports.py

echo "Running G1-G3: Headless Runtime Trace..."
python /root/Project/GR00T-WholeBodyControl/motionbricks_lite_plan_skill_pack/scripts/run_and_trace.py

echo "Running G4: Synthetic Training Sanity Checks..."
python /root/Project/GR00T-WholeBodyControl/motionbricks_lite_plan_skill_pack/scripts/run_synthetic_sanity.py

echo "All pipeline execution completed!"
