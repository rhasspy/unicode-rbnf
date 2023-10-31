from abc import ABC
from bisect import bisect_left
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from math import log10
from pathlib import Path
from typing import Dict, Final, Iterable, List, Optional
from xml.etree import ElementTree as et

DEFAULT_LANGUAGE: Final = "en"
DEFAULT_RULESET_NAME: Final = "spellout-numbering"

_LANG_DIR = Path(__file__).parent / "rbnf"


class RbnfRulePart(ABC):
    """Abstract base class for rule parts."""


@dataclass
class TextRulePart(RbnfRulePart):
    """Literal text rule part."""

    text: str
    """Literal text to insert."""


class SubType(str, Enum):
    """Type of substitution."""

    REMAINER = "remainder"
    """Use remainder for rule value."""

    QUOTIENT = "quotient"
    """Use quotient for rule value."""


@dataclass
class SubRulePart(RbnfRulePart):
    """Substitution rule part."""

    type: SubType
    """Type of substitution."""

    is_optional: bool = False
    """True if substitution is optional."""

    text_before: str = ""
    """Text to insert before substitution."""

    text_after: str = ""
    """Text to insert after substitution."""

    ruleset_name: Optional[str] = None
    """Ruleset name to use during substitution (None for current ruleset name)."""


@dataclass
class ReplaceRulePart(RbnfRulePart):
    """Replace with other ruleset (keep value)."""

    ruleset_name: str
    """Name of ruleset to use."""


class ParseState(str, Enum):
    """Set of rbnf parser."""

    TEXT = "text"
    SUB_OPTIONAL_BEFORE = "optional_before"
    SUB_OPTIONAL_AFTER = "optional_after"
    SUB_REMAINER = "remainder"
    SUB_QUOTIENT = "quotient"
    SUB_RULESET_NAME = "sub_ruleset_name"
    REPLACE_RULESET_NAME = "replace_ruleset_name"


