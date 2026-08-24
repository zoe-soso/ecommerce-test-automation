import allure

import pytest


from pages.product_page import ProductPage


from utils.config_reader import load_config
from utils.data_reader import load_yaml
from utils.assertions import (
    assert_contains,
    assert_true
)



config = load_config()


data = load_yaml(
    "data/product_detail.yaml"
)



@allure.feature(
    "商品模块"
)
@allure.story(
    "商品详情"
)
@pytest.mark.parametrize(
    "case",
    data["cases"]
)
def test_product_detail(
    page_context,
    case
):


    product_page = ProductPage(
        page_context
    )


    product_page.open(
        config["base_url"]
    )


    product_page.open_products()


    product_page.click_product()


    with allure.step(
        "校验商品名称"
    ):

        name = product_page.get_product_name()

        assert_contains(
            name,
            case["expected"]["name"]
        )


    with allure.step(
        "校验商品价格"
    ):

        price = product_page.get_product_price()

        assert_contains(
            price,
            case["expected"]["price"]
        )


    with allure.step(
        "校验商品图片"
    ):

        assert_true(
            product_page.is_product_image_visible()
        )
