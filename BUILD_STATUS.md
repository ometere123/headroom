# HEADROOM Release Status

## Canonical deployment

- Network: GenLayer Studionet, chain 61999; RPC `https://studio.genlayer.com/api`.
- Contract: `0x4d300dF9aCADC904DfC9473F0D970bd6CB1c122C`.
- Deployment transaction: `0x571288f46cef612de2ff24cf120a2ddeb922a3ce1e9b5200bb2c05668ee6b929`; FINALIZED and successful execution.
- The deployed contract source exactly matches `contracts/headroom.py` from source commit `7aecd8f4312557de504de2709d04f646c102dce0` (SHA-256 `461fc74172e1d4a8a3e36d344280bc4e1cb22afd8ac44d9ea750138ee3954abe`). Frontend and documentation work does not require a contract redeployment.
- Deployed schema: 31 methods, 10 views and 21 writes. Deployed `get_stats()` reports Studionet/61999, `accounting_balanced=true`, and `admin_controls=false`.

## Release candidate

The app uses an infrastructure operations shell with a persistent operations rail, live-data control/service boards, admission/change/incident command boards, a service workspace, and a settlement/withdrawal workspace. Evidence forms are structured, date inputs interpret UTC or UTC+1, and durations convert at the contract boundary. The landing page distinguishes on-chain values from unavailable reads and includes the HEADROOM-specific product workflow and trust model.

| Gate | Result |
| --- | --- |
| Stable network lock | Studionet 61999 only |
| Contract source / deployment match | Verified; contract unchanged since deployed source commit |
| Contract methods | 10 views / 21 writes |
| Direct Mode | 54 passed on Python 3.12.3 |
| GenVM validation/lint | `genvm-linter==0.11.1rc2`: validation passes; wrapper passes with exactly seven reviewed E010 diagnostics |
| Static release/pattern/frontend checks | PASS |
| Frontend typecheck/build | PASS |
| Vercel | Existing `headroom` project, root `frontend`; Production env configured for canonical contract and Studionet |
| Production deploy/browser walkthrough | Pending production deploy and browser review |
| Live contract writes | Awaiting the user’s wallet approval when a real operation is prepared |

The canonical contract currently has no covenants or lifecycle records. No incident, semantic decision, admission, settlement, or withdrawal is claimed until a real finalized transaction establishes it.
