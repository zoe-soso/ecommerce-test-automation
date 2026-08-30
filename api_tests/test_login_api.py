import allure

from utils.data_reader import load_yaml


# 账号统一取自 data/login.yaml，与 UI 登录用例共用同一份数据源，
# 避免同一账号在多个文件里硬编码、改一处漏一处。
login_data = load_yaml("data/login.yaml")

VALID_CASE = next(
    case
    for case in login_data["cases"]
    if case["expected"] != "error"
)

VALID_EMAIL = VALID_CASE["email"]
VALID_PASSWORD = VALID_CASE["password"]


@allure.feature("API 测试")
@allure.story("登录验证接口")
def test_verify_login_success(api_client):
    """正确账号密码应验证通过（HTTP 200 且 responseCode=200）。"""
    resp = api_client.verify_login(
        VALID_EMAIL,
        VALID_PASSWORD
    )
    assert resp.status_code == 200
    assert resp.json().get("responseCode") == 200


@allure.feature("API 测试")
@allure.story("登录验证接口")
def test_verify_login_wrong_password(api_client):
    """
    错误密码应验证失败（responseCode=404）。

    注意该站点鉴权失败时 HTTP 状态码仍是 200，
    真正的错误信息放在响应体的 responseCode 里，
    所以接口断言不能只看 status_code。
    """
    resp = api_client.verify_login(
        VALID_EMAIL,
        "this_is_wrong"
    )
    assert resp.json().get("responseCode") == 404
