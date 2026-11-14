
from pipeline.preprocessing import clean_text


def test_remove_html_tags():
    result = clean_text("<p>Hello AI</p>")
    assert result == "Hello AI"


def test_decode_html_entities():
    result = clean_text("AI &amp; Machine Learning")
    assert result == "AI & Machine Learning"


def test_remove_extra_spaces():
    result = clean_text("  Hello     AI   World  ")
    assert result == "Hello AI World"


def test_handle_none():
    result = clean_text(None)
    assert result == ""


def test_handle_empty_string():
    result = clean_text("")
    assert result == ""
