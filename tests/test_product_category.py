import allure
import pytest

from pages.product_page import ProductPage

from utils.config_reader import load_config
from utils.assertions import assert_contains


config = load_config()


@allure.feature(
    "商品模块"
)
@allure.story(
    "商品分类筛选"
)
@pytest.mark.parametrize(
    "case",
    [
        {"name": "Women", "panel": "#Women"},
        {"name": "Men", "panel": "#Men"},
        {"name": "Kids", "panel": "#Kids"},
    ],
    ids=[
        "Women分类",
        "Men分类",
        "Kids分类"
    ]
)
def test_product_category(
    page_context,
    case
):
    """
    商品分类筛选：
        展开 Women / Men / Kids 分类，
        点击其下子分类，结果页标题应包含对应分类名。
    """

    product_page = ProductPage(
        page_context
    )

    product_page.open(
        config["base_url"]
    )

    product_page.open_products()

    with allure.step(
        f"筛选 {case['name']} 分类"
    ):
        product_page.click_category(
            case["panel"]
        )

    with allure.step(
        "校验分类结果页标题"
    ):
        title = product_page.get_result_title()

        assert_contains(
            title.upper(),
            case["name"].upper()
        )
