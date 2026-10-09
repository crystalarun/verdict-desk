---
id: playbook.ab_readout
title: Experiment readout rules
type: playbook
status: canonical
owner: product-analytics
sensitivity: internal
---

## Guardrail
A Dineflow experiment may be called only if the pre-registered primary metric moved with 95% confidence, sample ratio mismatch is under 2%, and no guardrail metric (checkout failure rate, refund rate) degraded.

## Reporting
Do not mix users who saw both variants. Do not use venue GMV as a proxy primary metric for a consumer checkout test.
