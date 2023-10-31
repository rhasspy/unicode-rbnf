# Unicode RBNF

A pure Python implementation of [rule based number formatting](https://icu-project.org/docs/papers/a_rule_based_approach_to_number_spellout/) (RBNF) using the [Unicode Common Locale Data Repository](https://cldr.unicode.org) (CLDR).

This lets you spell out numbers for a large number of locales:

``` python
from unicode_rbnf import RbnfEngine

engine = RbnfEngine.for_language("en")
assert engine.format_number(1234) == "one thousand two hundred thirty-four"
```

Depending on the locale, different rulesets are supported as well:

``` python
from unicode_rbnf import RbnfEngine, RulesetName

engine = RbnfEngine.for_language("en")
assert engine.format_number(1999, RulesetName.YEAR) == "nineteen ninety-nine"
assert engine.format_number(11, RulesetName.ORDINAL) == "eleventh"
```

## Supported locales

See: https://github.com/unicode-org/cldr/tree/release-44/common/rbnf

## Engine implementation

Not [all features](https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classRuleBasedNumberFormat.html) of the RBNF engine are implemented. The following features are available:

* Literal text (`hundred`)
* Quotient substitution (`<<` or `←←`)
* Reminder substitution (`>>` or `→→`)
* Optional substitution (`[...]`)
* Rule substituton (`←%ruleset_name←`)
* Rule replacement (`=%ruleset_name=`)
* Special rules:
    * Negative numbers (`-x`)
    * Improper fractions (`x.x`)
    * Not a number (`NaN`)
    * Infinity (`Inf`)
    
Some features that will need to be added eventually:

* Proper fraction rules (`0.x`)
* Preceding eeminder substitution (`>>>` or `→→→`)
* Number format strings (`==`)
