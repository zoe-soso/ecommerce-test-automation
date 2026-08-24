"""
统一断言封装

将所有散落在测试用例中的 `assert` 收敛到本模块，
好处：
    1. 失败信息格式统一，便于阅读 Allure / 日志；
    2. 失败时同步写入日志，方便定位；
    3. 后续若需接入自定义校验逻辑（如软断言、差异对比），
       只需在此一处扩展。
"""

import logging

from utils.logger import logger


def assert_equal(
    actual,
    expected,
    message=None
):
    if actual != expected:
        msg = (
            message
            or f"断言失败: 期望 {expected!r}, 实际 {actual!r}"
        )
        logger.error(f"ASSERT FAIL: {msg}")
        raise AssertionError(msg)


def assert_text_equal(
    actual,
    expected,
    message=None
):
    if str(actual).strip() != str(expected).strip():
        msg = (
            message
            or f"文本不匹配: 期望 {expected!r}, 实际 {actual!r}"
        )
        logger.error(f"ASSERT FAIL: {msg}")
        raise AssertionError(msg)


def assert_contains(
    container,
    sub,
    message=None
):
    if sub not in container:
        msg = (
            message
            or f"期望包含 {sub!r}, 实际 {container!r}"
        )
        logger.error(f"ASSERT FAIL: {msg}")
        raise AssertionError(msg)


def assert_true(
    condition,
    message=None
):
    if not condition:
        msg = (
            message
            or f"期望为 True, 实际为 {condition!r}"
        )
        logger.error(f"ASSERT FAIL: {msg}")
        raise AssertionError(msg)


def assert_false(
    condition,
    message=None
):
    if condition:
        msg = (
            message
            or f"期望为 False, 实际为 {condition!r}"
        )
        logger.error(f"ASSERT FAIL: {msg}")
        raise AssertionError(msg)


def assert_greater(
    a,
    b,
    message=None
):
    if not a > b:
        msg = message or f"期望 {a} > {b}"
        logger.error(f"ASSERT FAIL: {msg}")
        raise AssertionError(msg)
