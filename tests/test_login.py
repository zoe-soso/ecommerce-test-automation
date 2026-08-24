import pytest
import allure


from pages.login_page import LoginPage
from utils.data_reader import load_yaml
from utils.config_reader import load_config
from utils.assertions import assert_contains


config = load_config()


data = load_yaml(
    "data/login.yaml"
)



@allure.feature(
    "用户登录模块"
)
@allure.story(
    "登录功能验证"
)
@pytest.mark.usefixtures(
    "ensure_test_account"
)
@pytest.mark.parametrize(
    "case",
    data["cases"],
    ids=[
        case["name"]
        for case in data["cases"]
    ]
)
def test_login(
    page_context,
    case
):


    login_page = LoginPage(
        page_context
    )


    with allure.step(
        "打开登录页面"
    ):

        login_page.open(
            config["base_url"]
        )

        login_page.open_login_page()



    with allure.step(
        "执行登录"
    ):

        login_page.login(
            case["email"],
            case["password"]
        )


    with allure.step(
        "验证登录结果"
    ):


        if case["expected"] == "error":

            assert_contains(
                login_page.get_error_message(),
                "incorrect"
            )


        else:

            assert_contains(
                login_page.get_login_user(),
                case["expected"]
            )