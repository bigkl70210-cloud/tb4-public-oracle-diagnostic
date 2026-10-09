# OpenHands v1.53.0 SDK pinned no-model smoke — one-shot receipt

**Status:** COMPLETED_SUCCESS / CONSUMED_NONREPLAY / SDK_SMOKE_PASS_BOUNDED  
**Owner-authorized scope:** One isolated public GitHub Actions run to install the official OpenHands SDK and run a no-model smoke test. No model API, secrets/private data, operational harness replacement or provider dispatch.  
**Date:** 2026-10-10 KST  
**Workflow:** [openhands-sdk-v153-smoke-once.yml](../.github/workflows/openhands-sdk-v153-smoke-once.yml)  
**Execution:** [run 37955328482](https://github.com/bigkl70210-cloud/tb4-public-oracle-diagnostic/actions/runs/37955328482), attempt 1, event push, conclusion success, UTC 2026-10-09T15:55:36Z–15:55:54Z  
**Workflow commit:** `5c6caff3221263f26468b7ae8e2bada0f602032a`  
**Official upstream:** [OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk), `v1.53.0`, commit `54daf056bd863bb46f922a2fe9324dd736b37ff6` (exact HEAD verified)
**Environment:** isolated GitHub-hosted `ubuntu-24.04` job; Python 3.13.16; upstream native `uv.lock` with `uv sync --frozen --no-dev --package openhands-sdk --python 3.13` and 126 packages installed.  
**Model calls:** 0 by program path and absent provider variables; no LLM constructed/executed. No secrets referenced or transmitted in workflow. No private repository checkout. No operation on production/operational harness.

## Passed native smoke checks

1. Installed `openhands-sdk` reports version 1.53.0.
2. Native `MessageEvent` roundtrips through typed `Event` JSON.
3. Native `EventLog` appends and reopens with `InMemoryFileStore`.
4. Native `LocalFileStore` writes, reads and persists a temporary file.
5. Native `EventLog` appends and reopens across new `LocalFileStore` instances.
6. Native `LocalFileStore` rejects `../` traversal.
7. Socket-level per-process network guard denies a TCP connection attempt.
8. Common provider API-key environment variables absent.

**Boundary observation:** On SDK import, LiteLLM attempted to fetch an *external public model-cost map*. The smoke process's network guard blocked this and LiteLLM fell back to its local backup. This was NOT a model API call. The guard is Python-process scoped, not proof of whole-runner network-default-deny during dependency installation. Native end-to-end agent runtime and server/GUI remain **NOT_RUN**.

**Artifact:** `openhands-v153-sdk-no-model-smoke-receipt`, artifact ID `11627223940`, GitHub SHA256 digest `615a284f26e4f211f851213babb8dd2964c5b9862dbe2c06a0e4959e8260640a`; hosted retention 1 day; readback ZIP integrity PASS. The JSON content digest is `f3e7bc3a68dec233477f9e19c45ebddac5997feeca844772998ae7bd39d25eea`, matches the included `.sha256` file. JSON declares `status=PASS`, `claim_ceiling=installed_SDK_no_model_smoke_only`, `real_agent_run=false`.

**Disposition:** Software source-acquisition run `37954211466` previously SUCCESS_NONREPLAY. This smoke run `37955328482` SUCCESS_NONREPLAY, one run and one attempt. Do NOT repeat either under consumed one-shot permission. No Harbor/TB4 measured-agent run, no paid model performance result, no adoption or replacement decision, no cross-project scientific promotion. Further actual agent execution/provider calls/public workflows require their exact separate Owner authorization.
