# HEADROOM security notes

## Security model

HEADROOM uses prevention before adjudication. Deterministic capacity/collateral rules and live GenLayer admission consensus decide whether a new SLA-backed promise can be formed. Change preflight restricts which operational changes can later qualify for protection. If prevention still fails, independent measurement consensus proves the miss, incident consensus establishes causal facts, and contract code derives liability and settlement.

## Critical invariants

1. Studionet `61999` / `https://studio.genlayer.com/api` is the only release target.
2. Requests failing deterministic capacity or collateral checks are auditable `DENIED_DETERMINISTIC` records; they never reach semantic review or reserve resources. Provider collateral must cover every activated maximum service credit.
3. Eligible capacity headroom is checked again immediately before SAFE activation to close admission races; pending requests hold no resources.
4. Covenant evidence origins and classes are frozen at creation. Every consequential submitted URL must match its authorized HTTPS origin and declared class; provider-controlled origins cannot masquerade as independent probes. Distinct-source rules still apply. Redirect destinations are not observable and are not claimed.
5. `SAFE` is structurally invalid if service/dependencies are unhealthy, an incident/maintenance conflict exists, risk is red, or capacity evidence does not support the promise.
6. A customer-typed metric cannot create liability; a miss must pass independent multi-source measurement consensus.
7. Provider exceptions are frozen in the covenant. Any exception requiring a change permit must reference a valid preflighted change.
8. Incident consensus establishes facts; `judge_liability()` applies the liability rule deterministically. The model does not invent payout percentage or GEN amount.
9. Provider silence/unresolved exception evidence after a verified miss cannot strand reserved liability forever; bounded default paths exist.
10. Challenge is symmetric, bonded and bounded.
11. Covenant closure is impossible while active reservations/reserved liability remain.
12. `total_deposited == covenant_escrow + challenge_escrow + claimable + withdrawn` must remain true.

## Adversarial surfaces

- **Provider overbooks capacity:** deterministic headroom gate stores `DENIED_DETERMINISTIC`; review cannot reach it and no resources are reserved.
- **Provider sells more liability than its bond:** reserved maximum credits cannot exceed bond headroom.
- **Provider self-reports healthy service:** admission requires frozen origin/class authorization, distinct evidence origins, an independent probe and a provider/capacity source; validators independently re-fetch/reason.
- **Unsafe maintenance tries to become an exception:** deterministic notice/duration rules plus semantic change preflight create a permit; permit-required clauses cannot rely on an unpermitted change.
- **Customer fabricates an outage:** measurement consensus must establish exact service/window/measured availability first.
- **Provider blames an overlapping upstream incident without causation:** examiner separately establishes event, causation, clause satisfaction, permit match, source conflict and causal overlap.
- **LLM chooses a convenient payout:** impossible in normal settlement; liability bps are derived from structured facts by contract code, then applied to reserved credit deterministically.
- **Liveness griefing:** provider-response, evidence-retry and challenge-resolution deadlines provide bounded exits.

## Live proof status

The canonical contract deployment and source/schema match are verified; the deployed starting state has no covenants or lifecycle transactions. Real covenant, prevention, admission, change preflight, and incident settlement actions require user-approved wallet transactions and truthful evidence. Do not claim any until its transaction is finalized with successful execution and post-state is re-read. See `docs/REVIEW_EVIDENCE.md` for the chronological record.

Frontend validation is a convenience boundary, not authority. The contract remains authoritative for origin/class policy, timing, headroom, collateral, state transitions and accounting. Human source and exception builders serialize to the existing contract arguments without changing its trust model.
