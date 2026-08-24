from playwright.sync_api import Page
from utils.logger import logger
from datetime import datetime


class BasePage:

    def __init__(self, page: Page):
        self.page = page


    def open(self,url):

        logger.info(f"打开页面: {url}")

        self.page.goto(
            url,
            timeout=60000,
            wait_until="domcontentloaded"
        )


    def get_title(self):
        """
        获取页面标题
        """
        logger.info("获取页面标题")

        return self.page.title()


    def click(self, locator, timeout=10000):

        logger.info(f"点击元素:{locator}")

        element = self.page.locator(locator)

        element.wait_for(
        state="visible",
        timeout=timeout
        )

        element.click()


    def fill(self, locator, text):
        text = str(text)
        
        logger.info(
        f"输入:{text}"
        )
        
        element = self.page.locator(locator)

        element.wait_for(
        state="visible"
        )

        element.fill(text)


    def get_text(self, locator):
        """
        获取元素文本
        """
        logger.info(f"获取元素文本: {locator}")

        return self.page.locator(locator).inner_text()


    def wait_for_visible(self, locator, timeout=5000):
        """
        等待元素可见
        """
        logger.info(f"等待元素可见: {locator}")

        self.page.locator(locator).wait_for(
            state="visible",
            timeout=timeout
        )


    def screenshot(self, name="screenshot"):
        """
        页面截图
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        path = f"screenshots/{name}_{timestamp}.png"

        logger.info(f"截图保存: {path}")

        self.page.screenshot(
            path=path,
            full_page=True
        )

        return path


    def get_url(self):
        """
        获取当前页面URL
        """

        logger.info("获取当前页面URL")

        return self.page.url


    def reload(self):
        """
        刷新页面
        """

        logger.info("刷新页面")

        self.page.reload()


    def go_back(self):
        """
        返回上一页
        """

        logger.info("返回上一页")

        self.page.go_back()


    def press(self, locator, key):

        logger.info(
        f"键盘操作:{key}"
        )   

        element = self.page.locator(locator)

        element.wait_for(
        state="visible"
        )

        element.press(key)

    def is_visible(self, locator):

        try:

            self.page.locator(locator).wait_for(
                state="visible",
                timeout=3000
            )

            return True

        except Exception:

            return False


    def is_visible(
        self,
        locator,
        timeout=3000
    ):

        try:

            self.page.locator(locator).wait_for(
                state="visible",
                timeout=timeout
            )

            return True

        except Exception:

            return False