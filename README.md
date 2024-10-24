# Unicode RBNF

A pure Python implementation of [rule based number formatting](https://icu-project.org/docs/papers/a_rule_based_approach_to_number_spellout/) (RBNF) using the [Unicode Common Locale Data Repository](https://cldr.unicode.org) (CLDR).

This lets you spell out numbers for a large number of locales:

``` python
from unicode_rbnf import RbnfEngine

engine = RbnfEngine.for_language("en")
assert engine.format_number(1234).text == "one thousand two hundred thirty-four"
```

Different formatting purposes are supported as well, depending on the locale:

``` python
from unicode_rbnf import RbnfEngine, FormatPurpose

engine = RbnfEngine.for_language("en")
assert engine.format_number(1999, FormatPurpose.CARDINAL).text == "one thousand nine hundred ninety-nine"
assert engine.format_number(1999, FormatPurpose.YEAR).text == "nineteen ninety-nine"
assert engine.format_number(11, FormatPurpose.ORDINAL).text == "eleventh"
```

For locales with multiple genders, cases, etc., the different texts are accessible in the result of `format_number`:

``` python
from unicode_rbnf import RbnfEngine

engine = RbnfEngine.for_language("de")
print(engine.format_number(1))
```

Result:

```
FormatResult(
  text='eins',
  text_by_ruleset={
    'spellout-numbering': 'eins',
    'spellout-cardinal-neuter': 'ein',
    'spellout-cardinal-masculine': 'ein',
    'spellout-cardinal-feminine': 'eine',
    'spellout-cardinal-n': 'einen',
    'spellout-cardinal-r': 'einer',
    'spellout-cardinal-s': 'eines',
    'spellout-cardinal-m': 'einem'
  }
)
```

The `text` property of the result holds the text of the ruleset with the shortest name (least specific).

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
* Preceding reminder substitution (`>>>` or `→→→`)
* Number format strings (`==`)
