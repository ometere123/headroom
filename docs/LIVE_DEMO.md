# HEADROOM Live Demo Protocol

HEADROOM must be demonstrated with truthful evidence and real wallet-approved transactions. The deployed Studionet contract currently has no covenants or lifecycle records.

## Evidence candidates

- GitHub status API: `https://www.githubstatus.com/api/v2/summary.json` - provider-operated status, `PROVIDER_STATUS`.
- Checkly GitHub availability: `https://www.checklyhq.com/availability/github/` - separate synthetic-monitor operator, candidate `INDEPENDENT_PROBE`.

These are research candidates, not frozen contract evidence and not proof of an outage. GitHub status reported its components operational with no incidents/maintenance at the time recorded in review evidence. Checkly's page reported a separate probe as up, but its observation time differed. These sources do not establish unsafe health or an outage and are not appropriate evidence for a service the covenant provider does not operate. Recheck relevance and freshness before forming any covenant. An old incident cannot be moved into a newly created SLA window.

## Current execution boundary

The canonical contract has no covenant yet. Do not create one until the provider identifies a service it operates and public evidence origins that honestly represent provider status/capacity, an independent probe, and any dependencies. The connected wallet is not a substitute for those facts. The app and chain are deployed and verified; no protocol write has been submitted.

## Safe execution sequence

1. Inspect sources and authorize each HTTPS origin for its real evidence class.
2. Ask the provider wallet to approve `create_covenant` and fund the bond.
3. Demonstrate deterministic refusal with an impossible request; verify it reserves nothing and increments `prevented`.
4. Use a distinct-source request supported by current, healthy evidence; obtain wallet approval, run consensus, and verify state after refresh.
5. Exercise change preflight with a real future notice and evidence before the window.
6. Run the post-failure path only if a genuine measured miss occurs within the active reservation window.
7. Re-fetch final state, settlement certificate, and accounting invariant after each completed step.

Do not create synthetic history, label provider-controlled evidence independent, fabricate an outage, or infer a successful execution from transaction finality alone. See [review evidence](REVIEW_EVIDENCE.md) for actual transactions; unexecuted paths are marked explicitly.
