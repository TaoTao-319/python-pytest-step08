"""与 test_cart.py 共用 conftest.py 的 fixture。"""

from decimal import Decimal

import pytest

from qa_utils.cart import calculate_cart_total


# sample_cart 来自同目录的 conftest.py，通过测试函数参数直接请求。
def test_missing_unit_price_is_rejected(sample_cart):
    """缺少单价字段时，错误消息应指出第一个商品的单价有问题。"""
    # del：删除第一个商品的 unit_price 字段，模拟缺少单价的情况。
    del sample_cart[0]["unit_price"]
    with pytest.raises(ValueError, match="第 1 个商品的 unit_price 无效"):
        calculate_cart_total(sample_cart)


def test_missing_quantity_is_rejected(sample_cart):
    """缺少数量字段时，item.get 返回 None，数量检查应拒绝它。"""
    del sample_cart[0]["quantity"]
    with pytest.raises(ValueError, match="第 1 个商品的 quantity"):
        calculate_cart_total(sample_cart)


def test_boolean_quantity_is_rejected(sample_cart):
    """True 虽然是 int 的子类实例，但不能作为有效商品数量。"""
    sample_cart[0]["quantity"] = True
    with pytest.raises(ValueError, match="quantity"):
        calculate_cart_total(sample_cart)


def test_nan_price_is_rejected(sample_cart):
    """NaN 可以转换成 Decimal，但 is_finite 检查应拒绝它。"""
    sample_cart[0]["unit_price"] = "NaN"
    with pytest.raises(ValueError, match="unit_price"):
        calculate_cart_total(sample_cart)


def test_zero_price_is_allowed(sample_cart):
    """零单价属于合法边界，第一件商品免费时只计第二件商品的金额。"""
    sample_cart[0]["unit_price"] = "0.00"
    assert calculate_cart_total(sample_cart) == Decimal("10.00")
