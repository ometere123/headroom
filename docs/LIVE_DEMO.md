# HEADROOM Live Demo Protocol

HEADROOM must be demonstrated with truthful evidence and real wallet-approved transactions. The deployed Studionet contract currently has no covenants or lifecycle records.

## Evidence candidates

- GitHub status API: `https://www.githubstatus.com/api/v2/summary.json` — provider-operated status, `PROVIDER_STATUS`.
- Checkly GitHub availability: `https://www.checklyhq.com/availability/github/` — separate synthetic-monitor operator, candidate `INDEPENDENT_PROBE`.

These are research candidates, not frozen contract evidence and not proof of an outage. Recheck that they are currently reachable and contain evidence relevant to the exact service before forming a covenant. An old incident cannot be moved into a newly created SLA window.

## Safe execution sequence

1. Inspect sources and authorize each HTTPS origin for its real evidence class.
2. Ask the provider wallet to approve `create_covenant` and fund the bond.
3. Demonstrate deterministic refusal with an impossible request; verify it reserves nothing and increments `prevented`.
4. Use a distinct-source request supported by current, healthy evidence; obtain wallet approval, run consensus, and verify state after refresh.
5. Exercise change preflight with a real future notice and evidence before the window.
6. Run the post-failure path only if a genuine measured miss occurs within the active reservation window.
7. Re-fetch final state, settlement certificate, and accounting invariant after each completed step.

Do not create synthetic history, label provider-controlled evidence independent, fabricate an outage, or infer a successful execution from transaction finality alone. See [review evidence](REVIEW_EVIDENCE.md) for actual transactions; unexecuted paths are marked explicitly.
