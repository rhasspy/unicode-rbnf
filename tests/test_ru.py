from unicode_rbnf import RbnfEngine


def test_russian_thousands_agreement():
    engine = RbnfEngine.for_language("ru")

    assert engine.format_number(1000).text == "одна тысяча"
    assert engine.format_number(2000).text == "две тысячи"
    assert engine.format_number(5000).text == "пять тысяч"

    # The teens take the "many" form even though they end in 1-4.
    assert engine.format_number(11000).text == "одиннадцать тысяч"
    assert engine.format_number(12000).text == "двенадцать тысяч"
    assert engine.format_number(13000).text == "тринадцать тысяч"
    assert engine.format_number(111000).text == "сто одиннадцать тысяч"
    assert engine.format_number(112000).text == "сто двенадцать тысяч"

    # Past the teens the final digit decides again.
    assert engine.format_number(21000).text == "двадцать одна тысяча"
    assert engine.format_number(22000).text == "двадцать две тысячи"
    assert engine.format_number(25000).text == "двадцать пять тысяч"


def test_russian_millions_agreement():
    engine = RbnfEngine.for_language("ru")

    assert engine.format_number(1000000).text == "один миллион"
    assert engine.format_number(2000000).text == "два миллиона"
    assert engine.format_number(5000000).text == "пять миллионов"
