---
id: architecture-design/modularity
title: Modularity
band: B4
track: architecture-design
tier: T2
bloom_target: apply
prerequisites: [programming/programming-paradigms]
related: [architecture-design/design-patterns, architecture-design/architectural-styles]
recommended: [architecture-design/design-patterns]
status: published
schema-version: 1
owner: l1-modularity
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0018, S-0137, S-0138, S-0139, S-0144]
---

# Modularity — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — decompose a described system into modules that hide likely changes, and justify each boundary with Parnas's criteria ([S-0137]).
- **apply** — classify a given design's coupling and cohesion and propose a re-decomposition ([S-0017]).
- **apply** — invert a concrete dependency (introduce an interface + injection point) so policy does not depend on details ([S-0144]).
- **apply** — locate or introduce a seam in a legacy code sample and explain its enabling point ([S-0139]).
- **analyze** — explain why the same system decomposed two ways has different changeability (KWIC-style comparison) ([S-0137]).
- **evaluate** — judge a proposed module boundary against Conway's law and SOLID, and say where the boundary is likely to break ([S-0138], [S-0144]).

## Worked example 1 — two decompositions of a reporting system

System: fetch orders from a database, compute order totals, render a report (HTML today, PDF planned), send it by email (SMTP today, HTTP API planned).

**Decomposition A — by processing steps:** `FetchOrders` → `ComputeTotals` → `RenderReport` → `SendReport`, each calling the next. Trace three changes: (1) orders move from SQL to a REST API — only `FetchOrders` changes, good; (2) a new output format PDF arrives — `RenderReport` changes, but `SendReport` also changes (it attaches an HTML file), and `ComputeTotals` must pass the format through; (3) SMS delivery arrives — `SendReport` and `FetchOrders`... the change ripples. Each decision (storage, format, transport) is spread across several modules.

**Decomposition B — by design decisions (information hiding):** `OrderSource` (interface; hides storage choice), `TotalsEngine` (hides pricing/total algorithm), `ReportRenderer` (interface; hides format), `DeliveryChannel` (interface; hides transport). Now: (1) SQL→REST touches only `OrderSource`; (2) PDF touches only a new `PdfRenderer`; (3) SMS touches only a new `SmsChannel`. Every likely change is confined to one module — the Parnas criterion ([S-0137]).

## Worked example 2 — inverting a dependency

Before: `BillingService → PayPalClient` (concrete class). Change "add Stripe" means editing `BillingService`. After: `BillingService → PaymentGateway (interface) ← StripeClient / PayPalClient`. The arrow from `BillingService` now points at an abstraction; both providers depend on the same interface. `BillingService` is closed for modification, open for extension ([S-0144]). Cost: one interface and an injection point — the indirection is the price of the policy's stability.

## Elaboration prompts

- Why does Parnas's criterion ("list difficult design decisions") give a different module structure than "list processing steps"? What kinds of changes does each structure favor?
- Where exactly does Conway's law show up in a codebase you know — which module boundary tracks which team boundary?
- Why is "high cohesion AND low coupling" a balance rather than two independent targets? Give a case where raising cohesion raises coupling.
- When is a seam the right tool, and when is introducing one just extra indirection? (Compare: stable, rarely changing module vs. known variation point.)

## Common misconceptions

- "More modules = more modular": modularity is about what each module hides and whether changes stay confined, not about module count (Parnas's criteria list, [S-0137]).
- "Information hiding = private fields": private is an enforcement mechanism; the design decision is keeping format/algorithm/policy out of the interface ([S-0137]).
- "SOLID is law": SOLID is context-dependent heuristic advice; rigid application over-engineers designs ([S-0144]).
- "Decoupling is free / less coupling is always better": decoupling costs indirection, and SWEBOK evaluates coupling together with cohesion and complexity ([S-0017]).
- "Conway's law prescribes team structure": it describes a constraint; prescriptive use is a separate organizational strategy ([S-0138]).

## Feynman targets

- Explain to a non-programmer why two teams that never talk produce software whose parts are glued together.
- Explain why "the module hides the fact that prices now come in euros" is a design statement, not a coding style.
- Explain how you could change a program's behavior without editing the place where the behavior is written.

## Interleaving hooks

- **programming/programming-paradigms**: encapsulation is a modularity mechanism that OOP implements via classes and modules implement without classes — revisit the paradigm claims while designing boundaries.
- **architecture-design/design-patterns**: GRASP re-uses Low Coupling and High Cohesion as responsibility-assignment principles; patterns (Adapter, Observer) are vehicles for the dependency rules above — continue there.
- **architecture-design/architectural-styles**: layered and hexagonal styles are module-boundary policies at system scale — connect this pack's seam concept to style-level port/adapter boundaries.
