"""用于测试设计练习的简单输入校验函数。"""


def is_phone_number(value: object) -> bool:
    """按教学规则判断手机号样例是否有效。

    规则：必须是以 1 开头的 11 位 ASCII 数字字符串。
    这只是稳定的练习规则，不用于真实手机号校验。
    """
    # isinstance(value, str)：检查 value 是否为字符串。
    if not isinstance(value, str):
        return False

    return (
        len(value) == 11
        and value.startswith("1")
        and value.isascii()
        and value.isdigit()
    )


def is_password_valid(value: object) -> bool:
    """按教学规则判断密码样例是否有效。

    规则：长度为 8 到 20 个字符，至少包含一个英文字母和一个数字。
    """
    if not isinstance(value, str) or not 8 <= len(value) <= 20:
        return False

    has_ascii_letter = any(char.isascii() and char.isalpha() for char in value)
    has_ascii_digit = any(char.isascii() and char.isdigit() for char in value)
    return has_ascii_letter and has_ascii_digit
