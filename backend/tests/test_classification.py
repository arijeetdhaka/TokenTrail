
from pipeline.classification import classify_article


def test_generates_multiple_categories():
    result = classify_article(
        "OpenAI releases a new GPT model",
        "The new generative AI model improves language generation."
    )

    assert "Generative AI" in result
    assert "Large Language Models" in result
    assert "AI Companies and Industry" in result
    assert "Model Releases and Updates" in result


def test_deep_learning_classification():
    result = classify_article(
        "New research on neural networks",
        "Researchers developed a deep learning model."
    )

    assert "Deep Learning" in result
    assert "Research and Breakthroughs" in result


def test_robotics_classification():
    result = classify_article(
        "New humanoid robot introduced",
        "The robotics company developed an autonomous robot."
    )

    assert "Robotics" in result


def test_unmatched_article():
    result = classify_article(
        "Weather forecast for tomorrow",
        "Expect sunny skies."
    )

    assert result == []


def test_empty_article():
    result = classify_article("", "")

    assert result == []
