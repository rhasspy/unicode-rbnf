from unicode_rbnf import RbnfEngine


def test_kazakh_fractions():
    engine = RbnfEngine.for_language("kk")

    assert engine.format_number(1.5).text == "бір бүтін оннан бес"
    assert engine.format_number(14.89).text == "он төрт бүтін жүзден сексен тоғыз"
