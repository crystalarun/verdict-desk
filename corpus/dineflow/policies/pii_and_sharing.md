---
id: policy.pii_sharing
title: Customer data sharing
type: policy
status: canonical
owner: data-governance
sensitivity: confidential
---
Dineflow treats consumer phone numbers, emails, and payment identifiers as restricted.

## Slack and email
Do not paste consumer phone numbers, emails, Emirates IDs, or full order dumps into Slack, WhatsApp, or personal email. If an incident needs a record, use `venue_id` plus `order_id` and request access through the warehouse ACL.

## Vendors
No consumer-level extract leaves the warehouse without a ticket in the access register and a named deletion date. Aggregates with fewer than 15 consumers in a segment are not exported.
