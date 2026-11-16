from unicode_rbnf import FormatPurpose, RbnfEngine


def test_arabic_whitespace():
    """Rules joined at their edges must not leave extra spaces."""
    engine = RbnfEngine.for_language("ar")

    assert (
        engine.format_number(21, purpose=FormatPurpose.ORDINAL).text_by_ruleset[
            "spellout-ordinal-masculine"
        ]
        == "الحادي والعشرون"
    )
    assert (
        engine.format_number(1.5, ruleset_names=["spellout-cardinal-masculine"]).text
        == "واحد فاصل خمسة"
    )
