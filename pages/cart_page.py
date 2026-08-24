from pages.base_page import BasePage


class CartPage(BasePage):

    CART_LINK = "a[href='/view_cart']:visible"

    CART_PRODUCT_NAME = ".cart_description h4 a"

    # 购物车价格 / 数量 / 总额
    CART_PRODUCT_PRICE = ".cart_price p"

    CART_QUANTITY = ".cart_quantity"

    CART_TOTAL = ".cart_total_price"

    # 删除按钮
    CART_REMOVE = "a.cart_quantity_delete"

    # 空购物车标识
    CART_EMPTY = "text=Cart is empty!"


    def open_cart(self):

        self.click(
            self.CART_LINK
        )


    def get_product_name(self):

        return self.get_text(
            self.CART_PRODUCT_NAME
        )


    def get_product_price(self):

        return self.get_text(
            self.CART_PRODUCT_PRICE
        ).strip()


    def get_quantity(self):

        return self.get_text(
            self.CART_QUANTITY
        ).strip()


    def get_total(self):

        return self.get_text(
            self.CART_TOTAL
        ).strip()


    # ===============================
    # 多商品购物车支持
    # ===============================

    @staticmethod
    def _amount(text):
        """将 'Rs. 500' 转为整数 500，便于金额断言。"""
        return int(
            "".join(
                ch for ch in str(text) if ch.isdigit()
            )
        )


    def get_item_count(self):
        """购物车中商品行数。"""
        return (
            self.page
            .locator(".cart_description")
            .count()
        )


    def get_all_product_names(self):
        """返回购物车中所有商品名称列表。"""
        count = self.get_item_count()
        names = []
        for i in range(count):
            names.append(
                self.page
                .locator(".cart_description h4 a")
                .nth(i)
                .inner_text()
            )
        return names


    def get_row_price(self, index=0):
        return (
            self.page
            .locator(self.CART_PRODUCT_PRICE)
            .nth(index)
            .inner_text()
            .strip()
        )


    def get_row_quantity(self, index=0):
        return (
            self.page
            .locator(self.CART_QUANTITY)
            .nth(index)
            .inner_text()
            .strip()
        )


    def get_row_total(self, index=0):
        return (
            self.page
            .locator(self.CART_TOTAL)
            .nth(index)
            .inner_text()
            .strip()
        )


    def get_grand_total(self):
        """
        购物车 / 结算页右侧 'Total Amount' 区域的总价。
        若该区域在页面未渲染（不同站点版本差异），返回 None，
        由调用方决定是否做硬性比对。
        """
        locator = self.page.locator(
            ".total_area span"
        )
        if locator.count() == 0:
            return None
        return (
            locator.first
            .inner_text()
            .strip()
        )


    def remove_product(self):

        # 删除第一条商品
        self.click(
            self.CART_REMOVE
        )


    def is_cart_empty(self):

        return (
            self.page
            .locator(self.CART_EMPTY)
            .count()
            > 0
        )


    def clear_cart(self):

        # 打开购物车并删除全部商品，保证后续断言环境干净
        self.open_cart()

        while (
            self.page
            .locator(self.CART_REMOVE)
            .count()
            > 0
        ):

            self.click(self.CART_REMOVE)

            self.page.wait_for_timeout(1000)
