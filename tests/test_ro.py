from unicode_rbnf import RbnfEngine


def test_romanian():
    engine = RbnfEngine.for_language("ro")
    assert engine.format_number(-100).text == "minus una sută"
