---
id: metric.churn_30d
title: 30-day venue churn
type: metric
status: canonical
owner: analytics
metric_id: churn_30d
sensitivity: internal
---
This is the only definition that may be used in executive reporting.

## Definition
A venue is counted as churned when it processed at least one paid order in the previous 30 complete calendar days and processed zero paid orders in the last 30 complete calendar days. The metric is a venue count, not a GMV amount.

## Grain and filters
Grain is `venue_id` in the Dineflow production schema. Test venues, internal canteens, and unpaid demo tenants are excluded. Partial days are not included; the window closes at 23:59 Asia/Dubai.

## Do not use
Do not use login inactivity, app uninstalls, or unpaid invoices as a substitute for this metric. Those are operational signals, not churn.
