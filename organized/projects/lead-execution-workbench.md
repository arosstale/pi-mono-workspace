# Lead Execution Workbench Project Plan

## Objective

Turn lead actions into a true execution cockpit with operational metrics and disciplined execution.

## Scope

1. **Lead Action Workbench UI**: Expand each lead card into quick action buttons for calling, texting, booking an intro, scheduling a follow-up, marking as invalid, or no response.
2. **SLA Enforcement (Disciplined, Not Noisy)**: Implement rules for showing red SLA badges, emitting discipline events per lead per 6 hours, and integrating into the Execution Discipline Layer.
3. **Roundtable Hook (Daily Execution Intelligence)**: Add an endpoint for daily execution intel, including new leads in the last 24 hours, SLA breaches, unworked leads, and top oldest open leads.
4. **Metrics Layer (Operational Intelligence)**: Measure execution performance with core metrics (first seen at, first contacted at, booked at, closed at, status, source) and derived metrics (response time, contact rate, booking rate, lead decay).
5. **Leads Metrics Dashboard Panel**: Display key metrics inside the Leads tab.

## Implementation Guardrails

1. No sending emails.
2. No draft creation.
3. Routing logic and fingerprint merge remain untouched.
4. Must remain in Stage 1 routing-only.

## Completion Criteria Before Stage 2

1. SLA breach alerts verified.
2. Response time metrics verified.
3. At least 3 real leads worked through the workbench.
4. Cross-provider merges verified stable.
5. No duplicate actions in 72 hours.

## Strategic Note

Right now, your system detects leads, normalizes them, dedupes across providers, routes with SLA, and audits routing. Stage 1.4 + 1.5 will turn it into an execution-tracked, performance-measured, discipline-enforced, and conversion-aware system. Then Stage 2 becomes a revenue multiplier — not a liability.
