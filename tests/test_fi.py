from unicode_rbnf import RbnfEngine


def test_finnish():
    engine = RbnfEngine.for_language("fi")
    assert engine.format_number(25).text == "kaksikymmentäviisi"
