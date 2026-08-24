import allure

from pages.product_page import ProductPage
from pages.cart_page import CartPage

from utils.config_reader import load_config
from utils.data_reader import load_yaml


config = load_config()

data = load_yaml(
    "data/cart.yaml"
)


@allure.feature(
    "购物车模块"
)
@allure.story(
    "修改商品数量"
)
def test_update_cart_quantity(
    page_context
):


    product_page = ProductPage(
        page_context
    )


    cart_page = CartPage(
        page_context
    )


    product_page.open(
        config["base_url"]
    )


    product_page.open_products()


    product_page.click_product()


    product_page.set_quantity(
        data["updated"]["quantity"]
    )


    product_page.add_to_cart()


    cart_page.open_cart()


    assert (
        cart_page.get_quantity()
        ==
        data["updated"]["quantity"]
    )