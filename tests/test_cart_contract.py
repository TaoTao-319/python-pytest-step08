"""验证金额舍入、可迭代输入和调用前后数据一致性。"""

from copy import deepcopy
from decimal import Decimal, ROUND_DOWN, localcontext

import pytest

from qa_utils import calculate_cart_total


@pytest.mark.parametrize(
    "items, expected",
    [
        pytest.param(
            [{"unit_price": "1.005", "quantity": 1}],
            Decimal("1.00"),
            id="half_even_round_down",
        ),
        pytest.param(
            [{"unit_price": "1.015", "quantity": 1}],
            Decimal("1.02"),
            id="half_even_round_up",
        ),
        pytest.param(
            [
                {"unit_price": "0.005", "quantity": 1},
                {"unit_price": "0.005", "quantity": 1},
            ],
            Decimal("0.01"),
            id="round_after_summing",
        ),
    ],
)
def test_total_uses_explicit_half_even_rounding(items, expected):
    """外部舍入模式变化时，函数仍按自身明确的规则计算。"""
    with localcontext() as context:
        context.rounding = ROUND_DOWN
        result = calculate_cart_total(items)
    assert result == expected
    assert result.as_tuple().exponent == -2


def test_generator_input_is_supported():
    """商品输入可以是生成器，不能依赖列表下标或长度。"""
    items = (
        {"unit_price": price, "quantity": quantity}
        for price, quantity in [("3.25", 2), ("10.00", 1)]
    )
    assert calculate_cart_total(items) == Decimal("16.50")


def test_calculation_does_not_modify_input(sample_cart):
    """计算不应改写调用方的价格、数量或商品顺序。"""
    before = deepcopy(sample_cart)
    assert calculate_cart_total(sample_cart) == Decimal("16.50")
    assert sample_cart == before
