---
id: runbook.orders_etl_delay
title: Orders warehouse delay
type: runbook
status: canonical
owner: data-platform
sensitivity: internal
---
Use this when the orders mart is more than 45 minutes behind POS capture.

## First checks
1. Confirm the delay in `ops.pipeline_freshness` for `mart_orders`, not in a Tableau extract.
2. If POS capture is current and only the mart is late, pause GMV and churn tiles on the exec dashboard rather than publishing stale numbers.
3. Page the platform on-call if freshness exceeds 90 minutes.

## What not to do
Do not backfill from the production POS replica during business hours. Do not recompute churn by hand in a spreadsheet while the mart is late.
