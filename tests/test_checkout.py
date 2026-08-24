import allure

from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage

from utils.config_reader import load_config
from utils.data_reader import load_yaml


config = load_config()

data = load_yaml(
    "data/checkout.yaml"
)


@allure.feature(
    "订单模块"
)
@allure.story(
    "完整下单流程"
)
def test_place_order(
    page_context,
    ensure_test_account
):
    """
    下单流程：登录 -> 选择商品 -> 加入购物车
    -> 提交订单 -> 支付页面 -> 校验订单生成
    """

    login_page = LoginPage(
        page_context
    )

    product_page = ProductPage(
        page_context
    )

    cart_page = CartPage(
        page_context
    )

    checkout_page = CheckoutPage(
        page_context
    )


    with allure.step(
        "登录账号"
    ):

        account = data["account"]

        login_page.open(
            config["base_url"]
        )

        login_page.open_login_page()

        login_page.login(
            account["email"],
            account["password"]
        )

        assert login_page.is_login_success(
            account["name"]
        )


    with allure.step(
        "清空购物车历史残留"
    ):

        cart_page.clear_cart()


    with allure.step(
        "选择商品并加入购物车"
    ):

        product_page.open(
            config["base_url"]
        )

        product_page.open_products()

        product_page.click_product()

        product_page.add_to_cart()


    with allure.step(
        "进入结算页并提交订单"
    ):

        checkout_page.click_checkout()

        address = (
            checkout_page
            .get_delivery_address()
            .lower()
        )

        for keyword in data["expected_address"]:

            assert (
                keyword.lower() in address
            ), f"收货地址缺少关键字: {keyword}"


        checkout_page.click_place_order()


    with allure.step(
        "在支付页面填写信息并确认支付"
    ):

        payment = data["payment"]

        checkout_page.fill_payment(
            payment["name_on_card"],
            payment["card_number"],
            payment["cvc"],
            payment["expiry_month"],
            payment["expiry_year"]
        )

        checkout_page.click_pay_and_confirm()


    with allure.step(
        "校验订单已生成"
    ):

        assert checkout_page.is_order_placed()
