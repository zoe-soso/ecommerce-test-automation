"""
本地代理环境隔离

问题背景：
    开发机上常开着代理 / 抓包软件（Clash、Charles、Fiddler 等），
    它们会把 HTTP_PROXY / HTTPS_PROXY 指向 127.0.0.1 的某个端口。
    一旦代理软件未启动或端口已关闭，requests / urllib 发出的所有
    外部请求都会因 ProxyError 直接失败，表现为「接口用例整片报红」，
    很容易被误判成代码或站点的问题。

解决策略：
    只清理「指向本机回环地址」的代理变量。
    这样既能排除本地代理软件的干扰，又不会影响企业内网中指向
    真实网关的代理配置——那种代理是访问外网所必需的，不能一刀切。

调用时机：
    由 conftest.py 的 pytest_configure 钩子在测试启动前统一执行，
    UI 用例与接口用例都会受益。
"""

import ipaddress
import os

from urllib.parse import urlparse

from utils.logger import logger


PROXY_ENV_KEYS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)


def _is_loopback_proxy(value: str) -> bool:
    """
    判断代理地址是否指向本机回环。

    兼容三种写法：
        127.0.0.1:20809          （不带 scheme）
        http://127.0.0.1:20809   （带 scheme）
        localhost:20809
    """

    if not value:
        return False

    if "://" not in value:
        value = "http://" + value

    try:
        host = urlparse(value).hostname
    except Exception:
        return False

    if not host:
        return False

    if host.lower() == "localhost":
        return True

    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        # 主机名不是 IP（例如企业内网代理域名），不视为本机回环
        return False


def disable_loopback_proxy():
    """
    清理指向本机的代理环境变量。

    返回被清理的变量名列表，便于写入日志、也让行为可观测。
    """

    removed = []

    for key in PROXY_ENV_KEYS:

        value = os.environ.get(key)

        if value and _is_loopback_proxy(value):
            os.environ.pop(key, None)
            removed.append(key)

    return removed


def ensure_clean_proxy_env():
    """对外入口：执行清理并记录日志。"""

    removed = disable_loopback_proxy()

    if removed:
        logger.info(
            "检测到指向本机的代理环境变量，已忽略: "
            + ", ".join(removed)
        )

    return removed
