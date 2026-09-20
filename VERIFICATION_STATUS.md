# Verification status

## Passed gates

- Source-derived contract surface: 10 public views and 21 public writes. Direct Mode suite: 54 tests. Run `python scripts/update_verification_facts.py` to refresh README/reviewer count facts from the current ASTs.
- Python 3.12 clean WSL Direct Mode environment installed `requirements.txt`; all 54 tests pass using official GenVM runner archive `v0.2.16`, which contains the contract Depends runner. `genlayer-test==0.29.2` and `genlayer-py==0.16.3` are compatible; the test package declares `genlayer-py>=0.13,<0.17`.
- `python -m py_compile contracts/headroom.py tests/direct/*.py tests/integration/*.py`: pass.
- `python scripts/check_genvm_lint.py`: pass with successful contract validation and only the exact, documented seven E010 warnings around custom `gl.vm.run_nondet_unsafe` leader closures/fetch helper. Raw diagnostics remain captured in `docs/genvm-lint-full-output.txt`.
- Release, contract-pattern and frontend-surface checks: pass.
- Frontend `npm install`, `npm run typecheck`, and `npm run build`: pass.
- GitHub Actions on `main`: pass; see [the latest HEADROOM CI run](https://github.com/ometere123/headroom/actions/workflows/ci.yml?query=branch%3Amain).

## Pending live proof

- Real Studionet integration and independent consensus evidence.
- Deployment, deployed source/schema comparison, complete live economic lifecycle, deployed-address frontend wiring, and public hosting.

No deployment has occurred. The release remains locked to Studionet 61999 / `https://studio.genlayer.com/api` with generic injected EIP-1193 only.
