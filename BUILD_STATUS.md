# HEADROOM Release Status

## Canonical deployment

- Network: GenLayer Studionet, chain 61999; RPC `https://studio.genlayer.com/api`.
- Contract: `0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2`.
- Deployment transaction: `0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8`; FINALIZED and successful execution.
- The deployed contract source is commit `d204e08cbe4753d80a865d34fc5f185e0d6083ed`, corresponding to `contracts/headroom.py` (SHA-256 `0AB5E90F00286962ED9FC727D97288A61EDAAE59DB55334D531F89B68BDE1565`).
- Deployed schema: 31 methods, 10 views and 21 writes. Deployed `get_stats()` reports Studionet/61999, `accounting_balanced=true`, and `admin_controls=false`.
- Activation requires provider authorization or meaningful requester stake before provider capacity or collateral can be locked. `INDEPENDENT_PROBE` must use immutable `stats.uptimerobot.com`; provider registries cannot extend it. Custom provider domains/CNAME aliases do not qualify, same-registrable-domain rejection remains defense in depth, and no DNS/WHOIS verification is claimed.

## Release candidate

The app uses an infrastructure operations shell with a persistent operations rail, live-data control/service boards, admission/change/incident command boards, a service workspace, and a settlement/withdrawal workspace. Evidence forms are structured, date inputs interpret UTC or UTC+1, and durations convert at the contract boundary. The landing page distinguishes on-chain values from unavailable reads and includes the HEADROOM-specific product workflow and trust model.

| Gate | Result |
| --- | --- |
| Stable network lock | Studionet 61999 only |
| Contract source / deployment match | Verified against the corrected trust-boundary source candidate |
| Contract methods | 10 views / 21 writes |
| Direct Mode | 60 passed in [GitHub Actions run 35908341602](https://github.com/ometere123/headroom/actions/runs/35908341602) |
| GenVM validation/lint | Pinned linter; only the exact reviewed seven E010 diagnostics are allowed |
| Static release/pattern/frontend checks | Candidate result recorded in review evidence |
| Frontend typecheck/build | Candidate result recorded in review evidence |
| Vercel | Existing `headroom` project, root `frontend`; Production env configured for canonical contract and Studionet |
| Production deploy/browser walkthrough | Release-candidate result recorded in review evidence |
| Live contract writes | Awaiting the user’s wallet approval when a real operation is prepared |

The canonical contract currently has no covenants or lifecycle records. No incident, semantic decision, admission, settlement, or withdrawal is claimed until a real finalized transaction establishes it.
