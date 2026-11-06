import allure

from faker import Faker
from utils.account_data import unique_email


fake = Faker()


def _random_account():
    return {
        "name": fake.first_name(),
        "email": unique_email(),
        "password": "Password1",
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "1990",
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": "",
        "country": "United States",
        "zipcode": fake.zipcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.phone_number(),
    }


@allure.feature("API 测试")
@allure.story("账号注册接口")
def test_create_account_success(api_client):
    """使用随机数据注册新账号应成功（responseCode=201），并清理。"""
    account = _random_account()
    created = False
    try:
        resp = api_client.create_account(**account)
        created = resp.json().get("responseCode") == 201
        assert created, "测试账号创建失败"
    finally:
        if created:
            cleanup = api_client.delete_account(account["email"], account["password"])
            assert cleanup.json().get("responseCode") == 200, "测试账号清理失败"

    # 不只检查清理接口有响应，还验证该账号已经不能登录。
    deleted = api_client.verify_login(account["email"], account["password"])
    assert deleted.json().get("responseCode") == 404


@allure.feature("API 测试")
@allure.story("账号注册接口")
def test_create_account_duplicate_email(api_client):
    """
    重复邮箱注册应失败（responseCode=400）。

    用 try/finally 保证账号一定被清理，
    否则断言失败时残留数据会污染后续运行。
    """
    account = _random_account()
    created = False
    try:
        first = api_client.create_account(**account)
        created = first.json().get("responseCode") == 201
        assert created, "重复注册用例的前置账号创建失败"
        resp = api_client.create_account(**account)
        assert resp.json().get("responseCode") == 400
    finally:
        if created:
            cleanup = api_client.delete_account(account["email"], account["password"])
            assert cleanup.json().get("responseCode") == 200, "测试账号清理失败"
