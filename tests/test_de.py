from unicode_rbnf import RbnfEngine


def test_german():
    engine = RbnfEngine.for_language("de")
    assert engine.format_number(13) == "dreizehn"
    assert engine.format_number(32) == "zweiunddreißig"
