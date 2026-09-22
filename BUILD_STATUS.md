# HEADROOM Release Status

## Canonical deployment

- Network: GenLayer Studionet, chain 61999; RPC `https://studio.genlayer.com/api`.
- Contract: `0x235Fd204E6d78e61055a6BD24B06319aA503D2f1`.
- Deployment transaction: `0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`; FINALIZED and successful execution.
- The deployed contract source exactly matches `contracts/headroom.py` from source commit `add2f35d08cde554bec6d9bed98c5094554035d9` (SHA-256 `a61cb6815251ac3f118fb73fe81c9e10b7575c13ab3135e7664ebcdd9b587dbd`). Frontend and documentation work does not require a contract redeployment.
- Deployed schema: 31 methods, 10 views and 21 writes. Deployed `get_stats()` reports Studionet/61999, `accounting_balanced=true`, and `admin_controls=false`.

## Release candidate

The app uses an infrastructure operations shell with a persistent operations rail, live-data control/service boards, admission/change/incident command boards, a service workspace, and a settlement/withdrawal workspace. Evidence forms are structured, date inputs interpret UTC or UTC+1, and durations convert at the contract boundary. The landing page distinguishes on-chain values from unavailable reads and includes the HEADROOM-specific product workflow and trust model.

| Gate | Result |
| --- | --- |
| Stable network lock | Studionet 61999 only |
| Contract source / deployment match | Verified; contract unchanged since deployed source commit |
| Contract methods | 10 views / 21 writes |
| Direct Mode | 57 passed on Python 3.12.3 |
| GenVM validation/lint | `genvm-linter==0.11.1rc2`: validation passes; wrapper passes with exactly seven reviewed E010 diagnostics |
| Static release/pattern/frontend checks | PASS |
| Frontend typecheck/build | PASS |
| Vercel | Existing `headroom` project, root `frontend`; Production env configured for canonical contract and Studionet |
| Production deploy/browser walkthrough | READY; existing Vercel project deployed to https://the-headroom.vercel.app/ and browser routes/live reads/wallet connection exercised |
| Live contract writes | Awaiting the user’s wallet approval when a real operation is prepared |

Live protocol proof is now recorded. `hr-cv-3` is active; `hr-r-1` is a finalized deterministic prevention and `hr-r-2` is a finalized SAFE semantic admission. No incident or settlement is claimed because no qualifying real-world event occurred. Contract Source Commit: `add2f35d08cde554bec6d9bed98c5094554035d9`

Final application commits are frontend/docs commits and do not replace the deployed contract source commit.
Frontend Implementation Commit: `f6b9cf5c57348c956c4a559ab12e7ecb6aca8aa7`
Final Release HEAD: `PENDING_FINAL_COMMIT`; Final CI: `PENDING_FINAL_CI`. The live proof is documented in `docs/REVIEW_EVIDENCE.md`. No genuine change or incident occurred during the review window.
