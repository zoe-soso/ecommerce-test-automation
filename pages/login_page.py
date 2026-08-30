from pages.base_page import BasePage


class LoginPage(BasePage):

    # 登录入口按钮
    LOGIN_BUTTON = "a[href='/login']"


    # 登录表单
    EMAIL_INPUT = (
        "input[data-qa='login-email']"
    )

    PASSWORD_INPUT = (
        "input[data-qa='login-password']"
    )


    LOGIN_SUBMIT = (
        "button[data-qa='login-button']"
    )


    # 登录成功标识
    LOGGED_USER = (
        "a:has-text('Logged in as')"
    )


    # 登录失败提示
    ERROR_MESSAGE = (
        "p:has-text('Your email or password is incorrect!')"
    )


    def open_login_page(self):

        self.click(
            self.LOGIN_BUTTON
        )


    def login(
        self,
        email,
        password
    ):

        self.fill(
            self.EMAIL_INPUT,
            email
        )


        self.fill(
            self.PASSWORD_INPUT,
            password
        )


        self.click(
            self.LOGIN_SUBMIT
        )


    def get_login_user(self):

        return self.get_text(
            self.LOGGED_USER
        )


    def get_error_message(self):

        return self.get_text(
            self.ERROR_MESSAGE
        )
    def is_login_success(self, username):

        return self.is_visible(
            f"text=Logged in as {username}"
        )


    # 退出登录入口
    LOGOUT_LINK = "a[href='/logout']"


    def logout(self):

        self.click(
            self.LOGOUT_LINK
        )

        # 退出后回到登录/注册页
        self.page.wait_for_load_state(
            "domcontentloaded"
        )


    def is_logged_out(self):

        # 退出后顶部出现 "Signup / Login" 入口
        return self.is_visible(
            "a[href='/login']"
        )


    # ===============================
    # 注册相关
    # ===============================

    SIGNUP_NAME = (
        "input[data-qa='signup-name']"
    )

    SIGNUP_EMAIL = (
        "input[data-qa='signup-email']"
    )

    SIGNUP_BUTTON = (
        "button[data-qa='signup-button']"
    )

    ACCOUNT_PASSWORD = (
        "input[data-qa='password']"
    )

    FIRST_NAME = "#first_name"

    LAST_NAME = "#last_name"

    ADDRESS1 = "#address1"

    COUNTRY = "#country"

    STATE = "#state"

    CITY = "#city"

    ZIPCODE = "#zipcode"

    MOBILE = "#mobile_number"

    CREATE_ACCOUNT = (
        "button[data-qa='create-account']"
    )

    ACCOUNT_CREATED = (
        "text=ACCOUNT CREATED!"
    )

    DELETE_ACCOUNT_LINK = (
        "a[href='/delete_account']"
    )

    ACCOUNT_DELETED = (
        "text=ACCOUNT DELETED!"
    )


    def signup(self, name, email):
        """
        在 /login 的 “New User Signup!” 表单填写 name + email 并提交。

        返回值：
            True  —— 跳转到了 /signup 注册信息填写页（说明邮箱可用）；
            False —— 停留在 /login（邮箱已存在 / 字段为空等场景，
                     由调用方进一步断言错误提示）。
        """
        self.fill(self.SIGNUP_NAME, name)
        self.fill(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)

        # 新邮箱会跳转到注册信息页并渲染 #id_gender1；
        # 重复邮箱 / 空字段则停留当前页，不会渲染该元素。
        try:
            self.page.wait_for_selector(
                "#id_gender1",
                timeout=20000
            )
            return True
        except Exception:
            return False


    def is_email_exists_error(self):
        """
        注册时邮箱已存在提示。

        站点实际文案为 "Email Address already exist!"（并非
        "Email already exists!"）。这里改用正则匹配并忽略大小写，
        避免站点文案微调导致断言恒失败；提示为异步渲染，给足等待时间。
        """
        return self.is_visible(
            "text=/email address already exist/i",
            timeout=8000
        )


    def fill_account_info(self, info):
        """填写注册第二步的账号信息表单。"""

        self.click("#id_gender1")
        self.fill(self.ACCOUNT_PASSWORD, info["password"])

        self.page.select_option("#days", info["days"])
        self.page.select_option("#months", info["months"])
        self.page.select_option("#years", info["years"])

        self.fill(self.FIRST_NAME, info["firstname"])
        self.fill(self.LAST_NAME, info["lastname"])
        self.fill(self.ADDRESS1, info["address1"])
        self.page.select_option(self.COUNTRY, info["country"])
        self.fill(self.STATE, info["state"])
        self.fill(self.CITY, info["city"])
        self.fill(self.ZIPCODE, info["zipcode"])
        self.fill(self.MOBILE, info["mobile_number"])


    def create_account(self):

        self.click(self.CREATE_ACCOUNT)


    def is_account_created(self):

        return self.is_visible(
            self.ACCOUNT_CREATED
        )


    def delete_account(self):

        self.click(self.DELETE_ACCOUNT_LINK)


    def is_account_deleted(self):

        return self.is_visible(
            self.ACCOUNT_DELETED
        )