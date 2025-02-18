from unicode_rbnf import RbnfEngine


def test_slovenian():
    engine = RbnfEngine.for_language("sl")
    assert engine.format_number(2000).text == "dva tisoč"
