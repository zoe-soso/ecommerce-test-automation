import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_yaml(file_path):

    path = BASE_DIR / file_path


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)