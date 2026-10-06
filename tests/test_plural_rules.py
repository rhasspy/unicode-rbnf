from decimal import Decimal

from unicode_rbnf.plural_rules import PluralType, get_plural_category


def test_slovak_few_is_the_whole_integer():
    # Slovak "few" is i = 2..4, so it does not reach into the tens.
    assert get_plural_category("sk", 1) == "one"
    assert get_plural_category("sk", 2) == "few"
    assert get_plural_category("sk", 4) == "few"
    assert get_plural_category("sk", 5) == "other"
    assert get_plural_category("sk", 12) == "other"
    assert get_plural_category("sk", 22) == "other"
    assert get_plural_category("sk", 683) == "other"


def test_russian_looks_at_final_digits():
    assert get_plural_category("ru", 1) == "one"
    assert get_plural_category("ru", 2) == "few"
    assert get_plural_category("ru", 5) == "many"

    # The teens are "many" even though they end in 1-4.
    assert get_plural_category("ru", 11) == "many"
    assert get_plural_category("ru", 12) == "many"
    assert get_plural_category("ru", 14) == "many"
    assert get_plural_category("ru", 111) == "many"

    # Past the teens the final digit decides again.
    assert get_plural_category("ru", 21) == "one"
    assert get_plural_category("ru", 22) == "few"
    assert get_plural_category("ru", 25) == "many"


def test_polish_differs_from_russian():
    # Polish puts 12 in "many" and 22 in "few", like Russian, but 1000 and
    # every other i != 1 ending in 0-1 is "many" rather than "one".
    assert get_plural_category("pl", 1) == "one"
    assert get_plural_category("pl", 2) == "few"
    assert get_plural_category("pl", 12) == "many"
    assert get_plural_category("pl", 22) == "few"
    assert get_plural_category("pl", 112) == "many"


def test_two_category_languages():
    for language in ("en", "de", "sv", "bg", "lb"):
        assert get_plural_category(language, 1) == "one"
        assert get_plural_category(language, 2) == "other"


def test_portuguese_counts_zero_as_one():
    assert get_plural_category("pt", 0) == "one"
    assert get_plural_category("pt", 1) == "one"
    assert get_plural_category("pt", 2) == "other"


def test_region_falls_back_to_language():
    # pt_PT has its own rules; en_IN has none and falls back to en.
    assert get_plural_category("pt_PT", 1) == "one"
    assert get_plural_category("en_IN", 1) == "one"
    assert get_plural_category("en_IN", 2) == "other"


def test_unknown_language_is_other():
    assert get_plural_category("zz", 1) == "other"


def test_fractions():
    # Visible fraction digits put Slovak in "many" and English in "other".
    assert get_plural_category("sk", Decimal("1.5")) == "many"
    assert get_plural_category("en", Decimal("1.0")) == "other"
    assert get_plural_category("en", 1) == "one"


def test_ordinal_rules_are_separate():
    # English ordinals: 1st, 2nd, 3rd, 4th -- and 11th/12th/13th.
    assert get_plural_category("en", 1, PluralType.ORDINAL) == "one"
    assert get_plural_category("en", 2, PluralType.ORDINAL) == "two"
    assert get_plural_category("en", 3, PluralType.ORDINAL) == "few"
    assert get_plural_category("en", 4, PluralType.ORDINAL) == "other"
    assert get_plural_category("en", 11, PluralType.ORDINAL) == "other"
    assert get_plural_category("en", 12, PluralType.ORDINAL) == "other"
    assert get_plural_category("en", 21, PluralType.ORDINAL) == "one"

    # Cardinal English has no "two" category at all.
    assert get_plural_category("en", 2, PluralType.CARDINAL) == "other"
