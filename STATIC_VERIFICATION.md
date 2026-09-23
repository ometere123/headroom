# HEADROOM Verification Record

- Network: GenLayer Studionet only, chain `61999`, RPC `https://studio.genlayer.com/api`.
- Canonical contract: `0x44f03156B27d92e9527992744207ca73d0E6F980`.
- Deployment: `0x4976cfd3c27c3d31db6a9a9769ee887269b1e6b0940161924a1b023f272ac40b`; FINALIZED with successful execution.
- Deployed source corresponds to the corrected trust-boundary implementation in `contracts/headroom.py` (SHA-256 `FD652486B69C65DB6B7AACEF736BFF84C5A9E8456C946B117B95D13CD6FA5D11`); deployed schema is 10 views / 21 writes.
- Pinned linter gate validates the contract and tolerates only the exact reviewed seven E010 custom validator reachability warnings. See `docs/genvm-lint-disposition.md` and `docs/genvm-lint-full-output.txt`.
- Direct Mode uses Python 3.12, `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, and the tested pinned GenVM runner. The current suite contains 54 tests.
- Frontend is pinned to `genlayer-js==1.1.8`; candidate typecheck/build, CI, Vercel deploy, and browser results are recorded in `docs/REVIEW_EVIDENCE.md`.
- Initial deployed `get_stats()` reports zero covenants/reservations/changes/incidents/admissions/preventions/settlements, `accounting_balanced=true`, and `admin_controls=false`.

Deployment/read facts do not prove live semantic consensus or a complete economic lifecycle. No protocol write is claimed until its wallet-approved transaction and successful post-state are recorded.
