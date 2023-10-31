from unicode_rbnf import RbnfEngine, RulesetName


def test_french():
    engine = RbnfEngine.for_language("fr")
    assert engine.format_number(88) == "quatre-vingt-huit"
