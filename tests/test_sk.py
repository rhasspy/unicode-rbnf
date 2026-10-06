from unicode_rbnf import RbnfEngine


def test_slovak():
    engine = RbnfEngine.for_language("sk")

    assert engine.format_number(7).text == "sedem"
    assert engine.format_number(15).text == "pätnásť"
    assert engine.format_number(42).text == "štyridsaťdva"

    # A multiplier of one is not spoken: "sto", never "jednasto".
    assert engine.format_number(100).text == "sto"
    assert engine.format_number(101).text == "sto jeden"
    assert engine.format_number(150).text == "sto päťdesiat"
    assert engine.format_number(199).text == "sto deväťdesiatdeväť"

    # From two hundred up, the multiplier joins the word.
    assert engine.format_number(200).text == "dvesto"
    assert engine.format_number(300).text == "tristo"
    assert engine.format_number(500).text == "päťsto"
    assert engine.format_number(999).text == "deväťsto deväťdesiatdeväť"

    # Likewise "tisíc", never "jedna tisíc".
    assert engine.format_number(1000).text == "tisíc"
    assert engine.format_number(1100).text == "tisíc sto"
    assert engine.format_number(1234).text == "tisíc dvesto tridsaťštyri"

    # Slovak agreement on "tisíc": 2-4 take the plural "tisíce", 5 and above
    # take the counted form "tisíc". The category follows the whole multiplier,
    # so 12 and 22 take "tisíc" even though they end in 2.
    assert engine.format_number(2000).text == "dve tisíce"
    assert engine.format_number(3000).text == "tri tisíce"
    assert engine.format_number(5000).text == "päť tisíc"
    assert engine.format_number(12000).text == "dvanásť tisíc"
    assert engine.format_number(22000).text == "dvadsaťdve tisíc"

    assert engine.format_number(100000).text == "sto tisíc"
    assert (
        engine.format_number(683146).text
        == "šesťsto osemdesiattri tisíc sto štyridsaťšesť"
    )
