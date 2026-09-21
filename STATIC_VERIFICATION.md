# HEADROOM Verification Record

- Network: GenLayer Studionet only, chain `61999`, RPC `https://studio.genlayer.com/api`.
- Canonical contract: `0x4d300dF9aCADC904DfC9473F0D970bd6CB1c122C`.
- Deployment: `0x571288f46cef612de2ff24cf120a2ddeb922a3ce1e9b5200bb2c05668ee6b929`; FINALIZED with successful execution.
- Deployed source hash matches exact `contracts/headroom.py` at commit `7aecd8f4312557de504de2709d04f646c102dce0`; deployed schema is 10 views / 21 writes.
- Pinned linter gate validates the contract and tolerates only the exact reviewed seven E010 custom validator reachability warnings. See `docs/genvm-lint-disposition.md` and `docs/genvm-lint-full-output.txt`.
- Direct Mode uses Python 3.12, `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, and the tested pinned GenVM runner. The current suite contains 54 tests.
- Frontend is pinned to `genlayer-js==1.1.8`; candidate typecheck/build, CI, Vercel deploy, and browser results are recorded in `docs/REVIEW_EVIDENCE.md`.
- Initial deployed `get_stats()` reports zero covenants/reservations/changes/incidents/admissions/preventions/settlements, `accounting_balanced=true`, and `admin_controls=false`.

Deployment/read facts do not prove live semantic consensus or a complete economic lifecycle. No protocol write is claimed until its wallet-approved transaction and successful post-state are recorded.