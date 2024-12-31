from unicode_rbnf import RbnfEngine


def test_german():
    engine = RbnfEngine.for_language("de")
    assert engine.format_number(1).text == "eins"
    assert engine.format_number(2).text == "zwei"
    assert engine.format_number(3).text == "drei"
    assert engine.format_number(4).text == "vier"
    assert engine.format_number(5).text == "fünf"
    assert engine.format_number(6).text == "sechs"
    assert engine.format_number(7).text == "sieben"
    assert engine.format_number(8).text == "acht"
    assert engine.format_number(9).text == "neun"
    assert engine.format_number(10).text == "zehn"
    assert engine.format_number(11).text == "elf"
    assert engine.format_number(12).text == "zwölf"
    assert engine.format_number(13).text == "dreizehn"
    assert engine.format_number(14).text == "vierzehn"
    assert engine.format_number(15).text == "fünfzehn"
    assert engine.format_number(16).text == "sechzehn"
    assert engine.format_number(17).text == "siebzehn"
    assert engine.format_number(18).text == "achtzehn"
    assert engine.format_number(19).text == "neunzehn"
    assert engine.format_number(20).text == "zwanzig"
    assert engine.format_number(21).text == "einundzwanzig"
    assert engine.format_number(22).text == "zweiundzwanzig"
    assert engine.format_number(23).text == "dreiundzwanzig"
    assert engine.format_number(24).text == "vierundzwanzig"
    assert engine.format_number(25).text == "fünfundzwanzig"
    assert engine.format_number(26).text == "sechsundzwanzig"
    assert engine.format_number(27).text == "siebenundzwanzig"
    assert engine.format_number(28).text == "achtundzwanzig"
    assert engine.format_number(29).text == "neunundzwanzig"
    assert engine.format_number(30).text == "dreißig"
    assert engine.format_number(32).text == "zweiunddreißig"
    assert engine.format_number(100).text == "einhundert"
    assert engine.format_number(101).text == "einhunderteins"
    assert engine.format_number(120).text == "einhundertzwanzig"
    assert engine.format_number(121).text == "einhunderteinundzwanzig"
    assert engine.format_number(200).text == "zweihundert"
    assert engine.format_number(1000).text == "eintausend"
    assert engine.format_number(1001).text == "eintausendeins"
    assert engine.format_number(1100).text == "eintausendeinhundert"
    assert engine.format_number(1234).text == "eintausendzweihundertvierunddreißig"

    # All genders, cases
    assert set(engine.format_number(1).text_by_ruleset.values()) == {
        "ein",
        "eins",
        "eine",
        "eines",
        "einer",
        "einem",
        "einen",
    }
