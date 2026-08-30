import pytest

from api.api_client import ApiClient
from utils.config_reader import load_config


@pytest.fixture(scope="session")
def api_client():
    """
    接口测试客户端（会话级复用，复用同一条连接）。

    base_url 统一从 config/ 读取，不在用例里硬编码，
    换环境只改配置、用例代码不动；同时与 UI 层共用同一套
    配置来源，避免「UI 走配置、接口走硬编码」的双份维护。
    """

    cfg = load_config()

    return ApiClient(
        cfg.get(
            "base_url",
            "https://automationexercise.com"
        )
    )
