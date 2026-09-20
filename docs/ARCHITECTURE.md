# HEADROOM architecture

## Product boundary

HEADROOM is a preventive SLA admission and enforcement protocol. It uses the same frozen service covenant twice:

1. **before risk exists**, to prevent unsafe new SLA promises and unsafe operational changes; and
2. **after prevention fails**, to establish incident facts and settle reserved service-credit liability.

The provider is not trusted to admit its own workload, approve its own maintenance exception or adjudicate its own outage. The customer is not trusted to create liability with an asserted metric. GenLayer sits between those incentives.

## System state machine

```text
provider bonds covenant
        ↓
ACTIVE COVENANT
        │
        ├── reservation request
        │      ↓
        │ deterministic capacity + liability precheck
        │      ├─ DENIED_DETERMINISTIC
        │      └─ live admission consensus
        │             ├─ UNSAFE / INCONCLUSIVE / SOURCE_UNAVAILABLE
        │             └─ SAFE → reserve units + reserve liability → ACTIVE SLA
        │
        ├── operational change
        │      ↓
        │ deterministic notice + duration gate
        │      └─ public semantic change preflight → PERMITTED / NOT_PERMITTED
        │
        └── active SLA incident
               ↓
          claimed miss + independent measurement packet
               ↓
          measurement consensus
               ├─ reject / bounded unavailable retry
               └─ verified miss
                      ↓ provider exception window
                 frozen exception claim
                      ↓
                 incident examiner consensus
                      ↓
                 deterministic liability gate
                      ↓
                 symmetric bonded challenge
                      ↓
                 deterministic GEN settlement
```

## Formation prevention: deterministic headroom

A request with impossible capacity or collateral is recorded as `DENIED_DETERMINISTIC`, increments prevention metrics, and cannot be reviewed. Only requests passing both mechanical gates reach semantic admission. The same checks run again immediately before SAFE activation to close races:

```text
reserved_units + requested_units <= capacity_ceiling * (1 - minimum_headroom)
reserved_liability + requested_credit <= remaining provider bond
```

This prevents capacity overbooking and under-collateralized promises before an LLM is called.

## Formation prevention: live semantic admission

A covenant freezes its bounded origin/class registry and 2..8 admission sources. Each submitted source must match an authorized origin and class. The packet must contain at least two distinct origins and source classes, an `INDEPENDENT_PROBE`, and at least one provider/capacity-class source. Provider-controlled service/status/capacity origins cannot be registered as independent probes. Later evidence URLs may use new paths under a frozen origin; redirects are not claimed as verified because GenLayer does not expose redirect destinations.

`review_reservation()` independently re-fetches those sources and validators reproduce:

- `risk_state`
- service health
- dependency health
- active-incident flag
- maintenance-conflict flag
- whether current evidence supports the declared operating envelope
- final `SAFE` / `UNSAFE` / non-decision result

`SAFE` is structurally impossible if the risk state is red, service/dependencies are unhealthy, an active incident or maintenance conflict exists, or capacity evidence does not support the promise. Immediately before reserving capacity/liability, deterministic headroom is checked again to close admission races.

## Change prevention

A provider change first passes deterministic notice-duration rules. `review_change()` then re-fetches the public change evidence and validators independently reproduce:

- scope matches;
- notice evidence matches the claimed notice time;
- approved window matches;
- active SLAs remain protected;
- dependency risk is acceptable.

`PERMITTED` is allowed only if every field is true. A frozen exception that requires a change permit cannot later rely on an unpermitted change.

## Incident measurement gate

A customer can submit a claimed miss only inside its active reservation window. The measurement packet must use at least two distinct origins and authorized source classes, including a registered independent probe. `verify_incident_measurement()` independently establishes the exact service/window and measured availability.

A customer assertion therefore cannot create provider liability by itself:

- `NOT_PROVEN` or a measurement meeting the target clears the incident;
- unavailable sources enter a bounded retry and may be dismissed without liability;
- only an independently `VERIFIED` miss starts the provider exception response clock.

## Incident semantic adjudication

The provider may invoke only a frozen exception. `examine_incident()` combines the independently verified measurement evidence with the exception evidence and asks validators to reproduce a structured factual/legal-protocol record:

- bounded impact start/end and exception-event start/end timestamps;
- service affected;
- exception event established;
- causal link supported;
- **frozen clause rule satisfied**;
- required change permit matches;
- material source conflict.

The validator compares those outcome-bearing fields, not free-form prose.

## Deterministic liability gate

HEADROOM deliberately does **not** let a second LLM invent a payout percentage. Once the incident examiner has established the semantic facts, `judge_liability()` applies the frozen protocol rule mechanically.

If there is source conflict, no service impact, no established exception event, no supported causation, the clause rule is not satisfied, or a required permit is missing, the exception gets zero excused share and provider liability is `10000` bps.

Otherwise, contract code intersects the validated impact and exception intervals with the frozen observation window, divides the resulting overlap duration by the frozen measured impact duration, clamps the result to 0..10000 basis points, and derives provider liability as `10000 - excused_bps`. The semantic model supplies timestamps and factual predicates; it never supplies an economic percentage.

That produces `EXCUSED`, `PARTIAL` or `LIABLE` deterministically.

## Symmetric challenge

Either provider or customer may challenge the pending allocation with a bond and public counter-evidence. Upheld challenges revise the allocation and return the challenger bond. Rejected challenges transfer the bond to the opposing party. Unavailable/inconclusive challenges expire after a bounded resolution window, refunding the challenger and allowing the original allocation to finalize.

## Settlement / collateral conservation

Every admitted reservation reserves its maximum service credit against the provider's current bond balance. Settlement can never exceed the reserved credit. Finalization releases the reservation's capacity and reserved liability and debits any customer payout from the covenant bond.

```text
total_deposited == covenant_escrow + challenge_escrow + claimable + withdrawn
```

A provider can close the covenant and recover its remaining bond only when there are no active reservations and no reserved liability.

## Frontend boundary

HEADROOM is the flagship UI: a promise-surface control room rather than a generic dashboard. Capacity and liability gauges explain prevention; change-control panels explain permitted operations; incident timelines explain exactly which semantic facts GenLayer established. Wallet integration is generic injected EIP-1193 only, finalized reads are explicit, and finalized-but-failed executions are treated as errors.
