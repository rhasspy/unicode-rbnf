from unicode_rbnf import RbnfEngine, FormatPurpose


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
    assert engine.format_number(float("nan")).text == "not a number"
    assert engine.format_number(float("inf")).text == "infinite"

    # Fractions
    assert engine.format_number(3.14).text == "three point fourteen"
    assert engine.format_number("5.3").text == "five point three"

    # Ordinals
    assert engine.format_number(20, FormatPurpose.ORDINAL).text == "twentieth"
    assert engine.format_number(30, FormatPurpose.ORDINAL).text == "thirtieth"
    assert engine.format_number(99, FormatPurpose.ORDINAL).text == "ninety-ninth"
    assert engine.format_number(11, FormatPurpose.ORDINAL).text == "eleventh"

    # Years
    assert engine.format_number(1999, FormatPurpose.YEAR).text == "nineteen ninety-nine"
