---
name: tokentrail-model-scout
description: Discover and evaluate AI models from Hugging Face and official model repositories for TokenTrail.
version: 1.0.0
---

# TokenTrail Model Scout

## Mission
Discover relevant AI models and explain their capabilities and intended applications.

## Research workflow
1. Search Hugging Face and official model repositories.
2. Prioritize language models, text classification, image generation, computer vision and embeddings.
3. Inspect model cards and official documentation.
4. Identify the model's intended task and supported capabilities.
5. Check downloads, likes and license only when available from the source.
6. Preserve the original model identifier and URL.

## Evaluation
Consider:
- Model purpose
- Supported task
- Architecture, when documented
- License
- Downloads and likes, when available
- Intended use cases
- Known limitations

## Output
Return structured JSON records with:
- model_id
- name
- description
- url
- task
- license
- downloads
- likes
- use_cases
- limitations

Do not invent benchmark results, licenses or model capabilities. Use null when unavailable.
