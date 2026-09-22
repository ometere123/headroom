# HEADROOM Review Evidence

## Canonical network and contract

| Field | Verified value |
| --- | --- |
| Network | GenLayer Studionet |
| Chain ID | `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Explorer | [explorer-studio.genlayer.com](https://explorer-studio.genlayer.com) |
| Contract | [`0x235Fd204E6d78e61055a6BD24B06319aA503D2f1`](https://explorer-studio.genlayer.com/address/0x235Fd204E6d78e61055a6BD24B06319aA503D2f1) |
| Deployment transaction | [`0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`](https://explorer-studio.genlayer.com/tx/0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e) |
| Deployment status | FINALIZED; execution SUCCESS; 3 AGREE, 2 IDLE |
| Contract source commit | `add2f35d08cde554bec6d9bed98c5094554035d9` |
| Frontend implementation commit | `f6b9cf5c57348c956c4a559ab12e7ecb6aca8aa7` |
| Final release HEAD | `3f0d05c062da40d7df9828bcafe89670988e7f3` |
| Deployed source SHA-256 | `a61cb6815251ac3f118fb73fe81c9e10b7575c13ab3135e7664ebcdd9b587dbd` |
| Source match | Retrieved deployed source equals `contracts/headroom.py` at the source commit byte for byte |
| Schema | 31 methods: 10 views and 21 writes |
| CLI | GenLayer CLI 0.39.1; network config Studionet / 61999 / stable RPC |
| Frontend | [https://the-headroom.vercel.app/](https://the-headroom.vercel.app/) |

The source commit above identifies the deployed contract source. Later frontend and documentation commits do not change the contract and do not require redeployment.

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

Release evidence for the current candidate is recorded below. Re-run checks after any source change.

| Check | Result |
| --- | --- |
| Python | 3.12.3 |
| Direct Mode | `genlayer-test==0.29.2`, `genlayer-py==0.16.3`; 57 passed |
| GenVM lint | `genvm-linter==0.11.1rc2`; validation passed, 31 methods; wrapper PASS, exact seven reviewed E010 lint diagnostics only (validation also notes I200: a newer runner is available) |
| `py_compile` | PASS for contract, direct tests, integration tests |
| `check_release.py` | PASS; Studionet 61999 stable RPC |
| `check_contract_patterns.py` | PASS |
| `check_frontend_surface.py` | PASS; 6 required route patterns and 13 protocol actions checked |
| Frontend SDK | exact `genlayer-js==1.1.8` |
| Frontend typecheck/build | PASS; Next.js production build generated all routes |
| GitHub Actions | PASS, [run 35695176784](https://github.com/ometere123/headroom/actions/runs/35695176784), commit `add2f35d08cde554bec6d9bed98c5094554035d9` |
| Vercel | existing project `headroom`, root `frontend`; four Production variables configured; deployment READY at [production URL](https://the-headroom.vercel.app/); `/` and `/control` return HTTP 200 |
| Browser walkthrough | Production home and operational routes loaded; live contract reads, wallet connection and UTC preference exercised; no write transaction submitted |

## Chronological live transaction evidence

The deployment transaction and the user-approved covenant transaction below are recorded from Studionet. The covenant write finalized and executed successfully on-chain. The original production UI briefly reported a monitoring fetch error after submission; it did not represent protocol execution failure.

| Action | Method | Transaction | Finalized? | Execution success? | Result | Evidence / state |
| --- | --- | --- | --- | --- | --- | --- |
| Deploy canonical Headroom | Deployment | [`0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`](https://explorer-studio.genlayer.com/tx/0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e) | Yes | Yes | Contract created at canonical address | [Contract explorer](https://explorer-studio.genlayer.com/address/0x235Fd204E6d78e61055a6BD24B06319aA503D2f1); source hash above |
| Create/bond covenant | `create_covenant` | [`0xa0792d197bb882b55fffc1198043854a03793c0884c75c51a2563c664c003cbc`](https://explorer-studio.genlayer.com/tx/0xa0792d197bb882b55fffc1198043854a03793c0884c75c51a2563c664c003cbc) | Yes | Yes | `hr-cv-1`; 1 GEN bonded | Consensus Accepted; GenVM SUCCESS; return value `hr-cv-1`. Original UI monitoring fetch failed after submission and was hardened in `c73962e9`. |
| Deterministic prevention | `request_reservation` | COMPLETED | `0x7cc4f80a71da8a9bd062133aa3ea97591e4c5440593dec9598f4b13285988a5d` | FINALIZED, success | `hr-r-1` DENIED_DETERMINISTIC; no reserves; prevented +1 |
| Semantic prevention | `review_reservation` | NOT EXECUTED | - | - | Not yet demonstrated live | Requires truthful, currently unsafe evidence |
| SAFE admission | `request_reservation` + `review_reservation` | COMPLETED | `0x1123d3dd64165cacf8e9121699773eebec2a8805c46a9d94d340b60df5cfaf1a` / `0xe8f0931b08139f206eb0411e01642944b8b01bbf3e200c51de82645b7dbf30ed` | FINALIZED, success | `hr-r-2` SAFE and ACTIVE; one unit; 0.10 GEN reserved |
| Change preflight | `propose_change` + `review_change` | NOT EXECUTED | - | - | Not yet demonstrated live | Permit must precede its window |
| Incident opening | `open_incident` | NOT EXECUTED | - | - | No qualifying miss documented | Never infer from user-entered metric |
| Measurement verification | `verify_incident_measurement` | NOT EXECUTED | - | - | Not yet demonstrated live | Needs an actual measured miss in an active window |
| Frozen exception | `claim_exception` | NOT EXECUTED | - | - | Not yet demonstrated live | Requires frozen rule and authorized evidence |
| Incident examination | `examine_incident` | NOT EXECUTED | - | - | Not yet demonstrated live | GenLayer facts only; contract determines money |
| Deterministic liability | `judge_liability` | NOT EXECUTED | - | - | Not yet demonstrated live | Calculated from consensus facts |
| Challenge | `challenge_liability` + `resolve_challenge` | NOT EXECUTED | - | - | No truthful counter-evidence submitted | Do not manufacture disagreement |
| Settlement | `finalize_incident` | NOT EXECUTED | - | - | Not yet demonstrated live | Needs legitimate completed incident path |
| Withdrawal | `withdraw_credit` | COMPLETED | `0xbd1dbd26c544ed3bf542b602bce8a6249af539e877b185dd431a8b7dee9ae99b` | FINALIZED, success | Historical 1 GEN withdrawal; return value `1000000000000000000` |

## Evidence source research

Research retrieved the GitHub public status API (`https://www.githubstatus.com/api/v2/summary.json`) at 2026-09-21 19:18:58 UTC. It reported all listed components operational, no incidents or scheduled maintenance. Checkly’s public GitHub monitor (`https://www.checklyhq.com/availability/github/`) reported GitHub up when crawled five days earlier and its page describes its own two-region 10-minute HTTPS probe of `https://api.github.com`; the observations are not the same-time window, so it is only a candidate independent source. The two operators and origins are distinct. These sources have **not** been submitted to the contract or represented as evidence of a live decision. Their current health evidence does not support a truthful semantic UNSAFE test or an incident claim, and their use to promise service operated by someone else would be inappropriate. Select a service actually operated by the provider and recheck freshness before any wallet transaction.

