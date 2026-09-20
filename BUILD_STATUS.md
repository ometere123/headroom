# HEADROOM build status

| Gate | Result |
| --- | --- |
| Single-contract architecture and Studionet hard lock | Verified, chain 61999 / `https://studio.genlayer.com/api` |
| Injected EIP-1193 frontend | Verified |
| Reservation/change/incident/challenge hardening | Implemented; 46 Direct Mode tests pass |
| Python requirements | `genlayer-test==0.29.2`, compatible `genlayer-py==0.16.3` |
| GenVM contract validation | Passes with pinned Depends SDK using `genvm-linter==0.11.1rc2` |
| GenVM static lint | Seven documented custom-consensus E010 warnings; exact-set CI gate |
| Frontend typecheck/build | Pending final run |
| Repository static checks | Pending final run |
| CI push result | Pending push |
| Real Studionet integration/consensus | Not run in this pass |
| Deployment | Not performed; user explicitly deferred deployment |
