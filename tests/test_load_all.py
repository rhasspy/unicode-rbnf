from unicode_rbnf import RbnfEngine

import pytest


@pytest.mark.parametrize("language", RbnfEngine.get_supported_languages())
def test_load_language(language: str):
    engine = RbnfEngine.for_language(language)
    assert engine.format_number(0).text
