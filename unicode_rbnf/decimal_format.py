"""Handle decimal formatting.

See: https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1DecimalFormat.html
"""

from decimal import Decimal
from typing import Optional, Tuple, Union


def _grouping_sizes(integer_pattern: str) -> Optional[Tuple[int, int]]:
    """Return (primary, secondary) grouping sizes from an integer pattern.

    The primary size is the number of digits after the last comma; the
    secondary size is the number of digits between the last two commas, or
    the primary size if there is only one comma. For example, "#,##0" is
    (3, 3) and the Indian "#,##,##0" is (3, 2).
    """
    groups = integer_pattern.split(",")
    if len(groups) < 2:
        return None

    primary = len(groups[-1])
    secondary = len(groups[-2]) if len(groups) > 2 else primary
    if (primary < 1) or (secondary < 1):
        return None

    return primary, secondary


def _apply_grouping(digits: str, primary: int, secondary: int) -> str:
    """Insert grouping commas into a string of digits (with optional sign)."""
    sign = ""
    if digits and (digits[0] in "+-"):
        sign, digits = digits[0], digits[1:]

    if len(digits) <= primary:
        return sign + digits

    groups = [digits[-primary:]]
    digits = digits[:-primary]
    while digits:
        groups.append(digits[-secondary:])
        digits = digits[:-secondary]

    return sign + ",".join(reversed(groups))


def format_decimal(value: Union[int, float, str, Decimal], pattern: str) -> str:
    """Format a number according to a simplified ICU DecimalFormat pattern."""
    # Split the pattern into integer and fractional parts
    if "." in pattern:
        integer_part, fractional_part = pattern.split(".")
    else:
        integer_part, fractional_part = pattern, ""

    # Determine grouping (e.g., thousands or Indian lakh/crore separators)
    grouping = _grouping_sizes(integer_part)
    min_integer_digits = integer_part.replace(",", "").count("0")

    # Determine the number of decimal places
    min_fraction_digits = fractional_part.count("0")
    max_fraction_digits = len(fractional_part)

    # Round the number to the maximum fractional digits
    format_str = f"{{:.{max_fraction_digits}f}}"
    rounded_value = format_str.format(value)

    # Split the rounded value into integer and fractional parts
    if fractional_part:
        integer_value, fractional_value = rounded_value.split(".")
        fractional_value = fractional_value[:max_fraction_digits].rstrip("0")
    else:
        integer_value, fractional_value = rounded_value, ""

    # Apply integer padding
    if len(integer_value) < min_integer_digits:
        integer_value = integer_value.zfill(min_integer_digits)

    # Apply grouping
    if grouping:
        integer_value = _apply_grouping(integer_value, *grouping)

    # Combine integer and fractional parts
    if min_fraction_digits > 0:
        fractional_value = fractional_value.ljust(min_fraction_digits, "0")
        formatted_number = f"{integer_value}.{fractional_value}"
    else:
        formatted_number = integer_value

    return formatted_number