@dataclass
class RbnfRule:
    """Parsed rbnf rule."""

    value: int
    """Numeric lookup value for rule."""

    parts: List[RbnfRulePart] = field(default_factory=list)
    """Parts of rule in order to be processed."""

    @staticmethod
    def parse(value: int, text: str) -> "RbnfRule":
        """Parse RBNF rule for a value."""
        rule = RbnfRule(value=value)
        state = ParseState.TEXT
        part: Optional[RbnfRulePart] = None
        is_sub_optional = False
        sub_text_before = ""

        for c in text:
            if c == ";":
                break

            if c in (">", "→"):
                # Divide the number by the rule's divisor and format the remainder
                if state in {ParseState.TEXT, ParseState.SUB_OPTIONAL_BEFORE}:
                    state = ParseState.SUB_REMAINER
                    part = SubRulePart(
                        SubType.REMAINER,
                        is_optional=is_sub_optional,
                        text_before=sub_text_before,
                    )
                    rule.parts.append(part)
                    sub_text_before = ""
                elif state in {ParseState.SUB_REMAINER, ParseState.SUB_RULESET_NAME}:
                    if is_sub_optional:
                        state = ParseState.SUB_OPTIONAL_AFTER
                    else:
                        state = ParseState.TEXT
                        part = None
                else:
                    raise ValueError(f"Got {c} in {state}")
            elif c in ("<", "←"):
                # Divide the number by the rule's divisor and format the quotient
                if state in {ParseState.TEXT, ParseState.SUB_OPTIONAL_BEFORE}:
                    state = ParseState.SUB_QUOTIENT
                    part = SubRulePart(SubType.QUOTIENT, is_optional=is_sub_optional)
                    rule.parts.append(part)
                elif state in {ParseState.SUB_QUOTIENT, ParseState.SUB_RULESET_NAME}:
                    if is_sub_optional:
                        state = ParseState.SUB_OPTIONAL_AFTER
                    else:
                        state = ParseState.TEXT
                        part = None
                else:
                    raise ValueError(f"Got {c} in {state}")
            elif c == "%":
                # =%rule_name= replacement
                if state in {ParseState.SUB_QUOTIENT, ParseState.SUB_REMAINER}:
                    assert isinstance(part, SubRulePart)
                    state = ParseState.SUB_RULESET_NAME
                    part.ruleset_name = ""
                elif state == ParseState.REPLACE_RULESET_NAME:
                    pass
                else:
                    raise ValueError(f"Got {c} in {state}")
            elif c == "[":
                # [optional] (start)
                if state == ParseState.TEXT:
                    is_sub_optional = True
                    state = ParseState.SUB_OPTIONAL_BEFORE
                    sub_text_before = ""
                else:
                    raise ValueError(f"Got {c} in {state}")
            elif c == "]":
                # [optional] (end)
                if state == ParseState.SUB_OPTIONAL_AFTER:
                    is_sub_optional = False
                    state = ParseState.TEXT
                    part = None
                else:
                    raise ValueError(f"Got {c} in {state}")
            elif c == "=":
                # =%rule_name= replacement
                if state == ParseState.TEXT:
                    part = ReplaceRulePart("")
                    rule.parts.append(part)
                    state = ParseState.REPLACE_RULESET_NAME
                elif state == ParseState.REPLACE_RULESET_NAME:
                    part = None
                    state = ParseState.TEXT
                else:
                    raise ValueError(f"Got {c} in {state}")
            elif state == ParseState.SUB_OPTIONAL_BEFORE:
                # [before ...]
                sub_text_before += c
            elif state == ParseState.SUB_OPTIONAL_AFTER:
                # [... after]
                assert isinstance(part, SubRulePart)
                part.text_after += c
            elif state == ParseState.SUB_RULESET_NAME:
                # %ruleset_name in << or >>
                assert isinstance(part, SubRulePart)
                assert part.ruleset_name is not None
                part.ruleset_name += c
            elif state == ParseState.REPLACE_RULESET_NAME:
                # =%ruleset_name=
                assert isinstance(part, ReplaceRulePart)
                part.ruleset_name += c
            elif state == ParseState.TEXT:
                # literal text
                if part is None:
                    part = TextRulePart("")
                    rule.parts.append(part)

                assert isinstance(part, TextRulePart)
                part.text += c
            else:
                raise ValueError(f"Got {c} in {state}")

        return rule


@dataclass
class RbnfRuleSet:
    """Named collection of rbnf rules."""

    name: str
    """Name of ruleset."""

    numeric_rules: Dict[int, RbnfRule] = field(default_factory=dict)
    """Rules keyed by lookup number."""

    _sorted_numbers: Optional[List[int]] = field(default=None)
    """Sorted list of numeric_rules keys (updated on demand)."""

    def update(self) -> None:
        """Force update to sorted key list."""
        self._sorted_numbers = sorted(self.numeric_rules.keys())

    def find_rule(self, number: int) -> Optional[RbnfRule]:
        """Look up closest rule by number."""
        if (self._sorted_numbers is None) or (
            len(self._sorted_numbers) != len(self.numeric_rules)
        ):
            self.update()

        assert self._sorted_numbers is not None

        # Find index of place where number would be inserted
        index = bisect_left(self._sorted_numbers, number)
        num_rules = len(self._sorted_numbers)

        if index >= num_rules:
            # Last rule
            index = num_rules - 1
        elif index < 0:
            # First rule
            index = 0

        rule_number = self._sorted_numbers[index]
        if number < rule_number:
            # Not an exact match, use one rule down
            index = max(0, index - 1)
            rule_number = self._sorted_numbers[index]

        return self.numeric_rules.get(rule_number)


