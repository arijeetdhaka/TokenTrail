"""Pick the best learning topic for a piece of text using keyword rules.

Simple and explainable: every topic has a few patterns; the topic with the most
matching patterns wins. Ties go to the topic listed first (the more specific ones
are listed first). No match means no topic, never a guess.
"""
import re

TOPIC_PATTERNS: dict[str, list[str]] = {
    # Most specific first
    "rag": [r"\brag\b", r"retrieval[- ]augmented", r"\bretriev"],
    "vector-databases": [r"vector (database|store|search|db)", r"\bpgvector\b", r"\bfaiss\b", r"\bpinecone\b",
                         r"\bchroma\b", r"\bmilvus\b", r"\bweaviate\b", r"\bqdrant\b"],
    "embeddings": [r"\bembed", r"sentence[- ]transformers?", r"\bminilm", r"\bbge\b", r"\be5\b",
                   r"\bmpnet", r"\bgte\b", r"sentence similarity"],
    "fine-tuning": [r"fine[- ]?tun", r"\blora\b", r"\bqlora\b", r"\bpeft\b", r"instruction[- ]tun"],
    "multi-agent-systems": [r"multi[- ]agent"],
    "tool-calling": [r"tool[- ]?(calling|use)", r"function[- ]calling", r"\bmcp\b"],
    "prompt-engineering": [r"\bprompt"],
    "multimodal-ai": [r"multi[- ]?modal", r"vision[- ]language", r"text[- ]to[- ](image|video|speech)",
                      r"stable[- ]diffusion", r"\bsdxl\b", r"\bflux\b", r"\bdiffusion", r"\bclip\b",
                      r"video generation"],
    "llms": [r"\bllms?\b", r"large language model", r"language models?\b", r"\bgpt", r"\bllama", r"\bqwen",
             r"\bmistral", r"\bgemma", r"\bdeepseek", r"\bphi[- ]?\d", r"\bchatbot", r"\bchatgpt",
             r"\binstruct\b", r"\b\d+(\.\d+)?b\b"],
    "agent-architectures": [r"\bagents?\b", r"\bagentic", r"\blangchain", r"\blanggraph", r"\bautogen",
                            r"\bcrewai"],
    "planning": [r"\bplanning\b", r"\bplanner"],
    "memory": [r"agent memory", r"long[- ]term memory"],
    "agentic-workflows": [r"\bworkflows?\b"],
    "reinforcement-learning": [r"reinforcement learning", r"\brl\b", r"\brlhf\b", r"\breward"],
    "robotics": [r"\brobot", r"\bdrones?\b", r"\buavs?\b", r"\bnavigation", r"\bembodied", r"\bmanipulation"],
    "computer-vision": [r"computer vision", r"\bimage", r"\bvision\b", r"object detection", r"segmentation",
                        r"\byolo", r"\bvideo\b", r"\bpixel", r"\bocr\b", r"\bresnet", r"\bvit\b", r"\btimm\b"],
    "nlp": [r"\bnlp\b", r"natural language", r"text classification", r"sentiment", r"named entity",
            r"translation", r"summari[sz]", r"\bspeech\b", r"bert\b", r"\broberta", r"\bdeberta",
            r"\bdistilbert"],
    "transformers": [r"\btransformers?\b", r"\battention\b", r"\bkv[- ]cache"],
    "cnns": [r"\bcnns?\b", r"convolutional", r"\bmobilenet", r"\bconvnext", r"\befficientnet"],
    "rnns": [r"\brnns?\b", r"recurrent", r"\blstm", r"\bgru\b"],
    "optimization": [r"gradient descent", r"\boptimi[sz]", r"\bsgd\b", r"\badam\b"],
    "neural-networks": [r"neural networks?", r"deep learning", r"\bpytorch\b", r"\btensorflow\b", r"\bkeras\b"],
    "mlops": [r"\bmlops\b", r"\bmlflow\b", r"\bkubeflow\b", r"model monitoring", r"experiment tracking"],
    "ai-deployment": [r"\bdeploy", r"\binference\b", r"\bserving\b", r"\bquantiz", r"\bonnx\b", r"\bvllm\b", r"\bgguf\b",
                      r"\bdocker"],
    "unsupervised-learning": [r"unsupervised", r"self[- ]supervised", r"anomaly detection",
                              r"dimensionality reduction"],
    "supervised-learning": [r"\bsupervised"],
    "clustering": [r"\bcluster"],
    "classification": [r"\bclassif"],
    "regression": [r"\bregression", r"\bforecast"],
    "model-evaluation": [r"\bbenchmark", r"\bevaluat"],
    "feature-engineering": [r"feature (engineering|selection|extraction)", r"\bpreprocess"],
    "statistics-and-probability": [r"\bstatistic", r"\bprobabilit", r"\bbayesian"],
    "mathematics-for-ai": [r"linear algebra", r"\bcalculus", r"\bmathemat"],
    "data-structures-and-algorithms": [r"data structures?", r"\balgorithms?\b", r"\bleetcode", r"\bdsa\b"],
    "python-for-ai": [r"\bpython\b", r"\bnumpy\b", r"\bpandas\b", r"\bjupyter"],
}

_COMPILED = {slug: [re.compile(p) for p in patterns] for slug, patterns in TOPIC_PATTERNS.items()}


def match_topic(name: str | None, description: str | None = None) -> str | None:
    """Return the slug of the best matching topic, or None if nothing matches.

    A match in the name counts double, because a title says more than a long description.
    """
    def clean(text: str | None) -> str:
        # Treat / _ - . as spaces so "Qwen/Qwen3-8B" reads as "qwen qwen3 8b"
        return re.sub(r"[/_.-]", " ", (text or "").lower())

    title, body = clean(name), clean(description)
    best_slug, best_score = None, 0
    for slug, patterns in _COMPILED.items():
        score = sum(2 * bool(p.search(title)) + bool(p.search(body)) for p in patterns)
        if score > best_score:
            best_slug, best_score = slug, score
    return best_slug
