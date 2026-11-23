from unicode_rbnf.decimal_format import format_decimal


def test_format_decimal() -> None:
    assert format_decimal(12345.6789, "#,##0.00") == "12,345.68"
    assert format_decimal(5, "0000.00") == "0005.00"
    assert format_decimal(12345.6, "#,##0.0#") == "12,345.6"
    assert format_decimal(0.1, "#,##0.00") == "0.10"
    assert format_decimal(12345, "#,##0") == "12,345"


def test_format_decimal_indian_grouping() -> None:
    # Primary group of 3, then groups of 2 (lakh/crore)
    assert format_decimal(1234567, "#,##,##0") == "12,34,567"
    assert format_decimal(123456789, "#,##,##0") == "12,34,56,789"
    assert format_decimal(999, "#,##,##0") == "999"
    assert format_decimal(1000, "#,##,##0") == "1,000"
    assert format_decimal(1234567.25, "#,##,##0.0") == "12,34,567.2"
    assert format_decimal(-1234567, "#,##,##0") == "-12,34,567"


def test_format_decimal_optional_fraction_digits() -> None:
    # A "#" after the decimal point is an optional digit: it is shown when the
    # rounded value has a non-zero digit there and dropped otherwise. A "0" is
    # always shown. CLDR's x.x ordinal rule uses "#,##0.#", so 1.5 must keep its
    # ".5" (previously the whole fraction was dropped, giving "1").
    assert format_decimal(1.5, "#,##0.#") == "1.5"
    assert format_decimal(0.5, "#,##0.#") == "0.5"
    assert format_decimal(2.56, "#,##0.#") == "2.6"
    assert format_decimal(1.0, "#,##0.#") == "1"
    assert format_decimal(100.0, "#,##0.#") == "100"
    assert format_decimal(-1.5, "#,##0.#") == "-1.5"
    # Two optional places keep as many non-zero digits as are present.
    assert format_decimal(1.5, "#,##0.##") == "1.5"
    assert format_decimal(2.56, "#,##0.##") == "2.56"
    assert format_decimal(1.0, "#,##0.##") == "1"
    # A required "0" place is always shown, even for a whole number.
    assert format_decimal(1.0, "#,##0.0") == "1.0"
    assert format_decimal(100.0, "#,##0.0") == "100.0"


def test_format_decimal_grouping_edge_cases() -> None:
    assert format_decimal(1234567, "#,##0") == "1,234,567"
    assert format_decimal(-1234567, "#,##0") == "-1,234,567"
    assert format_decimal(1234567, "0") == "1234567"
    assert format_decimal(10**18, "#,##0") == "1,000,000,000,000,000,000"
