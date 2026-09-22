# Live Demo Evidence

HEADROOM is live on GenLayer Studionet (61999) at https://the-headroom.vercel.app/. The canonical contract is `0x235Fd204E6d78e61055a6BD24B06319aA503D2f1`, deployed by `0x99114e7506ca30f35ee1c9bc1f81c7147c56f305fb49c0bed97071c5a1e7545e`.

## Current truthful state

- `hr-cv-1` and `hr-cv-2` are historical CLOSED covenants.
- `hr-cv-3` is ACTIVE with a 1 GEN bond, 10 unit ceiling and 8 unit safe capacity.
- `hr-r-1` is a real 9 unit request recorded as `DENIED_DETERMINISTIC`; capacity precheck false, liability precheck true, and no capacity or liability was reserved. Transaction: `0x7cc4f80a71da8a9bd062133aa3ea97591e4c5440593dec9598f4b13285988a5d`.
- `hr-r-2` passed deterministic checks and underwent real GenLayer admission. Request transaction: `0x1123d3dd64165cacf8e9121699773eebec2a8805c46a9d94d340b60df5cfaf1a`. Review transaction: `0xe8f0931b08139f206eb0411e01642944b8b01bbf3e200c51de82645b7dbf30ed`. Consensus result: `SAFE`, risk `GREEN`; the reservation is ACTIVE with one unit and 0.10 GEN reserved liability.

The frozen evidence was the production URL and the Domainee HTTP probe. At review time both returned HTTP 200, and the probe reported `up=true` for the production URL. The semantic basis is recorded on-chain and in `docs/REVIEW_EVIDENCE.md`.

No genuine maintenance event or qualifying service incident occurred during this review window. Change control, measurement, exception, liability, challenge, settlement and withdrawal were not fabricated. Those branches remain covered by Direct Mode and prior read-only evidence.
