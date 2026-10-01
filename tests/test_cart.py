"""用 fixture 为购物车测试准备独立的数据。"""

from decimal import Decimal

import pytest

from qa_utils.cart import calculate_cart_total


# 参数化提供不同数量和预期总价；fixture 提供每次测试的新购物车。
@pytest.mark.parametrize(
    "quantity, expected",
    [
        pytest.param(0, Decimal("10.00"), id="zero_quantity"),
        pytest.param(1, Decimal("13.25"), id="one_item"),
        pytest.param(3, Decimal("19.75"), id="three_items"),
    ],
)
def test_total_after_changing_quantity(sample_cart, quantity, expected):
    """修改第一件商品数量，检查总价随之变化。"""
    # 参数名 sample_cart 与 conftest.py 中的 fixture 名称相同。
    # pytest 自动执行 fixture，并把返回的列表传进来，无需手动调用它。
    sample_cart[0]["quantity"] = quantity
    assert calculate_cart_total(sample_cart) == expected


def test_empty_cart(sample_cart):
    """清空当前测试的购物车，总价应为零。"""
    sample_cart.clear()
    assert calculate_cart_total(sample_cart) == Decimal("0.00")


def test_total_after_adding_item(sample_cart):
    """新增单价 2.00、数量 2 的商品，总价应增加 4.00。"""
    sample_cart.append({"unit_price": "2.00", "quantity": 2})
    assert calculate_cart_total(sample_cart) == Decimal("20.50")


def test_total_after_removing_item(sample_cart):
    """移除最后一件商品，只剩 3.25 × 2。"""
    sample_cart.pop()
    assert calculate_cart_total(sample_cart) == Decimal("6.50")


def test_negative_quantity_is_rejected(sample_cart):
    """数量为负数时，应抛出数量校验错误。"""
    sample_cart[0]["quantity"] = -1
    # pytest.raises 检查下面的调用是否抛出指定异常。
    # match 检查错误消息是否包含 quantity；没有抛出异常也会导致测试失败。
    with pytest.raises(ValueError, match="quantity"):
        calculate_cart_total(sample_cart)


def test_negative_price_is_rejected(sample_cart):
    """单价为负数时，应抛出单价校验错误。"""
    sample_cart[0]["unit_price"] = "-1.00"
    with pytest.raises(ValueError, match="unit_price"):
        calculate_cart_total(sample_cart)


def test_original_cart_total(sample_cart):
    """即使前面的测试改过数据，本测试仍拿到新的初始购物车。"""
    assert calculate_cart_total(sample_cart) == Decimal("16.50")
