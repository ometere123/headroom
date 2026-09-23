# Verification Status

## Canonical contract

The deployed Studionet contract `0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2` was finalized successfully by transaction `0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8`. Deployed source commit is `d204e08cbe4753d80a865d34fc5f185e0d6083ed`, SHA-256 `0AB5E90F00286962ED9FC727D97288A61EDAAE59DB55334D531F89B68BDE1565`, corresponding to `contracts/headroom.py`. Its schema is 31 methods: 10 views and 21 writes. Live `get_stats()` reports Studionet, chain 61999, balanced accounting, and no admin controls.

Activation requires provider authorization or meaningful requester stake before provider capacity or collateral can be locked. `INDEPENDENT_PROBE` is limited to immutable `stats.uptimerobot.com`; provider registries cannot extend it, custom domains/CNAME aliases do not qualify, same-registrable-domain rejection remains defense in depth, and no DNS/WHOIS verification is claimed.

## Candidate checks

Record the results for the exact release commit here and in [review evidence](docs/REVIEW_EVIDENCE.md):

- Python compile: result recorded after candidate run.
- GenVM validation: `genvm-linter==0.11.1rc2`; the reviewed exact seven E010 custom validator diagnostics remain the only accepted warnings.
- Direct Mode: 60 passed in [GitHub Actions run 35908341602](https://github.com/ometere123/headroom/actions/runs/35908341602).
- Release, contract-pattern and frontend-surface checks: result recorded after candidate run.
- Frontend SDK: exact `genlayer-js==1.1.8`; typecheck and production build results recorded after candidate run.
- GitHub Actions: [run 35908341602](https://github.com/ometere123/headroom/actions/runs/35908341602) passed all required checks.
- Vercel Production: existing project and canonical public domain verification recorded after deployment.

## Live protocol evidence

The deployment is verified. Covenant creation and subsequent protocol operations require a wallet signature from the user. Until those transactions are personally approved and successfully finalized, this repository makes no live claim for semantic admission, prevention, change preflight, incident measurement, exception examination, liability, challenge, settlement, or withdrawal.
