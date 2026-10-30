# Synopsis decisions and corrections

`scripts/review_decisions.py` records review events separately from frozen source packets, Qwen results and review queues. Each event has a timestamp, unique ID, queue SHA-256, reviewer identity/kind, rationale, original proposal, and any corrected text with exact source quotations. Repeated reviews create new files; the latest event is used in the summary while earlier decisions remain available.

Actions: `accept`, `revise`, `reject`, `needs_research`. Acceptance applies to a synopsis only. Existing edition/contents flags remain visible and every event retains `readyForPublication: false`. A correction requires source evidence, but matching quotations does not prove the prose follows from them; the reviewer must check that. Assistant assessments are explicitly labeled and never count as independent human review.

## Exercised on the ten-book queue

Five assistant assessments are saved in `data/local-ai-trials/worker-review-20261030/assistant-decisions`; the other five remain unreviewed. The frozen queue hash was verified unchanged after recording decisions.

| Edition | Assistant decision |
| --- | --- |
| Blade: Evil Against Evil | Accept main-premise excerpt as a synopsis draft |
| Moon Knight: God & Country | Accept source-excerpt synopsis draft |
| Doom Treasury Edition | Accept main-story premise draft; no exhaustive extras claim |
| Doctor Strange: The Way of the Weird | Revise to “Doctor Strange confronts supernatural threats as the cost of using magic comes due.” |
| Star-Lord & Kitty Pryde | Revise to restore Age of Apocalypse Kitty's distinction and Battleworld survival premise |

These assessments exercise the workflow and implement prior editorial findings. They are not new Qwen outputs, independent validation, human approval, or publication. Source-backed corrections are available in `assistant-assessment.json` with the original proposals and cited evidence.

## Record a decision

Save a JSON input such as:

```json
{
  "isbn": "9781302529567",
  "action": "accept",
  "reviewer": "Your name",
  "reviewer_kind": "human",
  "reason": "Checked the full description and accepted the central premise."
}
```

Then run from the project directory:

```powershell
python scripts/review_decisions.py --queue data/local-ai-trials/worker-review-20261030/review-queue.json --decisions data/local-ai-trials/worker-review-20261030/human-decisions --input decision.json
```

For revisions add `correction` (text) and `evidence` (a list of objects containing `source` and verbatim `quote`). Omit `--input` to print the latest summary for the specified decision directory. Keep assistant and human review streams separate when assessing performance.

Four tests pass: append-only history/source preservation, revision evidence rejection, changed-queue rejection, and empty-proposal rejection. Existing source files and website data are untouched. Future work can use these decisions to choose cases needing research and quantify correction effort; the present workflow does not measure reviewer time or publish accepted drafts.
