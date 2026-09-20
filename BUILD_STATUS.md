# HEADROOM build status

| Gate | Result |
| --- | --- |
| Single-contract architecture and network lock | Verified; Studionet chain 61999 / `https://studio.genlayer.com/api` |
| Admission deterministic prechecks | Failed capacity/collateral requests are persisted as `DENIED_DETERMINISTIC`, counted as prevented, and excluded from semantic review |
| Pending admission accounting | Pending requests reserve no units, liability, or active slot; SAFE activation rechecks live headroom |
| Evidence provenance | Covenant freezes bounded HTTPS origin/class registry; every consequential source must match |
| Contract surface | 10 public views / 21 public writes |
| Direct Mode adversarial tests | 54 tests |
| GenVM validation and lint gate | Validation passes; CI allows only the seven documented E010 custom consensus diagnostics |
| Frontend typecheck and production build | Passed |
| Release, contract-pattern and frontend-surface checks | Passed |
| GitHub Actions | Passed on pushed `main`; current workflow result linked in `docs/REVIEW_EVIDENCE.md` |
| Real Studionet integration/consensus | Pending |
| Deployment and public hosting | Pending; no deployment performed |
