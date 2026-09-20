# HEADROOM static packaging verification

Date: 2026-09-19

This report records checks that were actually executed on the packaged source. It is intentionally narrower than a live GenLayer verification report.

## Artifact facts

- network target: Studionet only
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- contract: `contracts/headroom.py`
- contract SHA-256: `1fbc3e79cbca5954e179379b12060a507c6552ba5cc1a4b5113cd6b4d5a956f6`
- contract lines: 458
- public methods: 29
- authored Direct Mode tests: 22
- frontend TS/TSX source files parsed: 17
- browser signer: injected EIP-1193 `window.ethereum`

## Passed in the packaging environment

```text
Python compile                         PASS
contract trust-boundary static guard  PASS
release/network/wallet static scan    PASS
frontend route/action surface guard   PASS
TypeScript/TSX parser diagnostics     PASS (0 syntax diagnostics)
```

## Deliberately unverified here

```text
genvm-lint                            NOT RUN — package unavailable offline
Direct Mode execution                 NOT RUN — genlayer-test unavailable offline
Next dependency typecheck/build       NOT RUN — npm dependencies unavailable offline
Studionet deployment/consensus        NOT RUN — requires finishing environment/account
live economic lifecycle               NOT RUN
public frontend                        NOT RUN
```

Passing this file is not evidence of a live deployment. Replace the `TBD` fields in `docs/REVIEW_EVIDENCE.md` only with real final hashes/addresses/results produced after the remaining gates run.
