# HEADROOM Release Handoff

HEADROOM is a preventive SLA admission and enforcement protocol: deterministic capacity and collateral rules reject impossible commitments; GenLayer assesses changing public evidence before a promise or operational change is protected; the same frozen covenant governs incident facts; contract code calculates liability and settlement.

## Canonical release facts

- Studionet only: chain `61999`, RPC `https://studio.genlayer.com/api`.
- Contract: `0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2`.
- Deployment transaction: `0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8`.
- Deployment is FINALIZED and execution succeeded. The deployed source is commit `d204e08cbe4753d80a865d34fc5f185e0d6083ed`, corresponding to `contracts/headroom.py` (SHA-256 `0AB5E90F00286962ED9FC727D97288A61EDAAE59DB55334D531F89B68BDE1565`); schema: 10 views / 21 writes.
- `get_stats()` verifies Studionet / 61999, the stable RPC, `accounting_balanced=true`, and `admin_controls=false`. Direct Mode: 60 passed in [green CI run 35908341602](https://github.com/ometere123/headroom/actions/runs/35908341602).
- Activation requires provider authorization or meaningful requester stake before provider capacity or collateral can be locked. `INDEPENDENT_PROBE` is limited to immutable `stats.uptimerobot.com`; provider registries cannot extend it, custom domains/CNAME aliases do not qualify, same-registrable-domain rejection remains defense in depth, and no DNS/WHOIS verification is claimed.
- Vercel project: existing `headroom` project, root `frontend`, production domain `https://the-headroom.vercel.app/`.
- Stable stack only: CLI 0.39.1, JS SDK 1.1.8, Python 3.12, Direct Mode `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, linter `genvm-linter==0.11.1rc2`.

## Safety invariants

Preserve deterministic request denials, pending requests reserving nothing, SAFE activation headroom recheck, pre-exposure formation, non-retrospective change permits, frozen evidence origin/classes, independent measurement, bounded incident facts, deterministic liability, full-case bonded challenge, and accounting conservation. Keep semantic validator replay substantive. The exact seven reviewed E010 warnings are accepted only if validation succeeds and CI confirms the same enumerated diagnostics.

Never claim a live transaction, outage, monitor, source outcome, or economic settlement that did not happen. The user requires pausing at each production wallet approval so they can sign. Do not use a private key, CLI account signer, backend signer, or fake transaction. The initial contract state contains no covenant or protocol records.

## Verification and evidence

Run the exact release checks in README. Use the chronological table and current stats in `docs/REVIEW_EVIDENCE.md`. Evidence candidates are distinguished from evidence actually used by a covenant. Any claim of semantic admission or incident settlement requires actual Studionet consensus, a finalized transaction with successful execution, and a refreshed state read.
