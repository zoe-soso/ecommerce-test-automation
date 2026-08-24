import re
import allure
import urllib.parse
import urllib.request

from datetime import datetime

import pytest

from utils.logger import logger
from utils.config_reader import load_config


# ===============================
# 测试账号保障
# ===============================

# 下单 / 登录模块依赖该账号，固件幂等预建（已存在则返回 400）
TEST_ACCOUNT = {
    "name": "zoe",
    "email": "123456@gmail.com",
    "password": "123456",
    "title": "Mr",
    "birth_date": "1",
    "birth_month": "January",
    "birth_year": "1990",
    "firstname": "Zoe",
    "lastname": "Test",
    "company": "TestCo",
    "address1": "123 Test Street",
    "address2": "Apt 1",
    "country": "United States",
    "zipcode": "123456",
    "state": "Central",
    "city": "Singapore",
    "mobile_number": "12345678",
}


@pytest.fixture(scope="session")
def ensure_test_account():
    """会话级幂等预建测试账号（已存在则视为正常跳过）。"""

    cfg = load_config()
    base_url = cfg.get(
        "base_url",
        "https://automationexercise.com"
    )

    url = f"{base_url}/api/createAccount"

    body = urllib.parse.urlencode(
        TEST_ACCOUNT
    ).encode()

    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": (
                "application/x-www-form-urlencoded"
            ),
            "Accept": "application/json",
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=20
        ) as resp:

            logger.info(
                f"预建测试账号: {resp.read().decode()}"
            )

    except urllib.error.HTTPError as e:

        # 400 = Email already exists，属正常情况
        logger.info(
            f"预建测试账号(已存在/跳过): {e.code}"
        )

    except Exception as e:

        logger.warning(
            f"预建测试账号失败: {e}"
        )

    yield


# ===============================
# 多浏览器参数化（Chromium / Firefox / WebKit）
# ===============================
# 说明：pytest-playwright 通过 --browser 选项（可多次指定）
#       自动对 browser_name 做参数化。本项目在 pytest.ini 的
#       addopts 中写入三个 --browser，使 `pytest` 默认即覆盖
#       三大内核，用例数由 10 扩展到 30。
#       若只想跑单浏览器，可单独指定：
#           pytest --browser chromium

# ===============================
# 页面生命周期
# ===============================

@pytest.fixture(scope="function")
def page_context(page):
    """
    用例级 page 包装：
        - 注入配置中的默认超时；
        - 透传 page 给测试用例。
    """

    cfg = load_config()

    try:
        page.set_default_timeout(
            int(cfg.get("timeout", 30000))
        )
        page.set_default_navigation_timeout(
            int(cfg.get("timeout", 30000))
        )
    except Exception:
        pass

    yield page


# ===============================
# 测试生命周期日志（START / END / PASS / FAIL）
# ===============================

def pytest_runtest_setup(item):
    """每个用例执行前打印 START TEST。"""
    logger.info(f"START TEST: {item.nodeid}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """生成测试报告时补充：END TEST 结果、失败 URL/异常、失败截图。"""

    outcome = yield

    report = outcome.get_result()

    # 仅关注用例执行（call）阶段
    if report.when != "call":
        return

    page = item.funcargs.get("page_context")

    if report.passed:

        logger.info(
            f"END TEST: PASS - {item.name}"
        )

    elif report.failed:

        logger.error(
            f"END TEST: FAIL - {item.name}"
        )

        # 记录失败时上下文，便于排查
        try:
            if page is not None:
                logger.error(
                    f"失败时当前 URL: {page.url}"
                )
            if report.longrepr:
                logger.error(
                    f"失败异常: {report.longrepr}"
                )
        except Exception:
            pass

        # 失败自动截图（同时附到 Allure）
        try:
            if page is not None:

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                test_name = re.sub(
                    r"[^a-zA-Z0-9_]", "_", item.name
                )

                path = (
                    f"screenshots/"
                    f"{test_name}_{timestamp}.png"
                )

                page.screenshot(
                    path=path,
                    full_page=True
                )

                with open(path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="失败截图",
                        attachment_type=(
                            allure.attachment_type.PNG
                        )
                    )

                logger.error(
                    f"测试失败，截图已保存: {path}"
                )

        except Exception as exc:
            # 截图 / 日志 / allure 附加失败绝不应影响测试结论
            try:
                logger.warning(
                    f"失败处理异常（已忽略）: {exc}"
                )
            except Exception:
                pass
