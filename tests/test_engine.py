import pytest

from unicode_rbnf.engine import (
    FormatResult,
    NoRuleForNumberError,
    RbnfEngine,
    RbnfRule,
    SubRulePart,
    SubType,
    TextRulePart,
)


def test_parse_text():
    assert RbnfRule.parse(1, "one;") == RbnfRule(1, parts=[TextRulePart("one")])


def test_parse_sub():
    assert RbnfRule.parse(100, "←← hundred[ →→];") == RbnfRule(
        100,
        parts=[
            SubRulePart(SubType.QUOTIENT),
            TextRulePart(" hundred"),
            SubRulePart(SubType.REMAINDER, is_optional=True, text_before=" "),
        ],
    )


def test_parse_ruleset_name():
    assert RbnfRule.parse(
        100, "←%spellout-cardinal-masculine←­hundert[­→→];"
    ) == RbnfRule(
        100,
        parts=[
            SubRulePart(SubType.QUOTIENT, ruleset_name="spellout-cardinal-masculine"),
            TextRulePart("­hundert"),
            SubRulePart(SubType.REMAINDER, is_optional=True, text_before="­"),
        ],
    )


def test_find_rule():
    engine = RbnfEngine("en")
    engine.add_rule(2, "two;", "spellout-numbering")
    engine.add_rule(20, "twenty[-→→];", "spellout-numbering")
    engine.add_rule(100, "←← hundred[ →→];", "spellout-numbering")

    ruleset = engine.rulesets["spellout-numbering"]

    rule_2 = ruleset.find_rule(2)
    assert rule_2 is not None
    assert rule_2.value == 2

    rule_20 = ruleset.find_rule(25)
    assert rule_20 is not None
    assert rule_20.value == 20

    rule_100 = ruleset.find_rule(222)
    assert rule_100 is not None
    assert rule_100.value == 100


def test_format_number():
    engine = RbnfEngine("en")
    engine.add_rule(2, "two;", "spellout-cardinal")
    engine.add_rule(20, "twenty[-→→];", "spellout-cardinal")
    engine.add_rule(100, "←← hundred[ →→];", "spellout-cardinal")

    assert engine.format_number(222) == FormatResult(
        text="two hundred twenty-two",
        text_ruleset="spellout-cardinal",
        text_by_ruleset={"spellout-cardinal": "two hundred twenty-two"},
    )


def test_zero_rules():
    engine = RbnfEngine("en")
    engine.add_rule(0, "abc=%ruleset_2=def;", "ruleset_1")
    engine.add_rule(0, " efg=%ruleset_3= hij;", "ruleset_2")
    engine.add_rule(1, "one;", "ruleset_3")

    assert (
        engine.format_number(1, ruleset_names=["ruleset_1"]).text == "abc efgone hijdef"
    )


def test_no_rules_for_number():
    engine = RbnfEngine("en")

    with pytest.raises(NoRuleForNumberError):
        engine.format_number(1, ruleset_names=["does_not_exist"])


def test_parse_remainder_whitespace():
    assert RbnfRule.parse(12.34, "←← x →→→;") == RbnfRule(
        12,
        parts=[
            SubRulePart(SubType.QUOTIENT),
            TextRulePart(" x"),
            SubRulePart(SubType.REMAINDER, text_before=" "),
        ],
    )


def test_replace_with_decimal_format_pattern():
    # =#,##0= emits the number through a DecimalFormat pattern, not a ruleset.
    # CLDR uses this as a fallback once a language runs out of words and for
    # digit-based ordinals (e.g. Hindi "7" -> "7वाँ"). The pattern must not be
    # looked up as a (non-existent) ruleset.
    engine = RbnfEngine("en")
    engine.add_rule(0, "=#,##0=th;", "digits-ordinal")

    assert engine.format_number(7, ruleset_names=["digits-ordinal"]).text == "7th"
    assert (
        engine.format_number(1234567, ruleset_names=["digits-ordinal"]).text
        == "1,234,567th"
    )


def test_replace_with_indian_grouping_pattern():
    # Hindi digits-ordinal uses =#,##,##0=, which groups lakh/crore style.
    engine = RbnfEngine.for_language("hi")
    assert (
        engine.format_number(1234567, ruleset_names=["digits-ordinal-masculine"]).text
        == "12,34,567वाँ"
    )


def test_divisor_uses_highest_power_not_leading_digit():
    # A rule whose base value has a non-zero digit after the first (e.g. 2001,
    # the "<< thousand >>" rule many languages use for 2000-2999) must still
    # divide on the power of the radix below it -- 1000 here, not 10000. ICU
    # derives the divisor as the highest radix power <= the rule's base value
    # (NFRule::expectedExponent). Deriving it from a "leading digit forced to 1"
    # proxy turned 2001 into 1001, whose ceil(log10) is 4, so 99999 divided by
    # 10000 and its quotient became 9 ("nine thousand") instead of 99.
    engine = RbnfEngine("en")
    for value, text in [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ]:
        engine.add_rule(value, f"{text};", "r")

    engine.add_rule(10, "←←ty[-→→];", "r")
    engine.add_rule(100, "←← hundred[ →→];", "r")
    engine.add_rule(1000, "thousand[ →→];", "r")
    engine.add_rule(2000, "←← thousand[ →→];", "r")
    engine.add_rule(2001, "←← thousand[ →→];", "r")

    # 99999 lands on the 2001 rule; the quotient must be 99, not 9.
    assert (
        engine.format_number(99999, ruleset_names=["r"]).text
        == "ninety-nine thousand nine hundred ninety-nine"
    )


def test_divisor_does_not_mutate_cached_rule():
    # The divisor was computed by writing a normalized value back onto the
    # shared rule object (rule.value = int("1" + ...)). The rule is parsed once
    # and cached, so formatting one number corrupted the value seen by the next.
    engine = RbnfEngine("en")
    for value, text in [(0, "zero"), (1, "one"), (2, "two"), (3, "three")]:
        engine.add_rule(value, f"{text};", "r")
    engine.add_rule(100, "←← hundred[ →→];", "r")
    rule_300 = engine.add_rule(300, "←← hundred[ →→];", "r")
    assert rule_300 is not None

    engine.format_number(321, ruleset_names=["r"])
    # Formatting must not have rewritten the rule's own base value.
    assert rule_300.value == 300


def test_invalid_radix_is_rejected():
    # The divisor loop needs radix >= 2; a smaller radix would never terminate.
    engine = RbnfEngine("en")
    for radix in (0, 1, -10):
        with pytest.raises(ValueError):
            engine.add_rule("100", "hundred;", "r", radix=radix)
