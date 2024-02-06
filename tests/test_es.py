from unicode_rbnf import RbnfEngine


def test_german():
    engine = RbnfEngine.for_language("es")
    assert engine.format_number(5) == "cinco"
    assert engine.format_number(2) == "dos"
    assert engine.format_number(5.2) == "cinco coma dos"
