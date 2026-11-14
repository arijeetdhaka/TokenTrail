---
name: tokentrail-github-scout
description: Discover and evaluate useful AI and machine learning GitHub repositories for TokenTrail.
version: 1.0.0
---

# TokenTrail GitHub Scout

## Mission
Discover useful, relevant and interesting open-source AI projects.

## Research workflow
1. Search GitHub for repositories related to AI.
2. Prioritize machine learning, generative AI, LLMs, AI agents, NLP and computer vision.
3. Inspect the repository description, README and available activity information.
4. Check the original repository URL.
5. Identify the main purpose and practical use case.
6. Avoid duplicate repositories and irrelevant projects.

## Evaluation
Consider:
- Relevance to AI
- Project purpose
- Programming language
- Stars, when available
- Recent activity, when available
- Documentation quality

Do not assume a high star count means a project is high quality.

## Output
Return structured JSON records with:
- name
- description
- url
- language
- stars
- topics
- updated_at
- use_case

Do not fabricate repository statistics or activity dates. Use null when unavailable.
