import allure

import pytest

from pages.login_page import LoginPage

from utils.config_reader import load_config
from utils.data_reader import load_yaml


config = load_config()

data = load_yaml(
    "data/login.yaml"
)


@allure.feature(
    "用户登录模块"
)
@allure.story(
    "退出登录"
)
@pytest.mark.usefixtures(
    "ensure_test_account"
)
def test_logout(
    page_context
):

    login_page = LoginPage(
        page_context
    )

    account = data["cases"][0]

    with allure.step(
        "登录账号"
    ):

        login_page.open(
            config["base_url"]
        )

        login_page.open_login_page()

        login_page.login(
            account["email"],
            account["password"]
        )

        assert login_page.is_login_success(
            account["expected"]
        )


    with allure.step(
        "退出登录"
    ):

        login_page.logout()


    with allure.step(
        "校验已退出登录"
    ):

        assert login_page.is_logged_out()
