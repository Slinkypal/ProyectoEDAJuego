#!/usr/bin/bash
source /home/slinkypal/miniforge3/etc/profile.d/conda.sh
eval "$(conda shell.bash hook)"
conda activate /home/slinkypal/miniforge3/envs/Arquitectura

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python main.py
