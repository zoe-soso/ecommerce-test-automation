"""
API 测试客户端（API Layer）

封装 Automation Exercise 提供的公开接口，供：
    - api_tests/    纯接口自动化测试
    - tests/        部分用例以「API 预置数据 → UI 校验」的混合方式使用

技术栈：requests
设计原则：与 UI 层（pages/）解耦，测试数据可通过 API 独立准备，
         从而把「造数据」与「界面验证」的关注点分开（典型 SDET 思路）。
"""

import requests


DEFAULT_BASE_URL = "https://automationexercise.com"


class ApiClient:
    """对 Automation Exercise API 的轻量封装。"""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL
    ):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0",
            }
        )

    # -----------------------------
    # 商品相关
    # -----------------------------
    def get_products(self):
        """获取商品列表 GET /api/productsList"""
        return self.session.get(
            f"{self.base_url}/api/productsList",
            timeout=20,
        )

    # -----------------------------
    # 账号相关
    # -----------------------------
    def create_account(self, **payload):
        """
        创建账号 POST /api/createAccount
        payload 至少包含：name, email, password,
        title, birth_date, birth_month, birth_year,
        firstname, lastname, address1, country,
        zipcode, state, city, mobile_number
        """
        return self.session.post(
            f"{self.base_url}/api/createAccount",
            data=payload,
            timeout=20,
        )

    def verify_login(self, email: str, password: str):
        """验证登录 POST /api/verifyLogin"""
        return self.session.post(
            f"{self.base_url}/api/verifyLogin",
            data={"email": email, "password": password},
            timeout=20,
        )

    def delete_account(self, email: str, password: str):
        """删除账号 POST /api/deleteAccount（用于测试后清理）"""
        return self.session.post(
            f"{self.base_url}/api/deleteAccount",
            data={"email": email, "password": password},
            timeout=20,
        )
