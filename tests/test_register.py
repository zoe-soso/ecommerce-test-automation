import allure
import pytest

from faker import Faker

from pages.login_page import LoginPage

from utils.config_reader import load_config
from utils.data_reader import load_yaml
from utils.assertions import (
    assert_true,
    assert_false,
    assert_contains
)


config = load_config()

data = load_yaml(
    "data/register.yaml"
)

fake = Faker()


@allure.feature(
    "用户注册模块"
)
@allure.story(
    "注册功能验证"
)
@pytest.mark.parametrize(
    "case",
    [
        {"name": "正常注册"},
        {"name": "邮箱重复"},
        {"name": "空字段"},
    ],
    ids=[
        "正常注册",
        "邮箱重复",
        "空字段"
    ]
)
def test_register(
    page_context,
    case
):
    """
    注册模块覆盖：
        1. 正常注册：填写信息 → 创建成功
        2. 邮箱重复：使用已存在邮箱 → 提示已存在
        3. 空字段：留空提交 → 不应注册成功
    """

    login_page = LoginPage(
        page_context
    )

    login_page.open(
        config["base_url"]
    )

    login_page.open_login_page()

    name = case["name"]

    if name == "正常注册":

        email = fake.email()

        with allure.step(
            "填写注册信息并提交"
        ):
            landed = login_page.signup(
                fake.first_name(),
                email
            )
            assert_true(
                landed,
                "正常注册应跳转到注册信息填写页"
            )
            login_page.fill_account_info(
                data["account_info"]
            )
            login_page.create_account()

        with allure.step(
            "校验注册成功"
        ):
            assert_true(
                login_page.is_account_created(),
                "正常注册应显示 ACCOUNT CREATED!"
            )

        # 通过 UI 删除账号，避免污染站点数据
        # （公开练习站点的 /api/deleteAccount 接口当前返回 405，故用界面删除）
        try:
            login_page.page.goto(
                config["base_url"] + "/delete_account"
            )
            login_page.page.wait_for_timeout(1500)
        except Exception:
            pass

    elif name == "邮箱重复":

        with allure.step(
            "使用已存在邮箱注册"
        ):
            landed = login_page.signup(
                fake.first_name(),
                data["existing_email"]
            )

        with allure.step(
            "校验停留在登录页并提示邮箱已存在"
        ):
            assert_false(
                landed,
                "邮箱重复不应进入注册信息页"
            )
            assert_true(
                login_page.is_email_exists_error(),
                "应提示 Email already exists!"
            )

    else:  # 空字段

        with allure.step(
            "留空提交注册表单"
        ):
            landed = login_page.signup("", "")

        with allure.step(
            "校验未注册成功"
        ):
            assert_false(
                landed,
                "空字段不应进入注册信息页"
            )
            assert_false(
                login_page.is_account_created(),
                "空字段提交不应注册成功"
            )
