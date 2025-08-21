from unicode_rbnf import FormatPurpose, RbnfEngine


def test_polish():
    engine = RbnfEngine.for_language("pl")

    assert engine.format_number(7).text == "siedem"
    assert engine.format_number(15).text == "piętnaście"
    assert engine.format_number(42).text == "czterdzieści dwa"
    assert engine.format_number(100).text == "sto"
    assert engine.format_number(143).text == "sto czterdzieści trzy"
    assert engine.format_number(1000).text == "tysiąc"
    assert engine.format_number(1234).text == "tysiąc dwieście trzydzieści cztery"
    assert engine.format_number(3144).text == "trzy tysiące sto czterdzieści cztery"
    assert engine.format_number(10000).text == "dziesięć tysięcy"
    assert (
        engine.format_number(83145).text
        == "osiemdziesiąt trzy tysiące sto czterdzieści pięć"
    )

    assert engine.format_number(100000).text == "sto tysięcy"
    assert (
        engine.format_number(683146).text
        == "sześćset osiemdziesiąt trzy tysiące sto czterdzieści sześć"
    )

    assert engine.format_number(1000000).text == "milion"
    assert engine.format_number(10000000).text == "dziesięć milionów"
    assert engine.format_number(100000000).text == "sto milionów"
    assert engine.format_number(1000000000).text == "miliard"

    # Special rules
    assert engine.format_number(-1).text == "minus jeden"
    assert engine.format_number(-14).text == "minus czternaście"
    # assert engine.format_number(-14.6).text == "minus czternaście przecinek sześć"
    # assert engine.format_number(-14.89).text == "minus czternaście przecinek osiemdziesiąt dziewięć"

    # assert engine.format_number(float("nan")).text == "nie jest liczbą"
    # assert engine.format_number(float("inf")).text == "nieskończona"

    # Fractions
    # assert engine.format_number(3.14).text == "trzy przecinek czternaście"
    # assert engine.format_number("5.3").text == "pięć przecinek trzy"

    # Years
    assert (
        engine.format_number(1999, FormatPurpose.YEAR).text
        == "tysiąc dziewięćset dziewięćdziesiąt dziewięć"
    )
