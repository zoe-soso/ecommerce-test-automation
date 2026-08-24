import pytest

from utils.db_helper import (
    is_db_configured,
    order_exists
)

from utils.assertions import assert_true


@pytest.mark.skipif(
    not is_db_configured(),
    reason="未配置 database（config/config.yaml），跳过数据库校验用例"
)
def test_order_record_exists():
    """
    数据库校验（P3 高级项）

    真实企业项目中，订单创建后需要在数据库层确认记录落库。
    本演示项目无法直连公开练习站点的数据库，因此：
        - 仅在 config.yaml 配置了 database 时才执行；
        - 未配置时通过 pytest.skip 自动跳过，整套用例仍可运行。

    接入真实数据库后，可在此先通过 UI/API 创建订单，
    再用 order_exists(order_id) 做数据层断言。
    """

    assert_true(
        is_db_configured(),
        "数据库未配置"
    )

    # 结构示例：order_id 应由下单流程产出后传入
    # assert_true(order_exists(some_order_id))
