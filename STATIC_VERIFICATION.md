# HEADROOM Verification Record

- Network: GenLayer Studionet only, chain `61999`, RPC `https://studio.genlayer.com/api`.
- Canonical contract: `0xE0dB1742E5e218CC0dEEbCdF998D37Ed017037b2`.
- Deployment: `0xd217dcd508e1009c4bbfbfc7dade9404147379a4c727672fee0a7a2bac19fec8`; FINALIZED with successful execution.
- Deployed source is commit `d204e08cbe4753d80a865d34fc5f185e0d6083ed`, corresponding to `contracts/headroom.py` (SHA-256 `0AB5E90F00286962ED9FC727D97288A61EDAAE59DB55334D531F89B68BDE1565`); deployed schema is 10 views / 21 writes.
- Activation requires provider authorization or meaningful requester stake before provider capacity/collateral can be locked. `INDEPENDENT_PROBE` accepts only immutable `stats.uptimerobot.com`; provider registries cannot extend it. Custom domains/CNAME aliases do not qualify, same-registrable-domain rejection is defense in depth, and no DNS/WHOIS verification is claimed.
- Pinned linter gate validates the contract and tolerates only the exact reviewed seven E010 custom validator reachability warnings. See `docs/genvm-lint-disposition.md` and `docs/genvm-lint-full-output.txt`.
- Direct Mode uses Python 3.12, `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, and the tested pinned GenVM runner. 60 tests passed in [GitHub Actions run 35908341602](https://github.com/ometere123/headroom/actions/runs/35908341602).
- Frontend is pinned to `genlayer-js==1.1.8`; candidate typecheck/build, CI, Vercel deploy, and browser results are recorded in `docs/REVIEW_EVIDENCE.md`.
- Initial deployed `get_stats()` reports zero covenants/reservations/changes/incidents/admissions/preventions/settlements, `accounting_balanced=true`, and `admin_controls=false`.

Deployment/read facts do not prove live semantic consensus or a complete economic lifecycle. No protocol write is claimed until its wallet-approved transaction and successful post-state are recorded.
