from unicode_rbnf import FormatPurpose, RbnfEngine


def test_english():
    engine = RbnfEngine.for_language("en")

    assert engine.format_number(7).text == "seven"
    assert engine.format_number(15).text == "fifteen"
    assert engine.format_number(42).text == "forty-two"
    assert engine.format_number(100).text == "one hundred"
    assert engine.format_number(143).text == "one hundred forty-three"
    assert engine.format_number(1000).text == "one thousand"
    assert engine.format_number(1234).text == "one thousand two hundred thirty-four"
    assert engine.format_number(3144).text == "three thousand one hundred forty-four"
    assert engine.format_number(10000).text == "ten thousand"
    assert (
        engine.format_number(83145).text
        == "eighty-three thousand one hundred forty-five"
    )

    assert engine.format_number(100000).text == "one hundred thousand"
    assert (
        engine.format_number(683146).text
        == "six hundred eighty-three thousand one hundred forty-six"
    )

    assert engine.format_number(1000000).text == "one million"
    assert engine.format_number(10000000).text == "ten million"
    assert engine.format_number(100000000).text == "one hundred million"
    assert engine.format_number(1000000000).text == "one billion"

    # Special rules
    assert engine.format_number(-1).text == "minus one"
    assert engine.format_number(-2.0).text == "minus two"

    # Negative fractions keep their fractional part
    assert engine.format_number(-1.5).text == "minus one point five"
    assert engine.format_number(-0.5).text == "minus zero point five"
    assert engine.format_number("-10.75").text == "minus ten point seven five"
    assert (
        engine.format_number(-1234.5).text
        == "minus one thousand two hundred thirty-four point five"
    )

    assert engine.format_number(float("nan")).text == "not a number"
    assert engine.format_number(float("inf")).text == "infinity"
    assert engine.format_number(float("-inf")).text == "minus infinity"

    # Fractions
    assert engine.format_number(3.14).text == "three point one four"
    assert engine.format_number("5.3").text == "five point three"
    assert engine.format_number(0.0123).text == "zero point zero one two three"

    # Small enough that str() would give scientific notation (1e-07)
    assert (
        engine.format_number(1e-7).text
        == "zero point zero zero zero zero zero zero one"
    )

    # Ordinals
    assert engine.format_number(20, FormatPurpose.ORDINAL).text == "twentieth"
    assert engine.format_number(30, FormatPurpose.ORDINAL).text == "thirtieth"
    assert engine.format_number(99, FormatPurpose.ORDINAL).text == "ninety-ninth"
    assert engine.format_number(11, FormatPurpose.ORDINAL).text == "eleventh"

    # Years
    assert engine.format_number(1999, FormatPurpose.YEAR).text == "nineteen ninety-nine"

    # At 1e18 CLDR falls back to the grouped digits (=#,##0=) once English runs
    # out of words, instead of failing with no rule.
    assert engine.format_number(10**18).text == "1,000,000,000,000,000,000"
