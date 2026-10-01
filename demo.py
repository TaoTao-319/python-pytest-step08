"""无需设置 PYTHONPATH 即可运行的项目演示入口。"""

from pathlib import Path
import sys

# 仅为直接运行演示添加项目源码目录；pytest 使用 pytest.ini 配置。
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from qa_utils import calculate_cart_total, is_password_valid, is_phone_number


def main():
    cart = [
        {"unit_price": "3.25", "quantity": 2},
        {"unit_price": "10.00", "quantity": 1},
    ]
    print(f"Phone validation: {is_phone_number('13812345678')}")
    print(f"Password validation: {is_password_valid('Abc12345')}")
    print(f"Cart total: {calculate_cart_total(cart)}")


if __name__ == "__main__":
    main()
