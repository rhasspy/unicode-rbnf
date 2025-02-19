from unicode_rbnf import RbnfEngine, FormatPurpose


def test_polish():
    engine = RbnfEngine.for_language("pl")

    assert engine.format_number(7).text == "siedem"
    assert engine.format_number(15).text == "piętnaście"
    assert engine.format_number(42).text == "czterdzieści dwa"
    assert engine.format_number(100).text == "sto"
    assert engine.format_number(143).text == "sto czterdzieści trzy"
    assert engine.format_number(1000).text == "tysiąc"
    assert engine.format_number(1234).text == "tysiąc dwieście trzydzieści cztery"
    # assert engine.format_number(3144).text == "trzy tysiące sto czterdzieści cztery"
    # assert engine.format_number(10000).text == "dziesięć tysięcy"
    # assert (
    #     engine.format_number(83145).text
    #     == "osiemdziesiąt trzy tysiące sto czterdzieści pięć"
    # )

    # assert engine.format_number(100000).text == "sto tysięcy"
    # assert (
    #     engine.format_number(683146).text
    #     == "sześćset osiemdziesiąt trzy tysiące sto czterdzieści sześć"
    # )

    assert engine.format_number(1000000).text == "milion"
    # assert engine.format_number(10000000).text == "dziesięć milionów"
    # assert engine.format_number(100000000).text == "sto milionów"
    assert engine.format_number(1000000000).text == "miliard"

    # Special rules
    assert engine.format_number(-1).text == "minus jeden"
    assert engine.format_number(-14).text == "minus czternaście"
    # assert engine.format_number(-14.6).text == "minus czternaście przecinek sześć"
    # assert engine.format_number(float("nan")).text == "nie jest liczbą"
    # assert engine.format_number(float("inf")).text == "nieskończona"

    # Fractions
    # assert engine.format_number(3.14).text == "trzy przecinek czternaście"
    # assert engine.format_number("5.3").text == "pięć przecinek trzy"

    # Dates
    # assert engine.format_number("01.01.2025", FormatPurpose.ORDINAL).text == "pierwszego stycznia dwa tysiące dwadzieścia piątego"
    # assert engine.format_number("01.01.2025").text == "pierwszy stycznia dwa tysiące dwadzieścia pięć"
    # assert engine.format_number("13.05.1998", FormatPurpose.ORDINAL).text == "trzynastego maja tysiąc dziewięćset dziewięćdziesiątego ósmego"
    # assert engine.format_number("13.05.1998").text == "trzynasty maja tysiąc dziewięćset dziewięćdziesiąty ósmy"
    # assert engine.format_number("01.12.1987", FormatPurpose.ORDINAL).text == "pierwszego grudnia tysiąc dziewięćset osiemdziesiątego siódmego"
    # assert engine.format_number("01.12.1987").text == "pierwszy grudnia tysiąc dziewięćset osiemdziesiąty siódmy"

    # Hours
    # assert engine.format_number("11:12").text == "jedenasta dwunasta"
    # assert engine.format_number("15:30").text == "piętnasta trzydzieści"
    # assert engine.format_number("00:00").text == "zero zero"
    # assert engine.format_number("01:23").text == "pierwsza dwadzieścia trzy"
    # assert engine.format_number("08:45").text == "ósma czterdzieści pięć"
    # assert engine.format_number("11:01").text == "jedenasta zero jeden"
    # assert engine.format_number("18:09").text == "osiemnasta zero dziewięć"

    # Currency
    # assert engine.format_number("100 zł").text == "sto złotych"
    # assert engine.format_number("100 €").text == "sto euro"
    # assert engine.format_number("100").text == "sto euro"
    # assert engine.format_number("$100").text == "sto dolarów"
    # assert engine.format_number("177 zł").text == "sto siedemdziesiąt siedem złotych"
    # assert engine.format_number("177 €").text == "sto siedemdziesiąt siedem euro"
    # assert engine.format_number("$177").text == "sto siedemdziesiąt siedem dolarów"
    # assert engine.format_number("1239 zł").text == "tysiąc dwieście trzydzieści dziewięć złotych"
    # assert engine.format_number("1239 €").text == "tysiąc dwieście trzydzieści dziewięć euro"
    # assert engine.format_number("$1239").text == "tysiąc dwieście trzydzieści dziewięć dolarów"

    # Units
    # assert engine.format_number("100 km").text == "sto kilometrów"
    # assert engine.format_number("100 m").text == "sto metrów"
    # assert engine.format_number("100 cm").text == "sto centymetrów"
    # assert engine.format_number("100 mm").text == "sto milimetrów"
    # assert engine.format_number("100 kg").text == "sto kilogramów"
    # assert engine.format_number("100 g").text == "sto gramów"
    # assert engine.format_number("100 dag").text == "sto dekagramów"
    # assert engine.format_number("100 mg").text == "sto miligramów"
    # assert engine.format_number("100 l").text == "sto litrów"
    # assert engine.format_number("100 ml").text == "sto mililitrów"
    # assert engine.format_number("100 m²").text == "sto metrów kwadratowych"
    # assert engine.format_number("100 m³").text == "sto metrów sześciennych"
    # assert engine.format_number("100 km/h").text == "sto kilometrów na godzinę"
    # assert engine.format_number("100 m/s").text == "sto metrów na sekundę"
    # assert engine.format_number("100 °C").text == "sto stopni Celsjusza"
    # assert engine.format_number("100 °F").text == "sto stopni Fahrenheita"
    # assert engine.format_number("100 K").text == "sto kelwinów"
    # assert engine.format_number("100 °").text == "sto stopni"
    # assert engine.format_number("100 %").text == "sto procent"
    # assert engine.format_number("100 ‰").text == "sto promili"

    # Ordinals
    # assert engine.format_number(20, FormatPurpose.ORDINAL).text == "dwudziesty"
    # assert engine.format_number(30, FormatPurpose.ORDINAL).text == "trzydziesty"
    # assert engine.format_number(99, FormatPurpose.ORDINAL).text == "dziewięćdziesiąty dziewiąty"
    # assert engine.format_number(11, FormatPurpose.ORDINAL).text == "jedenasty"

    # Years
    assert engine.format_number(1999, FormatPurpose.YEAR).text == "tysiąc dziewięćset dziewięćdziesiąt dziewięć"
