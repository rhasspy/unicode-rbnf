# Changelog

## Unreleased

- Emit digits for `=#,##0=` style replace rules instead of failing (en 1e18 -> "1,000,000,000,000,000,000", hi `digits-ordinal-masculine` 7 -> "7वाँ") (https://github.com/rhasspy/unicode-rbnf/pull/15)
- Use the grouping sizes from the DecimalFormat pattern, so Indian `#,##,##0` gives "12,34,567" instead of "1,234,567"
- Split numbers on the largest power of the radix at or below the rule's value, like ICU, and stop formatting from rewriting cached rules (it ordinal 99999 "novemilanovemila..." -> "novantanovemila...", also hu and vec ordinals) (https://github.com/rhasspy/unicode-rbnf/pull/17)
- Reject a rule radix below 2 instead of hanging while formatting

## 2.5.0

- Speak decimals as fractions where CLDR says to, like ICU does
  - Russian: 1.5 "одна  целыхноль десятых" -> "одна целая пять десятых", 0.5 -> "пять десятых"
  - Polish: 14.89 "czternaście przecinek zero zero" -> "czternaście przecinek osiemdziesiąt dziewięć"
  - Kazakh and Kyrgyz: 1.5 "бір бүтін оннан нөл" -> "бір бүтін оннан бес"
- Keep the fractional part of negative numbers: -1.5 "minus one" -> "minus one point five" (https://github.com/rhasspy/unicode-rbnf/pull/13)
- Fix crash on numbers small enough to print in scientific notation (1e-7)
- Fix crash on negative infinity: -inf -> "minus infinity"
- Keep a plural form inside an optional [...] group with its substitution, and text after a plural form in order
- Remove doubled and trailing spaces from output (Arabic ordinals, Arabic and Hebrew decimals)
- Add Arabic, Kazakh and Russian tests, and turn on the Polish decimal tests

## 2.4.1

- Select plural forms with CLDR plural rules instead of the final digit
  - Fixes Russian, Ukrainian, Belarusian and Polish in the 11-14 range, e.g. ru 12000 "двенадцать тысячи" -> "двенадцать тысяч"
- Fix Slovak hundreds: 100-199 spelled out as "jednasto ..." instead of "sto ..."
- Fix Slovak and Czech thousands: 1000-1999 spelled out as "jedna tisíc ..." instead of "tisíc ..."
- Fix Czech thousands gender: 2000 "dvě tisíce" -> "dva tisíce" ("tisíc" is masculine)
- Fix Serbian (sr, sr_Latn): a spoken multiplier of one, and missing agreement on the counted noun
  - 1000 "једна хиљаду" -> "хиљаду", 2000000 "два милион" -> "два милиона"
- Fix Romanian millions: "unu milion" -> "un milion"
- Add Slovak, Czech, Russian, Serbian, Romanian and plural-rule tests

## 2.4.0

- Render digit-by-digit after decimal point (0.123 -> zero point one two three)
- Initial support for Zulu (up to 19,999)

## 2.3.0

- Fix Romanian feminine numerals (https://github.com/rhasspy/unicode-rbnf/pull/8)
- Correct Slovenian spellings/grammar (https://github.com/rhasspy/unicode-rbnf/pull/7)
- Handle case where only sub-rules match (https://github.com/OHF-Voice/speech-to-phrase/issues/15)

## 2.2.0

- Fix use of optional sub part with zero remainder
- Transition to pyproject.toml

## 2.1.0

- Ensure all supported languages can load
- Start on decimal pattern format implementation (not complete)

## 2.0.0

- Change `format_number` to return `FormatResult` instead of a `str`
- Remove `RulesetName` enum and add `FormatPurpose` instead
- Add `purpose` to `format_number`, which selects all relevant rulesets
- Allow multiple ruleset names in `format_number` (prefer using `purpose`)
- Require an `RbnfEngine` to have a single language

## 1.3.0

- Remove soft hyphens by default (U+00AD)
- Search for special rules in replacement rules

## 1.2.0

- Fix zero remainder rules

## 1.1.0

- Add `get_supported_languages` method to engine
- Fix issue with "x,x" improper fraction rule
- Compute tolerance against rounded value instead of floor
- Use Decimal for string input
- Add command-line interface

## 1.0.0

- Initial release

