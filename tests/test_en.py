from unicode_rbnf import RbnfEngine


def test_english():
    engine = RbnfEngine.for_language("en")
    assert engine.format_number(7) == "seven"
    assert engine.format_number(15) == "fifteen"
    assert engine.format_number(42) == "forty-two"
    assert engine.format_number(100) == "one hundred"
    assert engine.format_number(143) == "one hundred forty-three"
    assert engine.format_number(1000) == "one thousand"
    assert engine.format_number(3144) == "three thousand one hundred forty-four"
    assert engine.format_number(10000) == "ten thousand"
    assert engine.format_number(83145) == "eighty-three thousand one hundred forty-five"
    assert engine.format_number(100000) == "one hundred thousand"
    assert (
        engine.format_number(683146)
        == "six hundred eighty-three thousand one hundred forty-six"
    )
    assert engine.format_number(1000000) == "one million"
    assert engine.format_number(10000000) == "ten million"
    assert engine.format_number(100000000) == "one hundred million"
    assert engine.format_number(1000000000) == "one billion"
