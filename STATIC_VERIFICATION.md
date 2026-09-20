# HEADROOM verification record

- Network: GenLayer Studionet only, chain `61999`, RPC `https://studio.genlayer.com/api`.
- Contract surface: 10 public views / 21 public writes.
- Direct Mode: 54 tests pass in clean Python 3.12 environment.
- Python compile, release scan, contract-pattern guard and frontend-surface guard: pass.
- Frontend typecheck and Next.js production build: pass.
- GenVM contract validation: pass using pinned Depends SDK and `genvm-linter==0.11.1rc2`. Raw static lint reports seven E010 reachability warnings on documented custom leader/validator functions and `_fetch`; a narrow CI gate checks exact messages and counts. See `docs/genvm-lint-disposition.md` and `docs/genvm-lint-full-output.txt`.
- GitHub Actions: pass on `main`; see the [HEADROOM CI workflow runs](https://github.com/ometere123/headroom/actions/workflows/ci.yml?query=branch%3Amain).
- Live Studionet consensus, deployment, public hosting and economic lifecycle proof: pending.

Passing local and hosted checks does not establish live consensus or deployment behavior. No deployment occurred during this verification.
