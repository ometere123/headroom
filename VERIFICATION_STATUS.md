# Verification status

## Completed

- Clean Python 3.12 WSL venv installed the pinned project requirements. The Direct Mode suite passed: **46 passed**. See [the environment and full package freeze](docs/direct-mode-environment.md).
- `genvm-lint setup --contract contracts/headroom.py` succeeds under `genvm-linter==0.11.1rc2`; `validate` passes for Headroom (31 public methods: 10 views, 21 writes). Raw lint reports seven E010 warnings on the documented custom leader/validator pattern. Full outputs and the narrow CI disposition are recorded in [the lint report](docs/genvm-lint-disposition.md) and [captured command output](docs/genvm-lint-full-output.txt).
- Current contract validation preserves the Depends runner pin and `gl.vm.run_nondet_unsafe` consensus design.
- Frontend dependency is GenLayer JS 1.1.8; only generic injected EIP-1193 is used, and the app is locked to Studionet 61999 / `https://studio.genlayer.com/api`.

## Pending final gates

- Frontend `npm run typecheck` and `npm run build`.
- Release, frontend-surface and contract static checks.
- Push-triggered GitHub Actions result.
- Real Studionet integration and independent consensus verification.

No deployment has occurred. Passing local checks does not establish deployed behavior or real-network consensus.
