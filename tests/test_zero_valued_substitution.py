from unicode_rbnf import RbnfEngine


def test_irish_zero_valued_quotient_emits_scale_word():
    """A bare required substitution of 0 recurses into rule 0 ("míle")."""
    engine = RbnfEngine.for_language("ga")

    # 20000 = 20 * 1000 + 0; the thousands rule has an exact rule for 0,
    # so ICU speaks the scale word "míle" instead of dropping it.
    assert engine.format_number(20000).text == "fiche míle"


def test_lithuanian_zero_valued_substitution_emits_scale_word():
    """Lithuanian thousands keep "tūkstančių" when the remainder is zero."""
    engine = RbnfEngine.for_language("lt")

    assert engine.format_number(100000).text == "šimtas tūkstančių"
    assert engine.format_number(100001).text == "šimtas tūkstančių vienas"


def test_english_no_spurious_zero_word():
    """Trailing-zero numbers must not gain a spurious zero-word.

    English rulesets have no exact rule 0 at these scales, so the bare
    required zero substitution is still dropped (unchanged behavior).
    """
    engine = RbnfEngine.for_language("en")

    assert engine.format_number(20).text == "twenty"
    assert engine.format_number(1000).text == "one thousand"
    assert engine.format_number(100).text == "one hundred"
