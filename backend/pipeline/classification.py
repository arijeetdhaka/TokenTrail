
import re

CATEGORIES = {
    "AI News": [
    "artificial intelligence",
    "artificial intelligence news",
],
    "Machine Learning": [
        "machine learning", "supervised learning",
        "unsupervised learning", "regression", "classification"
    ],
    "Deep Learning": [
        "deep learning", "neural network", "CNN",
        "RNN", "transformer"
    ],
    "Generative AI": [
        "generative AI", "text generation",
        "image generation", "prompt engineering"
    ],
    "Large Language Models": [
        "large language model", "LLM", "GPT",
        "language model", "BERT"
    ],
    "AI Agents": [
        "AI agent", "autonomous agent", "agentic",
        "tool calling", "multi-agent"
    ],
    "Research and Breakthroughs": [
        "research paper", "research breakthrough",
        "scientific discovery", "new research"
    ],
    "Open Source AI": [
        "open source", "open-source model",
        "open weights"
    ],
    "AI Tools and Frameworks": [
        "AI tool", "AI framework", "TensorFlow",
        "PyTorch", "LangChain"
    ],
    "Computer Vision": [
        "computer vision", "image recognition",
        "object detection", "image processing"
    ],
    "Natural Language Processing": [
        "natural language processing", "NLP",
        "text analysis", "sentiment analysis"
    ],
    "Robotics": [
        "robotics", "robot", "humanoid robot",
        "autonomous robot"
    ],
    "AI Companies and Industry": [
        "AI company", "AI industry", "OpenAI",
        "Google DeepMind", "Anthropic"
    ],
    "Model Releases and Updates": [
        "releases", "released", "launches",
        "new model", "model update"
    ]
}


def classify_article(title: str, text: str) -> list[str]:
    """
    Assign relevant categories to an AI news article.
    One article can have multiple categories.
    """

    content = f"{title} {text}".lower()

    matched_categories = []

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            pattern = r"(?<!\w)" + re.escape(keyword.strip().lower()) + r"(?!\w)"

            if re.search(pattern, content):
                matched_categories.append(category)
                break

    return matched_categories
