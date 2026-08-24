import allure

from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage

from utils.config_reader import load_config
from utils.data_reader import load_yaml
from utils.assertions import (
    assert_true,
    assert_contains
)


config = load_config()

data = load_yaml(
    "data/checkout.yaml"
)


@allure.feature(
    "订单模块"
)
@allure.story(
    "完整下单流程（地址/商品/总价/订单生成）"
)
def test_checkout_full(
    page_context,
    ensure_test_account
):
    """
    下单流程完整校验：
        登录 → 清空购物车 → 加购 → 结算
        → 地址校验 → 商品信息校验 → 总价校验
        → 提交订单 → 支付 → 订单生成（含可下载发票）
    """

    login_page = LoginPage(page_context)
    product_page = ProductPage(page_context)
    cart_page = CartPage(page_context)
    checkout_page = CheckoutPage(page_context)

    account = data["account"]

    # ---------- 登录 ----------
    with allure.step("登录账号"):
        login_page.open(config["base_url"])
        login_page.open_login_page()
        login_page.login(
            account["email"],
            account["password"]
        )
        assert_true(
            login_page.is_login_success(account["name"]),
            "登录失败"
        )

    # ---------- 清空历史残留 ----------
    with allure.step("清空购物车历史残留"):
        cart_page.clear_cart()

    # ---------- 选品加购 ----------
    with allure.step("选择商品并加入购物车"):
        product_page.open(config["base_url"])
        product_page.open_products()
        product_page.click_product()
        product_page.add_to_cart()

    # ---------- 结算 ----------
    with allure.step("进入结算页"):
        checkout_page.click_checkout()

    # ---------- 地址校验 ----------
    with allure.step("校验收货地址"):
        address = (
            checkout_page
            .get_delivery_address()
            .lower()
        )
        for keyword in data["expected_address"]:
            assert_contains(
                address,
                keyword.lower()
            )

    # ---------- 商品信息校验 ----------
    with allure.step("校验订单中的商品信息"):
        names = cart_page.get_all_product_names()
        assert_contains(
            " ".join(names),
            "Blue Top"
        )
        price_text = cart_page.get_row_price(0)
        assert_contains(price_text, "Rs. 500")

    # ---------- 总价校验 ----------
    with allure.step("校验订单总价"):
        assert_true(
            cart_page._amount(
                cart_page.get_row_total(0)
            )
            == cart_page._amount(price_text),
            "订单行总价应与单价一致"
        )

    # ---------- 提交订单 ----------
    with allure.step("提交订单进入支付页"):
        checkout_page.click_place_order()

    # ---------- 支付 ----------
    with allure.step("填写支付信息并确认支付"):
        payment = data["payment"]
        checkout_page.fill_payment(
            payment["name_on_card"],
            payment["card_number"],
            payment["cvc"],
            payment["expiry_month"],
            payment["expiry_year"]
        )
        checkout_page.click_pay_and_confirm()

    # ---------- 订单生成校验 ----------
    with allure.step("校验订单已生成"):
        assert_true(
            checkout_page.is_order_placed(),
            "支付后未生成订单"
        )
        # 出现「下载发票」入口，证明订单已落库并带编号
        assert_true(
            checkout_page.is_visible(
                "text=Download Invoice"
            ),
            "应出现可下载的订单发票"
        )