class RbnfEngine:
    """Formatting engine using rbnf."""

    def __init__(self, language: Optional[str] = None) -> None:
        # Default language
        self.language = language

        # lang -> ruleset name -> ruleset
        self.rulesets: Dict[str, Dict[str, RbnfRuleSet]] = defaultdict(dict)

    @staticmethod
    def for_language(language: str) -> "RbnfEngine":
        """Load XML rules for a language and construct an engine."""
        xml_path = _LANG_DIR / f"{language}.xml"
        if not xml_path.is_file():
            raise ValueError(f"{language} is not supported")

        engine = RbnfEngine(language=language)
        with open(xml_path, "r", encoding="utf-8") as xml_file:
            root = et.fromstring(xml_file.read())
            engine.load_xml(root)

        return engine

    def add_rule(
        self,
        value: int,
        rule_text: str,
        ruleset_name: Optional[str] = None,
        language: Optional[str] = None,
    ) -> RbnfRule:
        """Manually add a rule to the engine."""
        language = language or self.language or DEFAULT_LANGUAGE
        ruleset_name = ruleset_name or DEFAULT_RULESET_NAME

        ruleset = self.rulesets[language].get(ruleset_name)
        if ruleset is None:
            ruleset = RbnfRuleSet(name=ruleset_name)
            self.rulesets[language][ruleset_name] = ruleset

        rule = RbnfRule.parse(value, rule_text)
        ruleset.numeric_rules[value] = rule

        return rule

    def load_xml(self, root: et.Element, language: Optional[str] = None) -> None:
        """Load an XML file with rbnf rules."""
        if language is None:
            lang_elem = root.find("identity/language")
            language = (
                lang_elem.attrib["type"] if lang_elem is not None else DEFAULT_LANGUAGE
            )

        for group_elem in root.findall("rbnf//ruleset"):
            ruleset = RbnfRuleSet(name=group_elem.attrib["type"])
            for rule_elem in group_elem.findall("rbnfrule"):
                if not rule_elem.text:
                    continue

                value = rule_elem.attrib["value"]
                try:
                    value_int = int(value)
                    ruleset.numeric_rules[value_int] = RbnfRule.parse(
                        value_int, rule_elem.text
                    )
                except ValueError:
                    # Ignore for now
                    pass

            self.rulesets[language][ruleset.name] = ruleset

    def format_number(
        self,
        number: int,
        ruleset_name: Optional[str] = None,
        language: Optional[str] = None,
    ) -> str:
        """Format a number using loaded rulesets."""
        return "".join(
            self.iter_format_number(
                number, ruleset_name=ruleset_name, language=language
            )
        )

    def iter_format_number(
        self,
        number: int,
        ruleset_name: Optional[str] = None,
        language: Optional[str] = None,
    ) -> Iterable[str]:
        """Format a number using loaded rulesets (generator)."""
        language = language or self.language or DEFAULT_LANGUAGE
        ruleset_name = ruleset_name or DEFAULT_RULESET_NAME

        ruleset = self.rulesets[language].get(ruleset_name)
        if ruleset is None:
            raise ValueError(f"No ruleset: {ruleset_name}")

        rule = ruleset.find_rule(number)
        if rule is None:
            raise ValueError(f"No rule for {number} in {ruleset_name}")

        if rule.value > 0:
            q, r = divmod(number, 10 ** int(log10(rule.value)))
        else:
            q, r = 0, 0

        for part in rule.parts:
            if isinstance(part, TextRulePart):
                if part.text:
                    yield part.text
            elif isinstance(part, SubRulePart):
                if (part.type == SubType.QUOTIENT) and (q > 0):
                    if part.text_before:
                        yield part.text_before
                    yield from self.iter_format_number(
                        q, ruleset_name=part.ruleset_name or ruleset_name
                    )
                    if part.text_after:
                        yield part.text_after
                elif (part.type == SubType.REMAINER) and (r > 0):
                    if part.text_before:
                        yield part.text_before
                    yield from self.iter_format_number(
                        r, ruleset_name=part.ruleset_name or ruleset_name
                    )
                    if part.text_after:
                        yield part.text_after
            elif isinstance(part, ReplaceRulePart):
                yield from self.iter_format_number(
                    number, ruleset_name=part.ruleset_name
                )
