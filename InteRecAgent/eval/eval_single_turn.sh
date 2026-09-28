# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"

# API, model and domain settings are loaded from $DIR/.env.
python eval/one_turn_eval.py \
    --bot_type=chat \
    --timeout=20 \
    --enable_shorten=0 \
    --demo_mode=dynamic \
    --demo_dir_or_file="$DIR/demonstration/filtered/filtered_2023-07-12-14_06_31.jsonl" \
    --num_demos=3 \
    --enable_reflection=1 \
    --plan_first=1 \
    --langchain=0 \
    --data="$DIR/eval/data/steam/one_turn_test_data.jsonl" \
    --agent=recbot
