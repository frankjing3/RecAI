"""Verify the three ready-to-run resource bundles used in the paper."""

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CONFIG_ENTRY = ROOT / "llm4crs" / "environ_variables.py"
DOMAINS = ("game", "movie", "beauty_product")


def load_domain_config(domain):
    env = os.environ.copy()
    env["DOMAIN"] = domain
    result = subprocess.run(
        [sys.executable, str(CONFIG_ENTRY)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return json.loads(result.stdout)


def verify_domain(domain):
    config = load_domain_config(domain)
    item_table = pd.read_feather(config["game_info_file"])
    similarity = np.load(config["item_sim_file"], mmap_mode="r", allow_pickle=False)

    if not {"id", "title"}.issubset(item_table.columns):
        raise ValueError(f"{domain}: item table must contain id and title")
    if item_table["id"].nunique() != len(item_table):
        raise ValueError(f"{domain}: item IDs are not unique")

    # Item IDs start at 1, while row/column 0 in the similarity matrix is padding.
    expected_size = int(item_table["id"].max()) + 1
    if similarity.shape != (expected_size, expected_size):
        raise ValueError(
            f"{domain}: similarity shape {similarity.shape} does not match "
            f"item ID space {expected_size}"
        )

    return {
        "domain": domain,
        "dataset": config["dataset"],
        "items": len(item_table),
        "similarity_shape": list(similarity.shape),
        "similarity_dtype": str(similarity.dtype),
        "checkpoint_bytes": Path(config["model_ckpt_file"]).stat().st_size,
    }


if __name__ == "__main__":
    print(json.dumps([verify_domain(domain) for domain in DOMAINS], indent=2))