No controlled outage, fabricated status page, edited evidence timestamp, or historical outage reused for a new reservation is claimed.

## Production deployment and browser verification

The existing Vercel project (`headroom`, root directory `frontend`) has the four required Production variables configured for the canonical contract and Studionet. Production is publicly reachable at [https://the-headroom.vercel.app/](https://the-headroom.vercel.app/). Its latest deployment is READY and uses the frontend release commit documented below. and aliases the production domain. The production interface was opened in a browser; home, control, service, admission, change, incident, settlement and protocol routes were exercised. The injected EIP-1193 wallet connected and chain reads returned the deployed state after load. Real protocol writes were submitted and reconciled; the deterministic and SAFE admission evidence is recorded above. No genuine change or incident occurred during the review window.

The read-only integration smoke path uses `genlayer-js==1.1.8` unsigned `readContract`, because `genlayer-py==0.16.3` currently raises `No account provided` on views. The SDK read was verified against the canonical deployment; full Python/Node cross-runtime smoke orchestration remains environment-dependent and is not reported as a passing integration-suite run.


## Final release state

Contract Source Commit: `add2f35d08cde554bec6d9bed98c5094554035d9`

Frontend and documentation release commits are separate from the deployed contract source. The final application commit is recorded after this release commit is pushed.

Canonical Contract: `0x235Fd204E6d78e61055a6BD24B06319aA503D2f1`

Deployment Transaction: `0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`

### Live transaction chronology

| Action | Transaction | Result |
|---|---|---|
| Create `hr-cv-1` | `0xa0792d197bb882b55fffc1198043854a03793c0884c75c51a2563c664c003cbc` | FINALIZED, execution success, return `hr-cv-1` |
| Close `hr-cv-1` | `0x1898d9f453d82c70cb8194b698bd385d522f9d3f346f089337ee973ddbc5ad20` | FINALIZED, execution success, null return |
| Withdraw | `0xbd1dbd26c544ed3bf542b602bce8a6249af539e877b185dd431a8b7dee9ae99b` | execution success, 1 GEN return |
| Create `hr-cv-3` | `0x80c3f3e09d4fb8d27722a0dbe9bb87cf07e72a1030e03a075b011cbb6969fec0` | FINALIZED, execution success |
| Deterministic prevention `hr-r-1` | `0x7cc4f80a71da8a9bd062133aa3ea97591e4c5440593dec9598f4b13285988a5d` | `DENIED_DETERMINISTIC`, no reserves |
| Request `hr-r-2` | `0x1123d3dd64165cacf8e9121699773eebec2a8805c46a9d94d340b60df5cfaf1a` | PENDING, deterministic checks passed |
| Review `hr-r-2` | `0xe8f0931b08139f206eb0411e01642944b8b01bbf3e200c51de82645b7dbf30ed` | `SAFE`, ACTIVE, one unit and 0.10 GEN reserved |

The first reservation attempt `0xed55427df945500c9e772413f9d711bc6f0c7b30e9700c82256b190c27728de0` rolled back because the frontend encoded `max_credit_atto` as a string. It changed no state; commit `e8df75a` corrected the encoding.

The production UI previously showed false failures when receipt monitoring lost RPC connectivity or execution metadata was incomplete. Receipt reconciliation was hardened in `d02dbbe`; later casing, admissions visibility and amount-format issues were corrected without changing the contract.

At the final semantic review, the provider URL and Domainee probe both returned HTTP 200. No genuine change event or incident occurred during the review window, so those branches were not fabricated.

Final Release HEAD: `91b01d6261d6b5d606848aba8c64a721a939ceb3`
Final CI: `CI run for final HEAD is pending`

