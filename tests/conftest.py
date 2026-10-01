"""集中准备 tests 目录下多个测试文件共用的数据。"""

import pytest


# fixture 负责准备测试所需的数据，不负责判断测试是否通过。
# scope="function" 表示每个测试场景都重新执行一次这个准备函数。
# 列表和其中的字典都在函数内部新建，避免不同测试修改同一份数据。
# pytest 会自动发现 conftest.py 中的 fixture，测试文件不用手动导入它。
@pytest.fixture(scope="function")
def sample_cart():
    """为每个测试提供一份新购物车，初始总价为 16.50。"""
    return [
        {"unit_price": "3.25", "quantity": 2},
        {"unit_price": "10.00", "quantity": 1},
    ]
