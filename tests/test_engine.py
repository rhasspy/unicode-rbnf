from unicode_rbnf.engine import (
    RbnfRule,
    TextRulePart,
    SubRulePart,
    SubType,
    RbnfEngine,
    FormatResult,
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
