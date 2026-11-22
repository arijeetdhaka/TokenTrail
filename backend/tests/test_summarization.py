
from pipeline.summarization import (
    summarize_article,
    split_sentences
)


def test_split_sentences():
    text = "AI is growing. Machine learning is useful. NLP is powerful."

    result = split_sentences(text)

    assert len(result) == 3


def test_empty_article():
    result = summarize_article("", "")

    assert result == ""


def test_summary_with_short_article():
    text = "AI is growing. NLP is useful."

    result = summarize_article("AI News", text, 3)

    assert result == text


def test_summary_respects_max_sentences():
    text = (
        "AI is growing rapidly. "
        "Machine learning helps computers learn. "
        "NLP processes human language. "
        "Deep learning uses neural networks. "
        "AI is used in healthcare."
    )

    result = summarize_article("", text, 2)

    assert len(split_sentences(result)) == 2


def test_zero_max_sentences():
    text = "AI is growing. NLP is useful."

    result = summarize_article("", text, 0)

    assert result == ""


def test_empty_title_with_article():
    text = "AI is growing. NLP is useful."

    result = summarize_article("", text, 1)

    assert result != ""
