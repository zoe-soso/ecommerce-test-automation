import allure


from pages.product_page import ProductPage
from pages.cart_page import CartPage


from utils.config_reader import load_config
from utils.data_reader import load_yaml


config = load_config()

data = load_yaml(
    "data/cart_delete.yaml"
)



@allure.feature(
    "购物车模块"
)
@allure.story(
    "删除商品"
)
def test_delete_cart_product(
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


    product_page.add_to_cart()


    cart_page.open_cart()


    assert (
        data["product"]["name"]
        in
        cart_page.get_product_name()
    )


    cart_page.remove_product()


    assert (
    cart_page.is_cart_empty()
    )