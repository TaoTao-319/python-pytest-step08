"""隔离的错误预期演示：显式运行时会失败，不属于默认测试集。"""

from decimal import Decimal

from qa_utils import calculate_cart_total


def test_wrong_expected_total():
    """正确总价为 16.50；错误断言用于学习阅读 pytest 失败输出。"""
    items = [
        {"unit_price": "3.25", "quantity": 2},
        {"unit_price": "10.00", "quantity": 1},
    ]
    actual = calculate_cart_total(items)
    assert actual == Decimal("16.00")
