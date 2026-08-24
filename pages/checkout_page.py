from pages.base_page import BasePage


class CheckoutPage(BasePage):

    CHECKOUT_BUTTON = "text=Proceed To Checkout"

    ADDRESS_TITLE = "#address_delivery"

    PLACE_ORDER_BUTTON = "a[href='/payment']"


    # 支付表单元素（automationexercise 使用 data-qa 属性）
    NAME_ON_CARD = "input[data-qa='name-on-card']"

    CARD_NUMBER = "input[data-qa='card-number']"

    CARD_CVC = "input[data-qa='cvc']"

    EXPIRY_MONTH = "input[data-qa='expiry-month']"

    EXPIRY_YEAR = "input[data-qa='expiry-year']"

    PAY_BUTTON = "button[data-qa='pay-button']"


    def click_checkout(self):

        self.click(
            self.CHECKOUT_BUTTON
        )


    def get_delivery_address(self):

        return self.get_text(
            self.ADDRESS_TITLE
        )


    def click_place_order(self):

        self.click(
            self.PLACE_ORDER_BUTTON
        )


    def fill_payment(
        self,
        name,
        number,
        cvc,
        month,
        year
    ):

        self.fill(
            self.NAME_ON_CARD,
            name
        )

        self.fill(
            self.CARD_NUMBER,
            number
        )

        self.fill(
            self.CARD_CVC,
            cvc
        )

        self.fill(
            self.EXPIRY_MONTH,
            month
        )

        self.fill(
            self.EXPIRY_YEAR,
            year
        )


    def click_pay_and_confirm(self):

        self.click(
            self.PAY_BUTTON
        )


    def is_order_placed(self):

        # 支付成功后页面出现 "ORDER PLACED!" 标识 / 跳转 payment_done
        if "payment_done" in self.page.url:

            return True

        return (
            "order placed"
            in self.page.content().lower()
        )