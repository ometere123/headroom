<p align="center">
  <img src="branding/headroom-logo.svg" alt="HEADROOM" width="300" />
</p>

# HEADROOM — Preventive SLA Admission & Enforcement

**Don’t promise what you can’t serve.** HEADROOM controls whether SLA-backed service commitments and operational exceptions may exist before risk is taken. If prevention fails, the same frozen covenant governs incident facts and deterministic settlement.

**Live app:** [the-headroom.vercel.app](https://the-headroom.vercel.app/) · **Protocol:** [Studionet explorer](https://explorer-studio.genlayer.com/address/0x44f03156B27d92e9527992744207ca73d0E6F980)

## What HEADROOM Does

A provider bonds a service covenant that freezes capacity, liability, evidence origins and classes, maintenance rules, and exception clauses. A customer requests a bounded SLA reservation. Mechanical headroom checks reject requests the provider cannot safely serve or collateralize. Only feasible requests reach GenLayer semantic admission against current public evidence. Operational changes must also pass preflight before their window begins.

If a service miss occurs, a customer’s typed metric cannot create liability by itself. Independent evidence must establish the miss. The provider may invoke only an exception frozen in the covenant. GenLayer reconstructs consequential facts and causation; contract code applies the frozen rule to those facts and settles native GEN from reserved liability.

## Why It Exists

The parties have conflicting incentives. Providers control capacity claims, maintenance notices, status evidence, and exception interpretation. Customers control complaints, claimed impact, and counter-evidence. Neither side should decide alone whether a new promise is safe or whether an incident is excused. HEADROOM assigns semantic evidence judgments to GenLayer validators and keeps arithmetic and accounting in contract code.

## Core Invariant

> **Consensus Before Risk. Consensus After Failure.**

Before risk, consensus reviews admission evidence and operational change preflight after deterministic timing, capacity, and collateral gates. After a measured failure, consensus verifies the evidence, reconstructs incident facts, and checks the frozen exception. Deterministic contract logic then calculates liability, settlement, and withdrawal accounting.

## Protocol Lifecycle

| Human stage | Contract method | What happens |
| --- | --- | --- |
| Bond covenant | `create_covenant` | Freeze capacity, evidence policy, exception rules, and bond |
| Request capacity | `request_reservation` | Deterministic headroom gate; denied requests reserve nothing |
| Live admission | `review_reservation` | GenLayer checks changing service/dependency evidence; SAFE activation rechecks headroom |
| Change preflight | `propose_change` / `review_change` | Verify notice, duration, evidence, and active SLA protection before start |
| Open measured incident | `open_incident` / `verify_incident_measurement` | Independently verify service, interval, and measured availability |
| Claim frozen exception | `claim_exception` / `examine_incident` | Reconstruct facts, causation, clause satisfaction, and permit match |
| Apply liability | `judge_liability` | Deterministic overlap, liable basis points, and payout |
| Challenge | `challenge_liability` / `resolve_challenge` | Re-fetch complete case, include counter-evidence, apply the same economic law |
| Finalize | `finalize_incident` | Release capacity/reserve and write settlement certificate |
| Withdraw | `withdraw_credit` | Owner-directed native GEN transfer |

## What Is Deterministic, What Uses Consensus

| Decision | Mechanism |
| --- | --- |
| Capacity headroom and reservation counters | Deterministic contract arithmetic |
| Bond/collateral and challenge bond | Deterministic contract arithmetic |
| Reservation lead time, expiry, notice, duration, and permit timing | Deterministic comparisons |
| Current service, dependency, risk, and evidence meaning | GenLayer consensus |
| Whether change evidence matches the claimed maintenance window | GenLayer consensus plus deterministic timing gates |
| Whether independent measurement establishes the service miss | GenLayer consensus |
| Incident timeline, exception event, causal relationship, and clause facts | GenLayer consensus |
| Temporal overlap, `excused_bps`, and `liable_bps` | Deterministic contract arithmetic |
| GEN payout, escrow conservation, and settlement certificate | Deterministic contract arithmetic |

GenLayer establishes facts from changing public evidence. It does not choose a payout amount or liability percentage.

## Evidence Trust Model

Covenant formation freezes HTTPS origin/class pairs. Later evidence may use paths under an authorized origin; each submitted URL must match both its actual parsed origin and claimed class. Required source families use distinct origins. A service/provider-controlled origin cannot claim `INDEPENDENT_PROBE`, and duplicate origins cannot count as independent sources. The current GenLayer web runtime does not expose final redirect destinations, so HEADROOM makes no claim that redirected content’s origin was verified.

Admission, measurement, change, exception, and challenge packets all use the frozen policy. The UI creates contract JSON from structured source rows; reviewers can inspect serialized payloads without typing raw JSON.

## Liability and Challenge

GenLayer establishes bounded impact and exception timestamps and factual predicates such as service affected, event established, causation, clause satisfaction, permit match, and source conflict. The contract intersects the established intervals and calculates proven excused overlap against the measured impact duration. It derives provider liability as `10,000 - excused_bps` when every frozen exception condition holds; otherwise the exception receives no excused share. Payout is derived from the reserved maximum credit and liability basis points.

A bonded challenge submits counter-evidence and re-fetches the original measurement, exception, and required permit evidence. If upheld, corrected factual fields pass through the same deterministic liability function. Bounded inconclusive/unavailable states cannot silently become a favorable decision.

## Live Release

| Field | Canonical value |
| --- | --- |
| Network | GenLayer Studionet |
| Chain ID | `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Explorer | [explorer-studio.genlayer.com](https://explorer-studio.genlayer.com) |
| Contract | [`0x44f03156B27d92e9527992744207ca73d0E6F980`](https://explorer-studio.genlayer.com/address/0x44f03156B27d92e9527992744207ca73d0E6F980) |
| Deployment transaction | [`0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b`](https://explorer-studio.genlayer.com/tx/0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b) |
| Contract source | Corrected trust-boundary implementation in `contracts/headroom.py` |
| Contract source SHA-256 | `FD652486B69C65DB6B7AACEF736BFF84C5A9E8456C946B117B95D13CD6FA5D11` |
| Frontend | [the-headroom.vercel.app](https://the-headroom.vercel.app/) |

Deployment receipt is FINALIZED with successful execution. The deployed source corresponds to the corrected trust-boundary implementation in `contracts/headroom.py`; the deployed schema exposes 31 methods (10 views and 21 writes). `get_stats()` reports Studionet / 61999, balanced accounting, and no admin controls. See [review evidence](docs/REVIEW_EVIDENCE.md) for the verified receipt and state. Live semantic admission and economic lifecycle evidence are recorded only after those actions have occurred.

## Run Locally

Requirements: Python 3.12.x, Node.js supported by the locked Next.js version, and npm.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest tests/direct/ -v
cd frontend
npm install
$env:NEXT_PUBLIC_HEADROOM_CONTRACT="0x44f03156B27d92e9527992744207ca73d0E6F980"
$env:NEXT_PUBLIC_GENLAYER_CHAIN_ID="61999"
$env:NEXT_PUBLIC_GENLAYER_RPC_URL="https://studio.genlayer.com/api"
$env:NEXT_PUBLIC_GENLAYER_EXPLORER="https://explorer-studio.genlayer.com"
npm run dev
```

The frontend uses `genlayer-js` **1.1.8** and generic injected EIP-1193 (`window.ethereum`). It does not use a backend signer, private-key browser wallet, WalletConnect, Privy, or Snaps. Connect a wallet and switch to GenLayer Studionet before signing. Public reads can be explored without signing.

## Verification

```powershell
python -m py_compile contracts/headroom.py tests/direct/*.py tests/integration/*.py
python scripts/check_genvm_lint.py
pytest tests/direct/ -v
python scripts/check_release.py
python scripts/check_contract_patterns.py
python scripts/check_frontend_surface.py
cd frontend
npm install
npm run typecheck
npm run build
```

The pinned `genvm-linter==0.11.1rc2` validation gate permits only the reviewed seven E010 custom validator reachability diagnostics; new diagnostics fail CI. Direct Mode uses `genlayer-test==0.29.2` and `genlayer-py==0.16.3`. Release results, CI, real transactions, and any uncompleted live proof are maintained in [docs/REVIEW_EVIDENCE.md](docs/REVIEW_EVIDENCE.md).

## Repository Map

- `contracts/` — single substantial GenLayer Intelligent Contract
- `frontend/` — Next.js App Router control room, structured evidence forms, injected wallet
- `tests/direct/` — deterministic and adversarial Direct Mode coverage
- `tests/integration/` — opt-in live Studionet read/smoke checks
- `deploy/` — stable Studionet deployment tooling
- `docs/` — architecture, security, live-demo and reviewer evidence
- `branding/` — reusable HEADROOM brand assets
- `scripts/` — source checks and pinned lint/release gates

## License

MIT. See [LICENSE](LICENSE).
