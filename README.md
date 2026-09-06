# Ecommerce UI Automation Test Framework

基于 **Playwright + Pytest** 的电商网站 UI 自动化测试框架，覆盖登录、注册、商品搜索、商品详情、购物车、下单结算等核心业务流程，并具备多浏览器兼容性测试、API+UI 混合测试、Allure 报告与 CI/CD 等能力。

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
│   ├── conftest.py         # api_client fixture，base_url 取自 config/
│   ├── test_products_api.py
│   ├── test_login_api.py
│   └── test_register_api.py
│
├── config/                 # 配置管理（按环境分层）
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
│   ├── config_reader.py    # 配置读取（合并 config.yaml + 环境文件）
│   ├── data_reader.py      # YAML 数据读取
│   ├── logger.py           # 日志系统
│   ├── assertions.py       # 统一断言封装
│   └── env_guard.py        # 本地代理隔离（清理指向本机的代理变量）
│
├── reports/                # 测试报告（Allure / HTML）
├── screenshots/            # 失败截图
├── logs/                   # 运行日志
├── conftest.py             # 环境预处理、账号保障、失败处理、生命周期日志
├── pytest.ini
└── requirements.txt
```

---

## Features

- **Page Object Model**：页面交互封装在 `pages/`，用例只描述业务步骤，可读性高、易维护。
- **Data Driven Testing**：测试数据集中在 `data/*.yaml`，用例通过 `@pytest.mark.parametrize` 驱动。
- **Multi-browser Testing**：pytest-playwright 的 `--browser` 参数让 UI 用例自动在 Chromium / Firefox / WebKit 三内核各执行一遍（19 条 UI 用例 → 57 次执行，全量 63 次）。
- **Automatic Screenshot**：用例失败时自动截图，并附到 Allure 报告。
- **Logging System**：每个用例打印 `START TEST` / `END TEST: PASS|FAIL`，失败时记录当前 URL 与异常堆栈。
- **Allure Report**：结构化测试报告，并保留历史趋势（history）。
- **API + UI Hybrid**：可通过 API 预置测试数据，再用 UI 校验，体现 SDET 分层思路。
- **Unified Assertion**：断言统一收敛到 `utils/assertions.py`，失败信息一致、便于排查。
- **Proxy Environment Isolation**：`utils/env_guard.py` 在启动前清理指向本机的代理变量，避免本地代理软件未启动时接口用例整片报 ProxyError。
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
| 下单结算 | 地址校验、商品信息校验、总价校验、订单生成 |
| 接口测试 | 商品列表、登录验证、账号注册 |
| 混合测试 | API 创建账号 → UI 验证登录 |

**用例规模**：UI 用例 19 条、接口用例 6 条。

- CI 默认（Chromium 单内核）：**25 次执行**
- 本地全量回归（三内核）：**63 次执行**（19 × 3 + 6）

---

## Environment Configuration

所有配置集中在 `config/` 目录：

- `config.yaml` —— 共享默认值（base_url、browser、timeout 等）
- `test.yaml` / `dev.yaml` / `prod.yaml` —— 具体环境覆盖

`utils/config_reader.load_config(env="test")` 会先读取 `config.yaml`，再用指定环境文件覆盖同名键，返回合并后的完整配置。

接口层的 `base_url` 同样取自这份配置（`api_tests/conftest.py`），因此 **UI 层与接口层共用同一份配置来源**，不存在「UI 走配置、接口走硬编码」的双份维护。

> 当前 `env` 以默认参数 `test` 加载，切换环境需修改调用处入参；后续可接入 `--env` 命令行选项或 `TEST_ENV` 环境变量，把切换动作外提到执行入口。

可通过 `--browser` 参数控制运行的浏览器（pytest-playwright 原生支持）：

```bash
# 仅运行 Chromium（CI 默认，速度更快）
pytest --browser chromium

# 运行全部三种浏览器（本地全量回归）
pytest --browser chromium --browser firefox --browser webkit
```

### 本地代理隔离

开发机上常开着代理 / 抓包软件，它们会把 `HTTP_PROXY` 指向 `127.0.0.1` 的某个端口；一旦代理未启动，`requests` 的所有请求都会因 `ProxyError` 失败，表现为接口用例整片报红。

框架做了两层隔离：

1. `utils/env_guard.py` 在 `pytest_configure` 阶段清理**指向本机回环**的代理变量 —— 只清回环地址，不影响企业内网指向真实网关的代理；
2. `ApiClient` 设置 `session.trust_env = False`，接口请求不读取任何代理配置。

---

## Test Data Management

- **YAML 驱动**：业务用例数据写在 `data/*.yaml`，与脚本解耦。
- **Faker 生成**：注册 / 接口测试中使用 `Faker` 动态生成唯一邮箱、用户名、地址等，避免固定账号冲突。
- **单一数据源**：接口登录用例的账号取自 `data/login.yaml`，与 UI 登录用例共用同一份数据，避免同一账号多处硬编码。

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

# 仅运行 Chromium（与 CI 一致）
pytest --browser chromium

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
安装 Chromium（CI 默认，更快更稳）
      ↓
解析上一次成功运行的 ID，恢复 Allure history
      ↓
运行 pytest（输出 Allure 结果，失败自动重试 1 次）
      ↓
生成 Allure 报告（测试失败也会生成，方便排查）
      ↓
上传 Allure 报告 / history / 截图 / 日志
      ↓
最终判定（失败则 Job 标红）
```

- **默认触发**：`push` / `pull_request` 自动跑 Chromium 单浏览器，兼顾速度与稳定性。
- **手动触发**：`workflow_dispatch` 可选择 `chromium,firefox,webkit` 跑全量多浏览器回归。
- **失败不中断**：pytest 步骤带 `continue-on-error`，后续步骤带 `if: always()`，保证失败时依然能生成报告并上传截图、日志；最后由 `Check pytest result` 统一判定标红。
- **历史趋势**：`actions/download-artifact@v4` 默认只取当前 run 的 artifact，跨 run 下载必须显式给出 `run-id` 与 `github-token`，因此流水线先用 `github-script` 查询上一次成功运行的 ID 再下载。

体现「代码提交 → 自动测试 → 生成报告 → 保留历史趋势」的真实工程流程。

---

## 设计亮点

1. **页面对象模型 + 数据驱动**：降低耦合，数据与脚本分离。
2. **多浏览器兼容性测试**：一套用例覆盖三大内核，25 次执行扩展到 63 次。
3. **失败可观测**：自动截图 + 结构化日志（URL/异常）+ Allure 报告。
4. **API 与 UI 分层**：`api/` 独立封装，支持「接口造数、界面验证」的混合模式。
5. **配置集中管理**：`config/` 按环境分层，UI 与接口共用同一份 `base_url`。
6. **环境干扰隔离**：代理变量清洗 + 接口客户端禁用代理，排除本地环境差异。
7. **CI/CD 落地**：GitHub Actions 实现提交即测，报告带历史趋势。

---

## Known Issues & Next Steps

- **`--reruns 1` 会掩盖 flaky**：失败重跑能提升 CI 通过率，但也会隐藏不稳定用例；后续应统计 flaky 用例并单独告警，而不是静默重试。
- **接口断言层次偏浅**：目前覆盖到 HTTP 状态码、业务响应码、字段非空三层，尚未做 JSON Schema 契约校验、异常入参与响应时间断言。
- **环境切换尚未外提**：`load_config(env)` 仍以默认参数加载，计划接入 `--env` 命令行选项。
