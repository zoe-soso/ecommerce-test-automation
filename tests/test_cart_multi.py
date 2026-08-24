import allure

from pages.product_page import ProductPage
from pages.cart_page import CartPage

from utils.config_reader import load_config
from utils.assertions import (
    assert_equal,
    assert_contains,
    assert_greater
)


config = load_config()


@allure.feature(
    "购物车模块"
)
@allure.story(
    "多商品购物车"
)
def test_multi_product_cart(
    page_context
):
    """
    多商品购物车：
        添加商品 A（Blue Top）和商品 B（Men Tshirt），
        校验商品数量、名称、单价、行总价与合计总价。
    """

    product_page = ProductPage(
        page_context
    )

    cart_page = CartPage(
        page_context
    )

    # ---- 添加商品 A（Blue Top, 详情页 1）----
    with allure.step(
        "添加商品 A 并继续购物"
    ):
        product_page.open(
            config["base_url"]
        )
        product_page.open_products()
        product_page.click_product()
        product_page.add_to_cart(
            view_cart=False
        )

    # ---- 添加商品 B（Men Tshirt, 详情页 2）----
    with allure.step(
        "添加商品 B 并进入购物车"
    ):
        product_page.open(
            config["base_url"]
        )
        product_page.open_products()
        product_page.open_product_detail(2)
        product_page.add_to_cart(
            view_cart=True
        )

    # ---- 校验 ----
    with allure.step(
        "校验购物车商品数量"
    ):
        assert_equal(
            cart_page.get_item_count(),
            2
        )

    with allure.step(
        "校验两件商品均存在"
    ):
        names = cart_page.get_all_product_names()
        joined = " ".join(names)
        assert_contains(joined, "Blue Top")
        assert_contains(joined, "Men Tshirt")

    with allure.step(
        "校验每件商品数量与行总价（数量均为 1）"
    ):
        for i in range(
            cart_page.get_item_count()
        ):
            assert_equal(
                cart_page.get_row_quantity(i),
                "1"
            )
            # 行总价 == 单价（数量为 1）
            assert_equal(
                cart_page._amount(
                    cart_page.get_row_total(i)
                ),
                cart_page._amount(
                    cart_page.get_row_price(i)
                )
            )

    with allure.step(
        "校验购物车总价 = 各行总价之和"
    ):
        expected_total = sum(
            cart_page._amount(
                cart_page.get_row_total(i)
            )
            for i in range(
                cart_page.get_item_count()
            )
        )

        assert_greater(expected_total, 0)

        # 若页面能定位到显示的总价，则进一步比对（无法定位时跳过）
        displayed = cart_page.get_grand_total()
        if displayed is not None:
            assert_equal(
                cart_page._amount(displayed),
                expected_total
            )
