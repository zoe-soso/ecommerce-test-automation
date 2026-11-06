"""每次测试独立的练习账号邮箱。"""

from uuid import uuid4


def unique_email():
    return f"qa_{uuid4().hex}@example.com"
