from unicode_rbnf import RbnfEngine


def test_czech():
    engine = RbnfEngine.for_language("cs")

    assert engine.format_number(7).text == "sedm"
    assert engine.format_number(15).text == "patnáct"

    assert engine.format_number(100).text == "sto"
    assert engine.format_number(150).text == "sto padesát"
    assert engine.format_number(200).text == "dvě stě"
    assert engine.format_number(300).text == "tři sta"
    assert engine.format_number(500).text == "pět set"

    # A multiplier of one is not spoken: "tisíc", never "jedna tisíc".
    assert engine.format_number(1000).text == "tisíc"
    assert engine.format_number(1100).text == "tisíc sto"
    assert engine.format_number(1234).text == "tisíc dvě stě třicet čtyři"

    assert engine.format_number(5000).text == "pět tisíc"
    assert engine.format_number(12000).text == "dvanáct tisíc"
