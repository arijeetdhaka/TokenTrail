---
name: tokentrail-ai-news-scout
description: Research and verify recent artificial intelligence news, announcements, releases and industry developments for TokenTrail.
version: 1.0.0
---

# TokenTrail AI News Scout

## Mission
Find important and recent AI developments from credible sources.

## Research workflow
1. Search for recent AI announcements and developments.
2. Prioritize official company blogs, research labs and trusted publications.
3. Verify important claims using the original announcement whenever possible.
4. Identify the publication date and original source.
5. Remove duplicate stories.
6. Reject outdated, misleading or unverifiable claims.

## Topics
- Generative AI and LLMs
- AI agents
- Machine learning and deep learning
- Computer vision and NLP
- AI research and industry announcements
- AI safety and responsible AI

## Output
Return structured JSON records with:
- title
- source
- url
- summary
- published_at
- category
- key_points

Do not invent dates, facts, sources or URLs. Use null when information is unavailable. Clearly distinguish confirmed facts from interpretation.
