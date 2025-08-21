from unicode_rbnf import RbnfEngine


def test_korean():
    engine = RbnfEngine.for_language("ko")

    assert engine.format_number(20.03).text == "이십점영삼"
    assert engine.format_number(20.0123).text == "이십점영일이삼"
