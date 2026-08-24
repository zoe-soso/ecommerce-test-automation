import allure

from api.api_client import ApiClient


client = ApiClient()


# 与 data/login.yaml 中「正常账号」保持一致
VALID_EMAIL = "123456@gmail.com"
VALID_PASSWORD = "123456"


@allure.feature("API 测试")
@allure.story("登录验证接口")
def test_verify_login_success():
    """正确账号密码应验证通过（responseCode=200）。"""
    resp = client.verify_login(
        VALID_EMAIL,
        VALID_PASSWORD
    )
    assert resp.status_code == 200
    assert resp.json().get("responseCode") == 200


@allure.feature("API 测试")
@allure.story("登录验证接口")
def test_verify_login_wrong_password():
    """错误密码应验证失败（responseCode=404）。"""
    resp = client.verify_login(
        VALID_EMAIL,
        "this_is_wrong"
    )
    assert resp.json().get("responseCode") == 404
