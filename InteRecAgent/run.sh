# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

#!/bin/bash
set -e

# API, model and domain settings are loaded by Python from ./.env.
# Copy .env.example to .env and fill in OPENAI_API_KEY before running.
cd "$(dirname "$0")"

python ./app.py \
    --enable_shorten=0 \
    --demo_mode=dynamic \
    --num_demos=5 \
    --enable_reflection=0 \
    --plan_first=1 \
    --langchain=0 \
    --demo_dir_or_file=./demonstration/seed_demos_placeholder.jsonl
