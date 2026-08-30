import allure


@allure.feature("API 测试")
@allure.story("商品列表接口")
def test_products_list_status(api_client):
    """商品列表接口应返回 200。"""
    resp = api_client.get_products()
    assert resp.status_code == 200


@allure.feature("API 测试")
@allure.story("商品列表接口")
def test_products_list_not_empty(api_client):
    """
    商品列表应至少包含 1 条商品数据。

    这里同时断言业务响应码 responseCode：
    该站点的错误也返回 HTTP 200，状态码并不足以判断请求是否成功。
    """
    body = api_client.get_products().json()
    assert body.get("responseCode") == 200
    assert len(body.get("products", [])) > 0
