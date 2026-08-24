from pages.base_page import BasePage


class BaiduPage(BasePage):

    def open_baidu(self, url):

        self.open(url)


    def get_page_title(self):

        return self.get_title()