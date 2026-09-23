# HEADROOM Review Evidence

## Canonical network and contract

| Field | Verified value |
| --- | --- |
| Network | GenLayer Studionet |
| Chain ID | `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Explorer | [explorer-studio.genlayer.com](https://explorer-studio.genlayer.com) |
| Contract | [`0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2`](https://explorer-studio.genlayer.com/address/0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2) |
| Deployment transaction | [`0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8`](https://explorer-studio.genlayer.com/tx/0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8) |
| Deployment status | FINALIZED; execution SUCCESS / return |
| Contract source | Corrected trust-boundary implementation in `contracts/headroom.py` |
| Deployed source commit | `d204e08cbe4753d80a865d34fc5f185e0d6083ed` |
| Deployed source SHA-256 | `0AB5E90F00286962ED9FC727D97288A61EDAAE59DB55334D531F89B68BDE1565` |
| Source match | Deployment record corresponds to the corrected local source candidate |
| Schema | 31 methods: 10 views and 21 writes |
| CLI | GenLayer CLI 0.39.1; network config Studionet / 61999 / stable RPC |
| Frontend | [https://the-headroom.vercel.app/](https://the-headroom.vercel.app/) |

Reservation activation requires provider authorization or meaningful requester stake before provider capacity/collateral can be locked. `INDEPENDENT_PROBE` uses the immutable contract-level authority `stats.uptimerobot.com`; provider registries cannot extend it. Custom provider domains/CNAME aliases do not qualify, same-registrable-domain rejection remains defense in depth, and no DNS/WHOIS verification is claimed.

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
| Direct Mode | `genlayer-test==0.29.2`, `genlayer-py==0.16.3`; 60 passed |
| GenVM lint | `genvm-linter==0.11.1rc2`; validation must pass; exact reviewed seven E010 warnings only |
| `py_compile` | PASS |
| `check_release.py` | PASS |
| `check_contract_patterns.py` | PASS |
| `check_frontend_surface.py` | PASS |
| Frontend SDK | exact `genlayer-js==1.1.8` |
| Frontend typecheck/build | PASS |
| GitHub Actions | [run 35908341602](https://github.com/ometere123/headroom/actions/runs/35908341602), green on commit `d204e08cbe4753d80a865d34fc5f185e0d6083ed` |
| Vercel | existing project `headroom`, Production domain `the-headroom.vercel.app`; record deployment ID/result |

## Chronological live transaction evidence

Only the deployment transaction exists at the time this evidence was written. Empty lifecycle cells are intentionally marked NOT EXECUTED; they are not simulated or inferred. Update rows with transaction hashes only after user-approved wallet operations finalize and execute successfully.

| Action | Method | Transaction | Finalized? | Execution success? | Result | Evidence / state |
| --- | --- | --- | --- | --- | --- | --- |
| Deploy corrected Headroom | Deployment | [`0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8`](https://explorer-studio.genlayer.com/tx/0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8) | Yes | Yes | Contract created at canonical address | [Contract explorer](https://explorer-studio.genlayer.com/address/0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2); source commit and hash above |
| Previous deployment (SUPERSEDED) | Deployment | `0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b` | Yes | Yes | Historical requester-boundary deployment only | Superseded by corrected deployment above; not evidence for current authority policy |
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
