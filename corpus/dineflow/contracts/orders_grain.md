---
id: contract.orders
title: Orders grain
type: contract
status: canonical
owner: analytics-engineering
metric_id: venue_gmv
sensitivity: internal
---

## Grain
One row per `order_id`. An order may contain many items; item-level analysis uses `order_item_id` and must not be summed as GMV.

## Keys
`venue_id` is mandatory. `consumer_account_id` may be null for guest checkout. Payment status values are `authorized`, `captured`, `refunded`, `failed`.
