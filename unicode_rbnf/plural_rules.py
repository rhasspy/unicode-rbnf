"""CLDR plural rules.

RBNF rules select a word form with ``$(cardinal,one{...}few{...}other{...})$``,
and which form applies is a property of the language, not of the last digit.
Slovak puts 12 in ``other`` because its ``few`` is the whole integer 2-4, while
Polish puts 12 in ``many`` and 22 in ``few`` because its categories look at the
final digits. There is no shared shortcut, so the categories come from CLDR's
own rules, parsed from the supplemental data vendored beside this module.

The rule syntax is small (TR35, "Language Plural Rules")::

    condition     = and_condition ('or' and_condition)*
    and_condition = relation ('and' relation)*
    relation      = expr ('=' | '!=') range_list
    expr          = operand ('%' value)?
    range_list    = (range | value) (',' range_list)*
    range         = value '..' value

Only the sample clauses that follow ``@integer`` / ``@decimal`` are discarded;
everything before them is evaluated.
"""

import re
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Union
from xml.etree import ElementTree as et

_DIR = Path(__file__).parent

# Order matters: CLDR evaluates these in sequence and the first match wins.
_CATEGORY_ORDER = ("zero", "one", "two", "few", "many")
OTHER = "other"


class PluralType(str, Enum):
    """Which set of CLDR rules to consult."""

    CARDINAL = "cardinal"
    """Counting forms: one apple, two apples."""

    ORDINAL = "ordinal"
    """Position forms: 1st, 2nd, 3rd."""


_FILES = {PluralType.CARDINAL: "plurals.xml", PluralType.ORDINAL: "ordinals.xml"}

# locale -> [(category, condition)], parsed lazily and kept.
_RULES: Dict[PluralType, Dict[str, List[Tuple[str, str]]]] = {}


def _operands(number: Union[int, float, Decimal]) -> Dict[str, Decimal]:
    """CLDR plural operands for a number.

    n: absolute value. i: integer digits. v/w: count of visible fraction
    digits with/without trailing zeros. f/t: those digits as an integer.
    """
    if isinstance(number, Decimal):
        decimal_number = number
    else:
        # str() first: Decimal(0.1) is not Decimal("0.1").
        decimal_number = Decimal(str(number))

    n = abs(decimal_number)
    i = int(n)

    frac = ""
    exponent = n.as_tuple().exponent
    if isinstance(exponent, int) and (exponent < 0):
        text = str(n)
        if "." in text:
            frac = text.split(".", maxsplit=1)[1]

    frac_stripped = frac.rstrip("0")
    return {
        "n": n,
        "i": Decimal(i),
        "v": Decimal(len(frac)),
        "w": Decimal(len(frac_stripped)),
        "f": Decimal(int(frac)) if frac else Decimal(0),
        "t": Decimal(int(frac_stripped)) if frac_stripped else Decimal(0),
        # Compact decimal exponent: always zero here, since RBNF never
        # formats compact notation.
        "c": Decimal(0),
        "e": Decimal(0),
    }


def _in_range_list(value: Decimal, range_list: str) -> bool:
    """Whether a value falls in a CLDR range list like ``2..4,7``.

    A range only ever matches an integer: CLDR says 2.5 is not "in" 2..4.
    """
    for part in range_list.split(","):
        part = part.strip()
        if ".." in part:
            low_str, high_str = part.split("..", maxsplit=1)
            low, high = int(low_str), int(high_str)
            if int(value) == value and low <= int(value) <= high:
                return True
        elif value == Decimal(part):
            return True

    return False


def _eval_relation(relation: str, operands: Dict[str, Decimal]) -> bool:
    """Evaluate a single ``expr = range_list`` or ``expr != range_list``."""
    match = re.match(r"^\s*(\w+)\s*(?:%\s*(\d+)\s*)?(!=|=)\s*(.+?)\s*$", relation)
    if match is None:
        raise ValueError(f"Cannot parse plural relation: {relation!r}")

    operand_name, modulus, operator, range_list = match.groups()
    value = operands[operand_name]
    if modulus is not None:
        value = value % int(modulus)

    result = _in_range_list(value, range_list)
    return result if operator == "=" else not result


def _eval_condition(condition: str, operands: Dict[str, Decimal]) -> bool:
    """Evaluate a full condition. ``and`` binds tighter than ``or``."""
    return any(
        all(_eval_relation(relation, operands) for relation in and_group.split(" and "))
        for and_group in condition.split(" or ")
    )


def _load(plural_type: PluralType) -> Dict[str, List[Tuple[str, str]]]:
    """Parse and cache the rules for one plural type."""
    cached = _RULES.get(plural_type)
    if cached is not None:
        return cached

    by_locale: Dict[str, List[Tuple[str, str]]] = {}
    root = et.parse(_DIR / _FILES[plural_type]).getroot()
    for group in root.findall(".//pluralRules"):
        rules: List[Tuple[str, str]] = []
        for rule in group.findall("pluralRule"):
            category = rule.get("count")
            if (category is None) or (category == OTHER) or (not rule.text):
                # "other" is the fallback and carries no condition.
                continue

            # Drop the @integer/@decimal sample clauses.
            condition = re.split(r"@(?:integer|decimal)", rule.text)[0].strip()
            if condition:
                rules.append((category, condition))

        for locale in (group.get("locales") or "").split():
            by_locale[locale] = rules

    _RULES[plural_type] = by_locale
    return by_locale


def get_plural_category(
    language: str,
    number: Union[int, float, Decimal],
    plural_type: PluralType = PluralType.CARDINAL,
) -> str:
    """Return the CLDR plural category of a number in a language.

    Falls back to "other" for a language CLDR does not cover, which is also
    the category every language uses when nothing else matches.
    """
    by_locale = _load(plural_type)

    rules = by_locale.get(language)
    if rules is None:
        # en_IN -> en, pt_PT -> pt
        base = re.split(r"[_-]", language)[0]
        rules = by_locale.get(base)

    if not rules:
        return OTHER

    operands = _operands(number)
    for category in _CATEGORY_ORDER:
        for rule_category, condition in rules:
            if (rule_category == category) and _eval_condition(condition, operands):
                return category

    return OTHER
