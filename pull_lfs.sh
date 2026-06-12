#!/bin/bash
export http_proxy="http://127.0.0.1:7897"
export https_proxy="http://127.0.0.1:7897"
echo "Using proxy: $http_proxy"
cd /root/Project/GR00T-WholeBodyControl
git lfs pull --include="motionbricks/out/**" --exclude=""
git lfs pull --include="motionbricks/assets/skeletons/g1/meshes/**" --exclude=""
echo "LFS Pull Complete!"
