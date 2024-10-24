from unicode_rbnf import RbnfEngine


def test_french():
    engine = RbnfEngine.for_language("fr")
    assert engine.format_number(88).text == "quatre-vingt-huit"

    # All genders
    assert set(engine.format_number(1).text_by_ruleset.values()) == {
        "un",
        "une",
    }
