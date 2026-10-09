---
id: metric.venue_gmv
title: Venue GMV
type: metric
status: canonical
owner: finance-analytics
metric_id: venue_gmv
sensitivity: internal
---
GMV is the commercial volume metric for Dineflow venues.

## Definition
Venue GMV is the sum of `order_gross_amount` for paid orders, including VAT, excluding tips, refunds, and failed payments. Currency is the venue settlement currency; GCC reporting converts to AED using the Finance daily rate at order time, not at payout time.

## Timing
An order enters GMV when payment status becomes `captured`, not when the kitchen ticket is printed.
