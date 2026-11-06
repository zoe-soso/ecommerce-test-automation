from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import conftest as framework
from pages.base_page import BasePage


def test_click_uses_timeout_and_waits_for_document_scripts():
    page = MagicMock()
    BasePage(page).click("#button", timeout=2500)
    page.locator.return_value.click.assert_called_once_with(timeout=2500)
    assert page.method_calls[0].__str__() == "call.wait_for_load_state('domcontentloaded')"
    assert page.wait_for_load_state.call_count == 2


def test_fill_does_not_log_input_value(caplog):
    page = MagicMock()
    with caplog.at_level("INFO"):
        BasePage(page).fill("input[type=password]", "private-value-for-regression")
    assert "private-value-for-regression" not in caplog.text
    page.locator.return_value.fill.assert_called_once_with("private-value-for-regression")


@pytest.mark.parametrize("code,message,allowed", [
    (201, "User created!", True),
    (400, "Email Address already exist!", True),
    (400, "Missing required fields", False),
    (503, "Service unavailable", False),
])
def test_account_setup_distinguishes_existing_account_from_service_error(monkeypatch, code, message, allowed):
    response = SimpleNamespace(status_code=200, json=lambda: {"responseCode": code, "message": message})
    monkeypatch.setattr(framework, "ApiClient", lambda *a: SimpleNamespace(create_account=lambda **kw: response))
    fixture = framework.ensure_test_account.__wrapped__()
    if allowed:
        next(fixture)
        fixture.close()
    else:
        with pytest.raises(pytest.fail.Exception, match="账号准备失败"):
            next(fixture)
