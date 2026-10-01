"""购物车金额计算练习函数。"""

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN

# items：参数名，表示一组商品。
# Iterable[...]：这组商品可以用 for 循环逐个取出，例如列表。
# Mapping[str, object]：每个商品是字典一类的数据，键是字符串，值可以是不同类型。
# -> Decimal：函数返回一个 Decimal 十进制数，用来表示金额。
# 最后的冒号：表示接下来是函数内部的代码。

def calculate_cart_total(items: Iterable[Mapping[str, object]]) -> Decimal:
    """计算商品总价，返回保留两位小数的 Decimal。

    每个商品需要包含 `unit_price` 和 `quantity`。价格必须是非负数，
    数量必须是非负整数。空购物车总价为 Decimal("0.00")。
    """
    total = Decimal("0.00")

    for index, item in enumerate(items, start=1):
        try:
            unit_price = Decimal(str(item["unit_price"]))
        # KeyError：商品字典缺少 "unit_price" 这个键。
        # InvalidOperation：无法转换成 Decimal，例如单价是 "abc"。
        # TypeError：操作用到了不合适的数据类型。
        except (KeyError, InvalidOperation, TypeError) as error:
            raise ValueError(f"第 {index} 个商品的 unit_price 无效") from error

        # is_finite()：检查是否为有限数值。
        if not unit_price.is_finite() or unit_price < 0:
            raise ValueError(f"第 {index} 个商品的 unit_price 必须是非负数")

        quantity = item.get("quantity")
        # not isinstance(quantity, int)：数量不是整数。
        # isinstance(quantity, bool)：数量是 True 或 False；Python 将布尔值视为整数的一种，需要单独排除。
        # quantity < 0：数量是负数。
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
            raise ValueError(f"第 {index} 个商品的 quantity 必须是非负整数")

        total += unit_price * quantity

    # Decimal("0.01")：指定精确到百分位，也就是两位小数。
    # quantize(...)：按这个小数位数调整 total，需要时进行舍入。
    # 明确使用银行家舍入，避免外部代码修改 Decimal 舍入设置后结果改变。
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
