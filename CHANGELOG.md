# Changelog

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

