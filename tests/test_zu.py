from unicode_rbnf import RbnfEngine, FormatPurpose


def test_zulu():
    engine = RbnfEngine.for_language("zu")

    assert engine.format_number(3).text == "kuthathu"
    assert engine.format_number(15).text == "ishumi nanhlanu"
    assert engine.format_number(21).text == "amashumi amabili nanye"
    assert engine.format_number(47).text == "amashumi amane nesikhombisa"
    assert engine.format_number(123).text == "ikhulu namashumi amabili nantathu"
    assert (
        engine.format_number(999).text
        == "amakhulu ayisishiyagalolunye namashumi ayisishiyagalolunye nesishiyagalolunye"
    )
    assert engine.format_number(4000).text == "izinkulungwane ezine"
    assert (
        engine.format_number(8192).text
        == "izinkulungwane eziyisishiyagalombili nekhulu namashumi ayisishiyagalolunye nambili"
    )

    assert (
        engine.format_number(15123).text
        == "izinkulungwane eziyishumi nanhlanu nekhulu namashumi amabili nantathu"
    )

    # # 3.5 million
    # assert (
    #     engine.format_number(3500000).text
    #     == "izigidi ezintathu namakhulu ayishihlanu ezinkulungwane"
    # )

    # # 12 million
    # assert engine.format_number(12000000).text == "izigidi eziyishumi ezimbili"
