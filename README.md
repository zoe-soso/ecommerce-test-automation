# 电商网站自动化测试

![CI](https://github.com/zoe-soso/ecommerce-test-automation/actions/workflows/test.yml/badge.svg)

用 pytest、Playwright 和 requests 测试 [Automation Exercise](https://automationexercise.com)。UI 测试按 POM 拆分页面操作，数据放在 YAML 中。

目前有 19 条 UI 用例和 6 条 API 用例，涉及登录、注册、商品、购物车和下单。这里只测试练习站提供的流程，不涉及真实付款。

## 本地运行

Python 3.12，以下命令在项目根目录用 PowerShell 执行：

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m playwright install chromium firefox webkit

# Chromium：25 次执行，不重试，输出 HTML 和 Allure 结果
.\venv\Scripts\python.exe -m pytest -o addopts= --browser chromium --reruns 0 --html=reports/report.html --self-contained-html --alluredir=reports/allure-results

# 三浏览器：19 × 3 + 6 = 63 次执行，默认失败重试一次
.\venv\Scripts\python.exe -m pytest

# 只跑 API
.\venv\Scripts\python.exe -m pytest api_tests -o addopts=

# 静态检查
.\venv\Scripts\python.exe -m ruff check .
```

`pytest.ini` 已设置三浏览器。运行单浏览器时要先用 `-o addopts=` 清空默认参数，直接追加 `--browser chromium` 会重复收集用例。

## 目录与配置

```text
pages/       页面对象
tests/       UI 和 API + UI 测试
api/         requests 客户端
api_tests/   API 测试
data/        测试数据
config/      环境配置
utils/       配置读取、断言、日志
conftest.py  账号准备、页面 fixture、失败截图
```

配置先读取 `config/config.yaml`，再用 `config/test.yaml` 覆盖。切换环境目前需要修改 `load_config()` 的入参。

默认过滤第三方广告和字体请求，保留本站脚本、接口、图片和页面请求。需要检查原始页面时，将 `block_external_noise` 设为 `false`。页面操作等待 DOMContentLoaded 和目标元素，不使用强制点击绕过失败。

测试启动时清理回环地址的代理变量；API 客户端不读取环境代理。输入日志不记录字段值，账号准备失败会直接报错。

## 报告和 CI

- `reports/report.html`：pytest HTML 报告。
- `reports/allure-results/`：Allure 原始数据；安装 Allure CLI 后可运行 `allure serve reports/allure-results`。
- `screenshots/`、`logs/`：失败截图和执行日志。

GitHub Actions 默认运行 Chromium，包含 Ruff 检查、测试和报告上传；手动运行可选择其他浏览器或三浏览器。Allure 的新历史从生成后的报告中保存，供下次运行恢复。工作流没有部署步骤。

测试依赖公共站点和网络。查看运行结果时应同时看日期、浏览器、重试次数和日志，一次通过不代表长期稳定。
