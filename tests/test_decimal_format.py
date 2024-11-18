from unicode_rbnf.decimal_format import format_decimal


def test_format_decimal() -> None:
    assert format_decimal(12345.6789, "#,##0.00") == "12,345.68"
    assert format_decimal(5, "0000.00") == "0005.00"
    assert format_decimal(12345.6, "#,##0.0#") == "12,345.6"
    assert format_decimal(0.1, "#,##0.00") == "0.10"
    assert format_decimal(12345, "#,##0") == "12,345"
