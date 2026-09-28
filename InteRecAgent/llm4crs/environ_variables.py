# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import json

try:
    from .config import ENV_FILE
except ImportError:  # Support: python llm4crs/environ_variables.py
    from config import ENV_FILE

DOMAIN_DATASETS = {
    'game': 'Steam',
    'movie': 'MovieLens',
    'beauty_product': 'Amazon Beauty',
}

DOMAIN_ALIASES = {
    'steam': 'game',
    'movielens': 'movie',
    'movie_lens': 'movie',
    'beauty': 'beauty_product',
    'amazon_beauty': 'beauty_product',
}


def _resolve_domain(value):
    """Resolve paper dataset names and RecAI domain names to one domain key."""
    domain = (value or 'game').strip().lower().replace('-', '_').replace(' ', '_')
    domain = DOMAIN_ALIASES.get(domain, domain)
    if domain not in DOMAIN_DATASETS:
        supported = ', '.join(DOMAIN_DATASETS)
        raise ValueError(
            f"Unsupported DOMAIN={value!r}. Expected one of: {supported}; "
            "paper dataset aliases Steam, MovieLens and Amazon Beauty are also accepted."
        )
    return domain


DOMAIN = _resolve_domain(os.environ.get('DOMAIN', 'game'))
DATASET_NAME = DOMAIN_DATASETS[DOMAIN]
__filepath = os.path.dirname(__file__)
RESOURCE_DIR = os.path.abspath(os.path.join(__filepath, f'../resources/{DOMAIN}'))
UNIREC_DIR = os.path.abspath(os.path.join(__filepath, '../UniRec/'))
SETTINGS_FILE = os.path.join(RESOURCE_DIR, 'settings.json')

if not os.path.isfile(SETTINGS_FILE):
    raise FileNotFoundError(
        f"Resource settings for {DATASET_NAME} were not found: {SETTINGS_FILE}. "
        "Install the ready-to-run resources described in InteRecAgent/README.md."
    )

with open(SETTINGS_FILE, encoding='utf-8') as f:
    environ = json.load(f)

_required_keys = {
    'GAME_INFO_FILE',
    'TABLE_COL_DESC_FILE',
    'MODEL_CKPT_FILE',
    'ITEM_SIM_FILE',
    'USE_COLS',
    'CATEGORICAL_COLS',
}
_missing_keys = sorted(_required_keys.difference(environ))
if _missing_keys:
    raise KeyError(f"Missing keys in {SETTINGS_FILE}: {', '.join(_missing_keys)}")


def _resource_path(setting_name):
    path = os.path.abspath(os.path.join(RESOURCE_DIR, environ[setting_name]))
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{setting_name} points to a missing file: {path}")
    return path


GAME_INFO_FILE = _resource_path('GAME_INFO_FILE')
TABLE_COL_DESC_FILE = _resource_path('TABLE_COL_DESC_FILE')
MODEL_CKPT_FILE = _resource_path('MODEL_CKPT_FILE')
ITEM_SIM_FILE = _resource_path('ITEM_SIM_FILE')
USE_COLS = environ['USE_COLS']
CATEGORICAL_COLS = environ['CATEGORICAL_COLS']

__all__ = [
    'DOMAIN', 'DATASET_NAME', 'DOMAIN_DATASETS', 'RESOURCE_DIR', 'SETTINGS_FILE',
    'UNIREC_DIR', 'GAME_INFO_FILE', 'TABLE_COL_DESC_FILE', 'MODEL_CKPT_FILE',
    'ITEM_SIM_FILE', 'USE_COLS', 'CATEGORICAL_COLS',
]


if __name__ == '__main__':
    print(json.dumps({
        'env_file': str(ENV_FILE),
        'domain': DOMAIN,
        'dataset': DATASET_NAME,
        'settings': SETTINGS_FILE,
        'game_info_file': GAME_INFO_FILE,
        'table_col_desc_file': TABLE_COL_DESC_FILE,
        'item_sim_file': ITEM_SIM_FILE,
        'model_ckpt_file': MODEL_CKPT_FILE,
        'use_cols': USE_COLS,
        'categorical_cols': CATEGORICAL_COLS,
    }, indent=2, ensure_ascii=False))
