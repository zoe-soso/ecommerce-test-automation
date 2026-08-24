import allure

import pytest


from pages.product_page import ProductPage

from utils.data_reader import load_yaml

from utils.config_reader import load_config
from utils.assertions import assert_equal



config = load_config()

data = load_yaml(
    "data/product.yaml"
)



@allure.feature(
    "商品模块"
)
@allure.story(
    "商品搜索"
)
@pytest.mark.parametrize(
    "case",
    data["cases"],
    ids=[
        case["name"]
        for case in data["cases"]
    ]
)
def test_product_search(
    page_context,
    case
):


    product_page = ProductPage(
        page_context
    )


    with allure.step(
        "打开商品页面"
    ):

        product_page.open(
            config["base_url"]
        )


        product_page.open_products()



    with allure.step(
        "搜索商品"
    ):

        product_page.search_product(
            case["keyword"]
        )



    with allure.step(
        "验证搜索结果"
    ):

        title = product_page.get_result_title()


        assert_equal(
            title,
            case["expected"]
        )