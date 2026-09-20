# HEADROOM verification record

Date: 2026-09-20

## Artifact facts

- network target: GenLayer Studionet only
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- contract: `contracts/headroom.py`
- public contract methods: 31 (10 view, 21 write)
- Direct Mode tests: 46
- browser signer: generic injected EIP-1193

## Passed

- Direct Mode on clean WSL Python 3.12.3 environment: **46 passed**.
- Frontend `npm run typecheck`: pass.
- Frontend `npm run build`: pass; Next.js generated all seven routes.
- `scripts/check_release.py`: pass; chain/RPC hard lock verified.
- `scripts/check_contract_patterns.py`: pass.
- `scripts/check_frontend_surface.py`: pass.
- GenVM `setup` and contract `validate`: pass with `genvm-linter==0.11.1rc2` and pinned Depends SDK. Static lint reports seven exact E010 reachability warnings; see `docs/genvm-lint-disposition.md`.

## Not performed

- Real Studionet integration/consensus was not run.
- Deployment and public hosting were not performed.

Passing local checks is not evidence of a live deployment or real-network consensus.
