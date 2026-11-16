
from pipeline.keyword_extraction import extract_keywords


def test_extracts_keywords():
    result = extract_keywords(
        "OpenAI releases a new GPT model",
        "The new GPT model uses advanced language "
        "processing and generative AI technology."
    )

    assert len(result) > 0
    assert len(result) <= 8


def test_empty_article():
    assert extract_keywords("", "") == []


def test_custom_keyword_count():
    result = extract_keywords(
        "Machine learning research",
        "Machine learning models are used in AI research.",
        top_n=3
    )

    assert len(result) <= 3


def test_non_positive_keyword_count():
    assert extract_keywords("AI research", "Machine learning", 0) == []
