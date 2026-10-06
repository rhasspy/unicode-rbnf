from unicode_rbnf import RbnfEngine


def test_romanian():
    engine = RbnfEngine.for_language("ro")
    assert engine.format_number(-100).text == "minus o sută"


def test_romanian_millions_use_the_article():
    engine = RbnfEngine.for_language("ro")

    # "un milion", not the standalone numeral "unu".
    assert engine.format_number(1000000).text == "un milion"
    assert engine.format_number(1000000000).text == "un miliard"

    assert engine.format_number(2000000).text == "două milioane"
    assert engine.format_number(5000000).text == "cinci milioane"
