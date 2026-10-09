# Verdict Desk

Most analytics AI demos answer anyway. This one issues a **verdict**:

- **answer** — with a quote from the canonical pack
- **conflict** — canonical and superseded definitions both showed up
- **abstain** — nothing in the pack supports the question
- **block** — jailbreak / policy tripwire

It is a small citation engine for metric definitions, data contracts, access rules, and runbooks. It is not a chatbot glued to a PDF folder.

I built this as a public portfolio piece. I lead BI and analytics (KPI standards, Snowflake modelling, customer analytics, governance). The point is to show how I would constrain an AI assistant in that job — not to pretend I shipped a foundation model.

## Why this shape

In a real analytics org the expensive failure is not "the model was 3% less fluent". It is:

1. Two dashboards using different churn definitions
2. Someone pasting customer phones into Slack
3. An exec number published while the orders mart is stale
4. An experiment called as a win on the wrong grain

Those are document problems before they are model problems. So v0.1 does **extractive** answers only. If the sentence is not in the corpus, the desk will not write it.

The corpus is **Dineflow**, a fictional GCC restaurant-commerce company. No employer data.

Sister repos:

- [verdict-eval](https://github.com/crystalarun/verdict-eval) — golden cases and a CI gate
- [verdict-router](https://github.com/crystalarun/verdict-router) — cheap vs expensive model path (later)

## Quick start

Python 3.11+. No API key.

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/evaluate.py

python -m verdict_desk.cli "What is the official definition of 30-day venue churn?"
python -m verdict_desk.cli "Can I paste customer phone numbers into Slack?"
python -m verdict_desk.cli "What is our employee NPS in the Riyadh office?"
```

API extra:

```bash
python -m pip install -e ".[api]"
uvicorn verdict_desk.api:app --host 127.0.0.1 --port 8000
```

```bash
curl -s http://127.0.0.1:8000/v1/verdict \
  -H 'Content-Type: application/json' \
  -d '{"question":"When does an order enter venue GMV?"}'
```

## What is in the pack

| Doc | Why it is there |
| --- | --- |
| 30-day venue churn (canonical + superseded) | Conflicting definitions are the real failure mode |
| Venue GMV | Timing and tax rules that people guess wrong |
| Repeat order rate | Grain mistakes (averaging venue rates) |
| PII / sharing policy | Slack and vendor extracts |
| Orders warehouse delay runbook | Stale exec tiles |
| Experiment readout rules | Calling a win too early |
| Orders grain contract | GMV vs item-level sums |

## Design choices I would defend in an interview

- **No paid LLM in v0.1.** The contract is the product. Generation can be added later behind the same verdict object.
- **Stdlib retrieval.** BM25 over a few dozen canonical docs is enough to test the decision layer. Hybrid search belongs in a later milestone, with a measured ablation, not as decoration.
- **Conflict is a first-class outcome.** Hiding the legacy churn definition would make the demo look cleaner and the system worse.
- **Residual risk is printed on every verdict.** "This is a quote, not a live warehouse number."

## v0.1 limits (intentional)

- Extractive quotes only; no synthesis
- English corpus
- Regex PII (email, UAE mobile, Emirates ID), not a full Presidio profile
- Jailbreak list is a tripwire, not a classifier
- No AWS deploy in this version (stays at $0)

## License

MIT
