from unicode_rbnf import RbnfEngine


def test_german():
    engine = RbnfEngine.for_language("es")
    assert engine.format_number(5).text == "cinco"
    assert engine.format_number(2).text == "dos"
    assert engine.format_number(5.2).text == "cinco coma dos"

    # All genders
    assert set(engine.format_number(1).text_by_ruleset.values()) == {
        "un",
        "uno",
        "una",
    }
