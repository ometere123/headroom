# Verification Status

## Canonical contract

The deployed Studionet contract `0x44f03156B27d92e9527992744207ca73d0E6F980` was finalized successfully by transaction `0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b`. Deployed source SHA-256 is `FD652486B69C65DB6B7AACEF736BFF84C5A9E8456C946B117B95D13CD6FA5D11`, corresponding to the corrected trust-boundary implementation in repository `contracts/headroom.py`. Its schema is 10 views and 21 writes. Live `get_stats()` reports Studionet, chain 61999, balanced accounting, and no admin controls.

## Candidate checks

Record the results for the exact release commit here and in [review evidence](docs/REVIEW_EVIDENCE.md):

- Python compile: result recorded after candidate run.
- GenVM validation: `genvm-linter==0.11.1rc2`; the reviewed exact seven E010 custom validator diagnostics remain the only accepted warnings.
- Direct Mode: suite count/result recorded after candidate run.
- Release, contract-pattern and frontend-surface checks: result recorded after candidate run.
- Frontend SDK: exact `genlayer-js==1.1.8`; typecheck and production build results recorded after candidate run.
- GitHub Actions: candidate CI run URL recorded after push.
- Vercel Production: existing project and canonical public domain verification recorded after deployment.

## Live protocol evidence

The deployment is verified. Covenant creation and subsequent protocol operations require a wallet signature from the user. Until those transactions are personally approved and successfully finalized, this repository makes no live claim for semantic admission, prevention, change preflight, incident measurement, exception examination, liability, challenge, settlement, or withdrawal.
