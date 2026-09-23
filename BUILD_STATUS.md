# HEADROOM Release Status

## Canonical deployment

- Network: GenLayer Studionet, chain 61999; RPC `https://studio.genlayer.com/api`.
- Contract: `0x44f03156B27d92e9527992744207ca73d0E6F980`.
- Deployment transaction: `0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b`; FINALIZED and successful execution.
- The deployed contract source corresponds to the corrected trust-boundary implementation in `contracts/headroom.py` (SHA-256 `FD652486B69C65DB6B7AACEF736BFF84C5A9E8456C946B117B95D13CD6FA5D11`). Frontend and documentation work does not require a contract redeployment.
- Deployed schema: 31 methods, 10 views and 21 writes. Deployed `get_stats()` reports Studionet/61999, `accounting_balanced=true`, and `admin_controls=false`.

## Release candidate

The app uses an infrastructure operations shell with a persistent operations rail, live-data control/service boards, admission/change/incident command boards, a service workspace, and a settlement/withdrawal workspace. Evidence forms are structured, date inputs interpret UTC or UTC+1, and durations convert at the contract boundary. The landing page distinguishes on-chain values from unavailable reads and includes the HEADROOM-specific product workflow and trust model.

| Gate | Result |
| --- | --- |
| Stable network lock | Studionet 61999 only |
| Contract source / deployment match | Verified against the corrected trust-boundary source candidate |
| Contract methods | 10 views / 21 writes |
| Direct Mode | 54 tests; exact candidate rerun is recorded in `docs/REVIEW_EVIDENCE.md` after CI |
| GenVM validation/lint | Pinned linter; only the exact reviewed seven E010 diagnostics are allowed |
| Static release/pattern/frontend checks | Candidate result recorded in review evidence |
| Frontend typecheck/build | Candidate result recorded in review evidence |
| Vercel | Existing `headroom` project, root `frontend`; Production env configured for canonical contract and Studionet |
| Production deploy/browser walkthrough | Release-candidate result recorded in review evidence |
| Live contract writes | Awaiting the user’s wallet approval when a real operation is prepared |

The canonical contract currently has no covenants or lifecycle records. No incident, semantic decision, admission, settlement, or withdrawal is claimed until a real finalized transaction establishes it.
