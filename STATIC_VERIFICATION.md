# HEADROOM Verification Record

- Network: GenLayer Studionet only, chain `61999`, RPC `https://studio.genlayer.com/api`.
- Canonical contract: `0x235Fd204E6d78e61055a6BD24B06319aA503D2f1`.
- Deployment: `0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`; FINALIZED with successful execution.
- Deployed source hash matches exact `contracts/headroom.py` at commit `add2f35d08cde554bec6d9bed98c5094554035d9`; deployed schema is 10 views / 21 writes.
- Pinned linter gate validates the contract and tolerates only the exact reviewed seven E010 custom validator reachability warnings. See `docs/genvm-lint-disposition.md` and `docs/genvm-lint-full-output.txt`.
- Direct Mode uses Python 3.12, `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, and the tested pinned GenVM runner. The current suite contains 54 tests.
- Frontend is pinned to `genlayer-js==1.1.8`; candidate typecheck/build, CI, Vercel deploy, and browser results are recorded in `docs/REVIEW_EVIDENCE.md`.
- Initial deployed `get_stats()` reports zero covenants/reservations/changes/incidents/admissions/preventions/settlements, `accounting_balanced=true`, and `admin_controls=false`.

Deployment/read facts do not prove live semantic consensus or a complete economic lifecycle. No protocol write is claimed until its wallet-approved transaction and successful post-state are recorded.