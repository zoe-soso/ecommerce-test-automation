import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"


def load_config(env="test"):
    """
    加载环境配置，实现「测试环境可配置」。

    加载顺序：
        1. config/config.yaml  —— 共享默认值
        2. config/{env}.yaml   —— 具体环境覆盖（如 test / dev / prod）

    这样测试用例只需调用 load_config() 即可拿到合并后的完整配置，
    切换环境只需修改传入的 env 参数或配置文件，无需改动测试代码。
    """

    config = {}

    # 共享默认值
    base_file = CONFIG_DIR / "config.yaml"
    if base_file.exists():
        with open(base_file, "r", encoding="utf-8") as f:
            config.update(yaml.safe_load(f) or {})

    # 具体环境覆盖
    env_file = CONFIG_DIR / f"{env}.yaml"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            config.update(yaml.safe_load(f) or {})

    return config
