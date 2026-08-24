from pages.base_page import BasePage


class ProductPage(BasePage):

    # 商品入口（导航栏链接，避免空购物车页 "here" 链接冲突）
    PRODUCTS_LINK = "ul.nav li a[href='/products']"


    # 搜索框
    SEARCH_INPUT = "#search_product"


    # 搜索按钮
    SEARCH_BUTTON = "#submit_search"


    # 商品列表标题
    SEARCH_RESULT_TITLE = "h2.title"

    #商品详情页元素定位
    PRODUCT_CARD = ".productinfo"


    PRODUCT_NAME = ".product-information h2"


    PRODUCT_PRICE = ".product-information span"


    PRODUCT_CATEGORY = ".product-information p"

    #加入购物车元素定位
    ADD_CART_BUTTON = "button:has-text('Add to cart')"

    QUANTITY_INPUT = "#quantity"

    def open_products(self):

        self.click(
            self.PRODUCTS_LINK
        )


    def search_product(self, keyword):

        self.fill(
            self.SEARCH_INPUT,
            keyword
        )

        self.click(
            self.SEARCH_BUTTON
        )


    def get_result_title(self):

        return self.get_text(
            self.SEARCH_RESULT_TITLE
        )

    def click_product(self):

        self.click(
            "a[href='/product_details/1']:visible"
        )


    def click_category(self, panel_id):
        """
        商品分类筛选：
            panel_id 为左侧分类面板 id，例如 #Women / #Men / #Kids。
            先展开该分类，再点击其下第一个子分类链接，
            页面标题会变为 'WOMEN - ...' / 'MEN - ...' / 'KIDS - ...'。
        """

        self.click(
            f"a[href='{panel_id}']"
        )

        sub = self.page.locator(
            f"{panel_id} a[href^='/category_products/']"
        )

        sub.first.wait_for(
            state="visible",
            timeout=5000
        )

        sub.first.click()


    def get_product_name(self):

        return self.get_text(
            self.PRODUCT_NAME
        )


    def get_product_price(self):

        # 详情页价格为嵌套 span：<span><span>Rs. 500</span>...</span>
        return self.page.locator(
            ".product-information span span"
        ).first.inner_text()


    def get_product_info(self):

        return self.get_text(
            self.PRODUCT_CATEGORY
        )


    def is_product_image_visible(self):

        # 详情页主商品图位于 .view-product 内（唯一），避免 .product-information 内多图触发严格模式
        return (
            self.page
            .locator(".view-product img")
            .first
            .is_visible()
        )

    #加入购物车
    def add_to_cart(self, view_cart=True):
        """
        加入购物车。
        view_cart=True  （默认）点击弹窗中的 "View Cart" 进入购物车；
        view_cart=False         点击 "Continue Shopping" 留在当前页，
                                便于连续添加多件商品。
        """

        self.click(
            self.ADD_CART_BUTTON
        )

        # 等待加购成功弹窗出现
        self.page.locator(
            "#cartModal"
        ).wait_for(
            state="visible",
            timeout=5000
        )

        if view_cart:
            target = self.page.get_by_text(
                "View Cart",
                exact=False
            )
        else:
            target = self.page.get_by_text(
                "Continue Shopping",
                exact=False
            )

        target.first.click()


    def open_product_detail(self, product_id):
        """打开指定 id 的商品详情页（用于多商品购物车场景）。"""

        self.click(
            f"a[href='/product_details/{product_id}']:visible"
        )


    def set_quantity(
        self,
        quantity
    ):

        self.fill(
            self.QUANTITY_INPUT,
            str(quantity)
        )