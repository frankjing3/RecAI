# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"

# API, model, simulator and domain settings are loaded from $DIR/.env.
python eval/user_simulator.py \
    --timeout=60 \
    --bot_type=chat \
    --enable_shorten=0 \
    --demo_mode=dynamic \
    --demo_dir_or_file="$DIR/demonstration/filtered/filtered_2023-07-12-14_06_31.jsonl" \
    --num_demos=3 \
    --enable_reflection=1 \
    --plan_first=1 \
    --langchain=0 \
    --data="$DIR/eval/data/steam/simulator_test_data.jsonl" \
    --max_turns=5 \
    --agent=recbot
