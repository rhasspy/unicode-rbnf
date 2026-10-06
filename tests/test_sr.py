from unicode_rbnf import RbnfEngine


def test_serbian_cyrillic():
    engine = RbnfEngine.for_language("sr")

    # A multiplier of one is not spoken.
    assert engine.format_number(1000).text == "хиљаду"
    assert engine.format_number(1100).text == "хиљаду сто"
    assert engine.format_number(1000000).text == "милион"
    assert engine.format_number(1000000000).text == "милијарду"

    # The counted noun agrees with the multiplier.
    assert engine.format_number(2000).text == "две хиљаде"
    assert engine.format_number(5000).text == "пет хиљада"
    assert engine.format_number(2000000).text == "два милиона"
    assert engine.format_number(5000000).text == "пет милиона"
    assert engine.format_number(2000000000).text == "две милијарде"
    assert engine.format_number(5000000000).text == "пет милијарди"


def test_serbian_latin():
    engine = RbnfEngine.for_language("sr_Latn")

    assert engine.format_number(1000).text == "hiljadu"
    assert engine.format_number(1000000).text == "milion"
    assert engine.format_number(1000000000).text == "milijardu"

    assert engine.format_number(2000).text == "dve hiljade"
    assert engine.format_number(2000000).text == "dva miliona"
    assert engine.format_number(5000000000).text == "pet milijardi"
