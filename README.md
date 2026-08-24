# Ecommerce UI Automation Test Framework

基于 **Playwright + Pytest** 的电商网站 UI 自动化测试框架，覆盖登录、商品搜索、商品详情、购物车、下单结算等核心业务流程，并具备多浏览器兼容性测试、API+UI 混合测试、Allure 报告与 CI/CD 等能力。

> 被测站点：[Automation Exercise](https://automationexercise.com)（公开电商练习站点）

---

## Tech Stack

| 分类 | 技术 |
| --- | --- |
| 语言 | Python 3.12 |
| 浏览器驱动 | Playwright（Chromium / Firefox / WebKit） |
| 测试框架 | Pytest |
| 测试报告 | Allure、pytest-html |
| 数据驱动 | YAML |
| 接口测试 | Requests |
| 测试数据 | Faker |
| 持续集成 | GitHub Actions |

---

## Project Structure

```
ecommerce-test-automation
│
├── .github/workflows/      # CI/CD：GitHub Actions 自动化测试流水线
│   └── test.yml
│
├── api/                    # API Layer（接口客户端，供接口测试与混合测试复用）
│   └── api_client.py
│
├── api_tests/              # 接口自动化测试（纯 API）
│   ├── test_products_api.py
│   ├── test_login_api.py
│   └── test_register_api.py
│
├── config/                 # 环境配置管理（测试环境可配置）
│   ├── config.yaml         # 共享默认配置
│   ├── test.yaml           # 测试环境
│   ├── dev.yaml            # 开发/预发环境
│   └── prod.yaml           # 生产环境
│
├── data/                   # 测试数据（YAML，数据驱动）
│
├── pages/                  # Page Object（页面对象模型）
│   ├── base_page.py
│   ├── login_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── tests/                  # UI 自动化测试用例
│   ├── test_login.py
│   ├── test_logout.py
│   ├── test_product.py
│   ├── test_product_detail.py
│   ├── test_product_category.py
│   ├── test_cart.py
│   ├── test_cart_delete.py
│   ├── test_cart_quantity.py
│   ├── test_cart_multi.py
│   ├── test_checkout.py
│   ├── test_checkout_full.py
│   ├── test_register.py
│   └── test_api_ui_register.py   # API + UI 混合测试
│
├── utils/                  # 公共工具
│   ├── config_reader.py    # 环境配置读取（合并 config.yaml + 环境文件）
│   ├── data_reader.py      # YAML 数据读取
│   ├── logger.py           # 日志系统
│   ├── assertions.py       # 统一断言封装
│   └── db_helper.py        # 数据库校验（可选，未配置则跳过）
│
├── reports/                # 测试报告（Allure / HTML）
├── screenshots/            # 失败截图
├── logs/                   # 运行日志
├── conftest.py             # 多浏览器参数化、账号保障、失败处理、生命周期日志
├── pytest.ini
└── requirements.txt
```

---

## Features

- **Page Object Model**：页面交互封装在 `pages/`，用例只描述业务步骤，可读性高、易维护。
- **Data Driven Testing**：测试数据集中在 `data/*.yaml`，用例通过 `@pytest.mark.parametrize` 驱动。
- **Multi-browser Testing**：通过覆盖 `browser_name` 固件，用例自动在 Chromium / Firefox / WebKit 三内核各执行一遍（10 条用例 → 30 条执行）。
- **Automatic Screenshot**：用例失败时自动截图，并附到 Allure 报告。
- **Logging System**：每个用例打印 `START TEST` / `END TEST: PASS|FAIL`，失败时记录当前 URL 与异常堆栈。
- **Allure Report**：结构化测试报告，并保留历史趋势（history）。
- **API + UI Hybrid**：可通过 API 预置测试数据，再用 UI 校验，体现 SDET 分层思路。
- **Unified Assertion**：断言统一收敛到 `utils/assertions.py`，失败信息一致、便于排查。
- **Configurable Environments**：`config/` 下按环境切分，`load_config(env)` 合并共享配置与环境配置。
- **CI/CD**：提交代码即触发 GitHub Actions 自动安装依赖、运行测试并生成 Allure 报告。

---

## Test Coverage

| 模块 | 覆盖点 |
| --- | --- |
| 用户登录 | 正常登录、错误密码、退出登录 |
| 注册 | 正常注册、邮箱重复、空字段 |
| 商品 | 商品搜索（iPhone / dress）、商品分类筛选（Women / Men / Kids） |
| 商品详情 | 商品名称、价格、图片 |
| 购物车 | 添加商品、删除商品、修改数量、多商品购物车 |
| 下单结算 | 地址校验、商品信息校验、总价校验、订单生成、订单记录 |
| 接口测试 | 商品列表、登录验证、账号注册 |
| 混合测试 | API 创建账号 → UI 验证登录 |

---

## Environment Configuration

所有环境配置集中在 `config/` 目录：

- `config.yaml` —— 共享默认值（base_url、browser、timeout 等）
- `test.yaml` / `dev.yaml` / `prod.yaml` —— 具体环境覆盖

`utils/config_reader.load_config(env="test")` 会先读取 `config.yaml`，再用指定环境文件覆盖同名键。切换环境只改配置，无需改动测试代码。

可通过环境变量控制运行的浏览器：

```bash
# 仅运行 Chromium（CI 调试更快）
BROWSERS=chromium pytest

# 运行全部三种浏览器（默认）
pytest
```

---

## Test Data Management

- **YAML 驱动**：业务用例数据写在 `data/*.yaml`，与脚本解耦。
- **Faker 生成**：注册 / 接口测试中使用 `Faker` 动态生成唯一邮箱、用户名、地址等，避免固定账号冲突。

---

## How to Run

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装浏览器驱动

```bash
playwright install chromium firefox webkit
```

### 3. 执行测试

```bash
# 运行全部用例（默认三浏览器）
pytest

# 仅运行 Chromium
BROWSERS=chromium pytest

# 运行指定用例
pytest tests/test_login.py
pytest tests/test_product.py -k "iPhone"
```

### 4. 生成 / 查看报告

```bash
# 生成 Allure 报告（保留历史趋势）
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

# pytest-html 报告位于 reports/report.html
```

---

## CI/CD

`.github/workflows/test.yml` 定义了完整的自动化流水线：

```
push / pull_request
      ↓
checkout 代码
      ↓
安装 Python 依赖
      ↓
安装 Chromium / Firefox / WebKit
      ↓
运行 pytest（输出 Allure 结果）
      ↓
生成 Allure 报告（合并历史趋势）
      ↓
上传报告产物
```

每次提交都会自动执行测试并产出报告，体现「代码提交 → 自动测试 → 生成报告」的真实工程流程。

---

## 设计亮点（面试要点）

1. **页面对象模型 + 数据驱动**：降低耦合，数据与脚本分离。
2. **多浏览器兼容性测试**：一套用例覆盖三大内核，用例数 10 → 30。
3. **失败可观测**：自动截图 + 结构化日志（URL/异常）+ Allure 报告。
4. **API 与 UI 分层**：`api/` 独立封装，支持「接口造数、界面验证」的混合模式。
5. **环境可配置**：`config/` 按环境管理，一键切换。
6. **CI/CD 落地**：GitHub Actions 实现提交即测，报告带历史趋势。
