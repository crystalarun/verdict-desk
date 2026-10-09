# Arun Kumar

Director of BI & Analytics. Dubai.

I have spent 11+ years building analytics functions in fintech, digital assets, and high-growth product companies: KPI standards, Snowflake modelling, customer analytics, experimentation, and data governance.

Public work right now is **Verdict** — an evidence-first analytics assistant. It quotes canonical metric definitions and runbooks, or it refuses. It does not invent numbers.

## Verdict

| Repo | What it is |
| --- | --- |
| [verdict-desk](https://github.com/crystalarun/verdict-desk) | Citation engine: answer / conflict / abstain / block |
| [verdict-eval](https://github.com/crystalarun/verdict-eval) | Golden cases; CI fails on regressions |
| [verdict-router](https://github.com/crystalarun/verdict-router) | Cheap path by default; paid models stay off |

Case study: [docs/CASE_STUDY.md](https://github.com/crystalarun/verdict-desk/blob/main/docs/CASE_STUDY.md)

```bash
git clone https://github.com/crystalarun/verdict-desk.git
cd verdict-desk
python -m pip install -e .
python -m unittest discover -s tests -v
python -m verdict_desk.cli "What is the official definition of 30-day venue churn?"
```

## Not in these repos

Hybrid vector search, paid LLMs, AWS deploy, and a live demo endpoint. I will not list them on a CV until they exist.

## Elsewhere

- [LinkedIn](https://www.linkedin.com/in/arun-kumar5)
- Other public work: [DE_Agent](https://github.com/crystalarun/DE_Agent)
