import allure


from pages.product_page import ProductPage
from pages.cart_page import CartPage


from utils.config_reader import load_config
from utils.data_reader import load_yaml
from utils.assertions import (
    assert_contains,
    assert_equal
)


config = load_config()

data = load_yaml(
    "data/cart.yaml"
)


@allure.feature(
    "购物车模块"
)
@allure.story(
    "添加商品"
)
def test_add_product_to_cart(
    page_context
):


    product_page = ProductPage(
        page_context
    )


    cart_page = CartPage(
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
        "加入购物车"
    ):

        product_page.click_product()

        product_page.add_to_cart()



    with allure.step(
    "验证购物车商品"
):

        cart_page.open_cart()


    name = cart_page.get_product_name()


    assert_contains(
        name,
        data["product"]["name"]
    )


    assert_equal(
        cart_page.get_product_price(),
        data["product"]["price"]
    )


    assert_equal(
        cart_page.get_quantity(),
        data["default"]["quantity"]
    )


    assert_equal(
        cart_page.get_total(),
        data["default"]["total"]
    )