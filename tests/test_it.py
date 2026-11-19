from unicode_rbnf import FormatPurpose, RbnfEngine


def test_italian_ordinal_thousands():
    # Italian's ordinal thousands rule is keyed 2001 ("<< mila <<"). Its divisor
    # must be 1000, so the quotient of a five- or six-digit number is its real
    # thousands count. A wrong 10000 divisor dropped a digit and then repeated
    # "mila", e.g. 99999 -> "...nove mila nove mila..." instead of "novanta nove
    # mila...". These expected strings match ICU's %spellout-ordinal-masculine.
    engine = RbnfEngine.for_language("it")

    def ordinal(number: int) -> str:
        return engine.format_number(
            number,
            purpose=FormatPurpose.ORDINAL,
            ruleset_names=["spellout-ordinal-masculine"],
        ).text

    assert ordinal(99999) == "novantanovemilanovecentonovantanovesimo"
    assert (
        ordinal(123456789)
        == "centoventitrémilionequattrocentocinquantaseimilasettecentoottantanovesimo"
    )
    assert (
        ordinal(999999999)
        == "novecentonovantanovemilionenovecentonovantanovemilanovecentonovantanovesimo"
    )
