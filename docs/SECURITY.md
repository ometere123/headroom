# HEADROOM security notes

## Security model

HEADROOM uses prevention before adjudication. Deterministic capacity/collateral rules and live GenLayer admission consensus decide whether a new SLA-backed promise can be formed. Change preflight restricts which operational changes can later qualify for protection. If prevention still fails, independent measurement consensus proves the miss, incident consensus establishes causal facts, and contract code derives liability and settlement.

## Critical invariants

1. Studionet `61999` / `https://studio.genlayer.com/api` is the only release target.
2. Provider collateral must cover every reserved maximum service credit; new reservations cannot create under-collateralized liability.
3. Capacity headroom is checked before semantic admission and checked again immediately before reservation to close admission races.
4. `SAFE` is structurally invalid if service/dependencies are unhealthy, an incident/maintenance conflict exists, risk is red, or capacity evidence does not support the promise.
5. A customer-typed metric cannot create liability; a miss must pass independent multi-source measurement consensus.
6. Provider exceptions are frozen in the covenant. Any exception requiring a change permit must reference a valid preflighted change.
7. Incident consensus establishes facts; `judge_liability()` applies the liability rule deterministically. The model does not invent payout percentage or GEN amount.
8. Provider silence/unresolved exception evidence after a verified miss cannot strand reserved liability forever; bounded default paths exist.
9. Challenge is symmetric, bonded and bounded.
10. Covenant closure is impossible while active reservations/reserved liability remain.
11. `total_deposited == covenant_escrow + challenge_escrow + claimable + withdrawn` must remain true.

## Adversarial surfaces

- **Provider overbooks capacity:** deterministic headroom gate blocks the request before semantic review.
- **Provider sells more liability than its bond:** reserved maximum credits cannot exceed bond headroom.
- **Provider self-reports healthy service:** admission requires multiple source families including an independent probe and a provider/capacity source; validators independently re-fetch/reason.
- **Unsafe maintenance tries to become an exception:** deterministic notice/duration rules plus semantic change preflight create a permit; permit-required clauses cannot rely on an unpermitted change.
- **Customer fabricates an outage:** measurement consensus must establish exact service/window/measured availability first.
- **Provider blames an overlapping upstream incident without causation:** examiner separately establishes event, causation, clause satisfaction, permit match, source conflict and causal overlap.
- **LLM chooses a convenient payout:** impossible in normal settlement; liability bps are derived from structured facts by contract code, then applied to reserved credit deterministically.
- **Liveness griefing:** provider-response, evidence-retry and challenge-resolution deadlines provide bounded exits.

## Release proof still required

The canonical demo should visibly prove both halves of the protocol: one prevented promise/change and one admitted promise that later enters verified incident adjudication and deterministic GEN settlement. Record `get_stats()` after the flow and keep the accounting invariant true.
