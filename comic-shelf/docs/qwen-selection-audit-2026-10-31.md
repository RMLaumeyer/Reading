# Qwen selection audit experiment — October 31, 2026

Tested a bounded second Qwen pass on the same ten saved sentence-selection cases. The audit received the original selected IDs and the complete original candidate list, and could return a replacement selection of zero to three existing IDs. It returned exactly the same synopsis and evidence in all ten cases. Do not enable this audit by default: it added ten model calls and 70.32 worker seconds without reducing editorial work.

| Fixed ten-case cohort | Editorial passes unchanged | Extra calls after saved baseline |
| --- | ---: | ---: |
| Original sentence selection | 4/10 | 0 |
| Adjacent-passage block experiment | 3/10 | 10 |
| Selection followed by this audit | 4/10 | 10 |

The audit had no observed improvements or regressions. It also left the six previously identified editorial problems unchanged, including missing setup/context, source text damage and omitted threads. An empty change list is not independent confirmation of correctness. Showing the previous selection may anchor the second pass; this trial does not isolate that effect or establish that every possible review prompt would fail.

## Experiment boundaries

The trial used qwen3.5-4b, temperature zero, thinking off and a 200-token structured-ID response budget. The audit instructions asked it to check named participants, central problems, pronouns, distinct threads, uncertainty, promotion, repetition and damaged source text. It could select only existing excerpt IDs. The existing worker validated the returned schema, ID count, uniqueness, source order and literal quotations.

No rewritten synopsis, editorial correction, assessment label or website annotation was included in the model input. The audit's actual request bodies were preserved separately from the worker's standard selection log, so the initial selection supplied to the model is auditable. The system prompt hash matches the audit prompt, and the input candidate payloads match the original run's actual candidate payloads exactly.

This was an isolated artifact-based prototype. It did not add a production audit option or change the default worker. The existing opt-in block mode remains experimental; ordinary sentence selection remains the default. An experiment result's draft status is not publication eligibility: current manual source and edition holds still apply independently.

The cohort is reused development data assessed by Codex under user delegation, not independent gold data. Original selection preceded the audit; order was not randomized and requests were not repeated. Identical outputs describe this run, not a general guarantee of deterministic output or proof that the model assessed the faults correctly.

## Verification

All ten audit requests completed without worker failures. All 26 selected evidence quotations are literal source text. Verified actual request bodies, model configuration, prompt hashes, packet and parent-result hashes, frozen code, identical candidate inputs and unchanged inventories. All ten synopsis/evidence objects exactly match their saved originals, so their existing editorial assessments remain applicable without inventing new labels.

Production code did not change in this experiment. The prior 355-test validation remains applicable; the broad suite was not repeated for the artifact-only runner. Exact before/after hashes confirm that canonical, public and built enrichment files are unchanged. No new synopsis was published and the approved total remains 123.

Artifacts are in data/local-ai-trials/selection-audit-ten-20261031: run.py, frozen manifest/packets/code, actual request bodies and responses, report.json, changed-assessments.json, assessment.json and verification.json. Original control cases remain in selection-check-fresh-ten-20261031.

## Working decision

Keep the single-pass selector and explicit source/editorial review. The tested longer-prompt, rewriting, fixed-block and audit variants do not justify changing the default. Cleaner source records can repair text damage, but the separate source comparison did not improve the two tested selections' coverage. Further runs of the same setup should not be presented as progress toward autonomous publication. A future change needs a concrete new hypothesis and a bounded comparison showing that it actually saves review work.
