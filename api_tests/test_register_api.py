import allure

from faker import Faker


fake = Faker()


def _random_account():
    return {
        "name": fake.first_name(),
        "email": fake.email(),
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
    resp = api_client.create_account(**account)
    assert resp.json().get("responseCode") == 201

    # 测试后清理，避免污染站点数据
    api_client.delete_account(
        account["email"],
        account["password"]
    )


@allure.feature("API 测试")
@allure.story("账号注册接口")
def test_create_account_duplicate_email(api_client):
    """
    重复邮箱注册应失败（responseCode=400）。

    用 try/finally 保证账号一定被清理，
    否则断言失败时残留数据会污染后续运行。
    """
    account = _random_account()
    api_client.create_account(**account)

    try:
        resp = api_client.create_account(**account)
        assert resp.json().get("responseCode") == 400
    finally:
        api_client.delete_account(
            account["email"],
            account["password"]
        )
