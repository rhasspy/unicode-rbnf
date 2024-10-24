from unicode_rbnf import RbnfEngine


def test_german():
    engine = RbnfEngine.for_language("de")
    assert engine.format_number(13).text == "dreizehn"
    assert engine.format_number(32).text == "zweiunddreißig"

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
