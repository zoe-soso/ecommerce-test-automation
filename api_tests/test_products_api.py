import allure

from api.api_client import ApiClient


client = ApiClient()


@allure.feature("API 测试")
@allure.story("商品列表接口")
def test_products_list_status():
    """商品列表接口应返回 200。"""
    resp = client.get_products()
    assert resp.status_code == 200


@allure.feature("API 测试")
@allure.story("商品列表接口")
def test_products_list_not_empty():
    """商品列表应至少包含 1 条商品数据。"""
    body = client.get_products().json()
    assert body.get("responseCode") == 200
    assert len(body.get("products", [])) > 0
