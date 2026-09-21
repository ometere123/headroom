# HEADROOM Release Handoff

HEADROOM is a preventive SLA admission and enforcement protocol: deterministic capacity and collateral rules reject impossible commitments; GenLayer assesses changing public evidence before a promise or operational change is protected; the same frozen covenant governs incident facts; contract code calculates liability and settlement.

## Canonical release facts

- Studionet only: chain `61999`, RPC `https://studio.genlayer.com/api`.
- Contract: `0x4d300dF9aCADC904DfC9473F0D970bd6CB1c122C`.
- Deployment transaction: `0x571288f46cef612de2ff24cf120a2ddeb922a3ce1e9b5200bb2c05668ee6b929`.
- Deployment is FINALIZED and execution succeeded. Deployed source hash matches `contracts/headroom.py` from source commit `7aecd8f4312557de504de2709d04f646c102dce0`; schema: 10 views / 21 writes.
- Vercel project: existing `headroom` project, root `frontend`, production domain `https://the-headroom.vercel.app/`.
- Stable stack only: CLI 0.39.1, JS SDK 1.1.8, Python 3.12, Direct Mode `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, linter `genvm-linter==0.11.1rc2`.

## Safety invariants

Preserve deterministic request denials, pending requests reserving nothing, SAFE activation headroom recheck, pre-exposure formation, non-retrospective change permits, frozen evidence origin/classes, independent measurement, bounded incident facts, deterministic liability, full-case bonded challenge, and accounting conservation. Keep semantic validator replay substantive. The exact seven reviewed E010 warnings are accepted only if validation succeeds and CI confirms the same enumerated diagnostics.

Never claim a live transaction, outage, monitor, source outcome, or economic settlement that did not happen. The user requires pausing at each production wallet approval so they can sign. Do not use a private key, CLI account signer, backend signer, or fake transaction. The initial contract state contains no covenant or protocol records.

## Verification and evidence

Run the exact release checks in README. Use the chronological table and current stats in `docs/REVIEW_EVIDENCE.md`. Evidence candidates are distinguished from evidence actually used by a covenant. Any claim of semantic admission or incident settlement requires actual Studionet consensus, a finalized transaction with successful execution, and a refreshed state read.