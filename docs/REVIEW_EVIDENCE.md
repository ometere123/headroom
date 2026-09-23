# HEADROOM Review Evidence

## Canonical network and contract

| Field | Verified value |
| --- | --- |
| Network | GenLayer Studionet |
| Chain ID | `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Explorer | [explorer-studio.genlayer.com](https://explorer-studio.genlayer.com) |
| Contract | [`0x44f03156B27d92e9527992744207ca73d0E6F980`](https://explorer-studio.genlayer.com/address/0x44f03156B27d92e9527992744207ca73d0E6F980) |
| Deployment transaction | [`0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b`](https://explorer-studio.genlayer.com/tx/0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b) |
| Deployment status | FINALIZED; execution SUCCESS; 5 AGREE |
| Contract source | Corrected trust-boundary implementation in `contracts/headroom.py` |
| Deployed source SHA-256 | `FD652486B69C65DB6B7AACEF736BFF84C5A9E8456C946B117B95D13CD6FA5D11` |
| Source match | Deployment record corresponds to the corrected local source candidate |
| Schema | 31 methods: 10 views and 21 writes |
| CLI | GenLayer CLI 0.39.1; network config Studionet / 61999 / stable RPC |
| Frontend | [https://the-headroom.vercel.app/](https://the-headroom.vercel.app/) |

The deployment record identifies the previously deployed requester-boundary source. The current release candidate adds an immutable contract-level `INDEPENDENT_PROBE` authority allowlist containing `stats.uptimerobot.com`; the provider cannot extend it through its registry. Custom provider domains and CNAME aliases do not qualify because the parsed origin must match exactly. The existing canonical deployment predates this correction, so the new authority rule is not claimed as live until redeployment. This is an explicit contract policy, not DNS/WHOIS ownership verification.

## Deployed `get_stats()`

The verified initial deployed response is:

```json
{
  "version": "0.1.0-studionet",
  "network": "Studionet",
  "chain_id": 61999,
  "rpc": "https://studio.genlayer.com/api",
  "covenants": 0,
  "reservations": 0,
  "changes": 0,
  "incidents": 0,
  "admissions": 0,
  "prevented": 0,
  "settlements": 0,
  "covenant_escrow": "0",
  "challenge_escrow": "0",
  "claimable": "0",
  "withdrawn": "0",
  "accounting_balanced": true,
  "admin_controls": false
}
```

## Toolchain and release checks

Record final candidate evidence here after checks run on the pushed release commit:

| Check | Result |
| --- | --- |
| Python | 3.12.14 (GitHub Actions) |
| Direct Mode | `genlayer-test==0.29.2`, `genlayer-py==0.16.3`; 60 tests collected, final pass count pending authority-fix CI |
| GenVM lint | `genvm-linter==0.11.1rc2`; validation must pass; exact reviewed seven E010 warnings only |
| `py_compile` | record result |
| `check_release.py` | record result |
| `check_contract_patterns.py` | record result |
| `check_frontend_surface.py` | record result |
| Frontend SDK | exact `genlayer-js==1.1.8` |
| Frontend typecheck/build | record result |
| GitHub Actions | Final green authority-fix run will be recorded after CI completes |
| Vercel | existing project `headroom`, Production domain `the-headroom.vercel.app`; record deployment ID/result |

## Chronological live transaction evidence

Only the deployment transaction exists at the time this evidence was written. Empty lifecycle cells are intentionally marked NOT EXECUTED; they are not simulated or inferred. Update rows with transaction hashes only after user-approved wallet operations finalize and execute successfully.

| Action | Method | Transaction | Finalized? | Execution success? | Result | Evidence / state |
| --- | --- | --- | --- | --- | --- | --- |
| Deploy canonical Headroom | Deployment | [`0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b`](https://explorer-studio.genlayer.com/tx/0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b) | Yes | Yes | Contract created at canonical address | [Contract explorer](https://explorer-studio.genlayer.com/address/0x44f03156B27d92e9527992744207ca73d0E6F980); source hash above |
| Create/bond covenant | `create_covenant` | NOT EXECUTED | — | — | Awaiting user wallet approval | No covenant exists in initial deployed state |
| Deterministic prevention | `request_reservation` | NOT EXECUTED | — | — | Not yet demonstrated live | Must inspect post-state and `prevented` count |
| Semantic prevention | `review_reservation` | NOT EXECUTED | — | — | Not yet demonstrated live | Requires truthful, currently unsafe evidence |
| SAFE admission | `request_reservation` + `review_reservation` | NOT EXECUTED | — | — | Not yet demonstrated live | Must record actual reservation and frozen evidence |
| Change preflight | `propose_change` + `review_change` | NOT EXECUTED | — | — | Not yet demonstrated live | Permit must precede its window |
| Incident opening | `open_incident` | NOT EXECUTED | — | — | No qualifying miss documented | Never infer from user-entered metric |
| Measurement verification | `verify_incident_measurement` | NOT EXECUTED | — | — | Not yet demonstrated live | Needs an actual measured miss in an active window |
| Frozen exception | `claim_exception` | NOT EXECUTED | — | — | Not yet demonstrated live | Requires frozen rule and authorized evidence |
| Incident examination | `examine_incident` | NOT EXECUTED | — | — | Not yet demonstrated live | GenLayer facts only; contract determines money |
| Deterministic liability | `judge_liability` | NOT EXECUTED | — | — | Not yet demonstrated live | Calculated from consensus facts |
| Challenge | `challenge_liability` + `resolve_challenge` | NOT EXECUTED | — | — | No truthful counter-evidence submitted | Do not manufacture disagreement |
| Settlement | `finalize_incident` | NOT EXECUTED | — | — | Not yet demonstrated live | Needs legitimate completed incident path |
| Withdrawal | `withdraw_credit` | NOT EXECUTED | — | — | No credit to withdraw in initial state | Await user wallet approval if credit later exists |

## Evidence source research

Research retrieved the GitHub public status API (`https://www.githubstatus.com/api/v2/summary.json`) at 2026-09-21 19:18:58 UTC. It reported all listed components operational, no incidents or scheduled maintenance. Checkly’s public GitHub monitor (`https://www.checklyhq.com/availability/github/`) reported GitHub up when crawled five days earlier and its page describes its own two-region 10-minute HTTPS probe of `https://api.github.com`; the observations are not the same-time window, so it is only a candidate independent source. The two operators and origins are distinct. These sources have **not** been submitted to the contract or represented as evidence of a live decision. Their current health evidence does not support a truthful semantic UNSAFE test or an incident claim, and their use to promise service operated by someone else would be inappropriate. Select a service actually operated by the provider and recheck freshness before any wallet transaction.

No controlled outage, fabricated status page, edited evidence timestamp, or historical outage reused for a new reservation is claimed.
