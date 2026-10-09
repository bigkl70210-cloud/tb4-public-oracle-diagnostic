# TB4 GPT-6.1 Sol one-shot #4 — terminal receipt (2026-10-09)

- **Owner authorization:** 1 new GitHub Actions run; one GPT-6.1 Sol / Codex trial on official frozen TB4 session-window-debug; previous target <=USD2, Owner accepts possible spend up to USD5 (not an absolute enforceable cutoff). Existing Meta Q1 key to be referenced only from scoped tb4-once environment.
- **New public workflow commit:** `89c19b8c5aa7dc730588983e5f5e9fd11dba33a4`.
- **Action run:** https://github.com/bigkl70210-cloud/tb4-public-oracle-diagnostic/actions/runs/37884327281
- **Actions outcome:** COMPLETED / FAILURE. First attempt. Non-replay.
- **Successful stages:** Ubuntu/Docker one-shot preflight; exact pinned official TB4+Harbor sources; Harbor installation; network allowlist overlay preparation.
- **Failed stage:** native Codex execution command returned `HARBOR_PROCESS_EXIT=2` immediately before any native trial result.
- **Receipt:** `native_result_found=false`, `reward=null`, `exception_type=null`, `agent=null`. This is not a model failure score and is not a zero reward.
- **Identified immediate command defect:** workflow passed `--agent-timeout 720`. At pinned Harbor source `4b94505a91c5ddcb70b5740ac95718ddee13e5a0`, the official `harbor run` CLI does not define `--agent-timeout` but does define `--agent-timeout-multiplier`. Fast exit code 2 and absent native result strongly support CLI parser rejection. This causal diagnosis is source-bounded; original stderr was redirected to ephemeral runner file and was not uploaded.
- **Model API:** No completed model trial and no confirmed provider call. Actual Platform-billed usage has not been independently checked; do not assert exact USD0 from the absent trial.
- **Follow-up:** inert research-only branch `research/tb4-sol-run4-cli-fix-inert-20261009` replaces unsupported flag with `--agent-timeout-multiplier 0.025`, yielding 720s from frozen task 28,800s base. No main-branch workflow change, no new Action, and no automatic rerun authorized by this patch.
- **Old Actions #1/#2/#3:** CLOSED/NONREPLAY unchanged.
- **Disposition:** RUN_37884327281_CLOSED_FAILED_CLI_PRETRIAL_NONREPLAY; code repair INERT; scientific claim ceiling unchanged; no model promotion. New material execution requires a new exact Owner authorization and separate safety/currentness preflight.
