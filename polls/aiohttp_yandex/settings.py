import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_db_path = BASE_DIR / 'config' / 'postgres.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config_db = get_config(config_db_path)
