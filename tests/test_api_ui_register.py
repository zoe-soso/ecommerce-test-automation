import allure

from faker import Faker

from pages.login_page import LoginPage
from api.api_client import ApiClient

from utils.config_reader import load_config
from utils.assertions import assert_true


fake = Faker()

config = load_config()


@allure.feature("API + UI 混合测试")
@allure.story("API 创建账号 → UI 验证登录")
def test_api_create_then_ui_login(
    page_context
):
    """
    混合测试（SDET 典型思路）：
        API Layer  → 通过接口预置测试数据（创建账号）
        Test Data  → Faker 生成的随机账号
        UI Test    → 用界面完成登录并校验结果

    相比于纯 UI 注册，接口造数更快、更稳定，
    界面验证则保证端到端业务流程真实可用。
    """

    client = ApiClient()

    name = fake.first_name()
    email = fake.email()
    password = "Password1"

    account = {
        "name": name,
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "1990",
        "firstname": name,
        "lastname": fake.last_name(),
        "company": "Co",
        "address1": "123 Test Street",
        "address2": "",
        "country": "United States",
        "zipcode": "12345",
        "state": "CA",
        "city": "LA",
        "mobile_number": "12345678",
    }

    # ---- API Layer：创建账号 ----
    create_resp = client.create_account(**account)
    assert create_resp.json().get("responseCode") == 201

    try:

        # ---- UI Test：用界面登录并校验 ----
        login_page = LoginPage(page_context)

        with allure.step("打开登录页并登录新账号"):
            login_page.open(config["base_url"])
            login_page.open_login_page()
            login_page.login(email, password)

        with allure.step("校验登录成功"):
            assert_true(
                login_page.is_login_success(name),
                f"新注册账号 {email} 未能通过 UI 登录"
            )

    finally:

        # 测试后清理账号
        client.delete_account(email, password)
