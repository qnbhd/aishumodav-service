from pathlib import Path
import yaml


def get_config(path: Path = Path(__file__).parent.parent.joinpath("config.yaml")) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
