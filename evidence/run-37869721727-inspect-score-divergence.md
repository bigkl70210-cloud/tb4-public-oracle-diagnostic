# TB4 Inspect-Harbor execution #3 — terminal forensic receipt (2026-10-09)

**TERMINAL_DISPOSITION=CLOSED_FAILED_SCORE_DIVERGENCE / OWNER_ONE_NEW_RUN_AUTH_CONSUMED / NO_REPLAY / NO_SUBSYSTEM_SWAP**

## Exact identity
- Public repository: `bigkl70210-cloud/tb4-public-oracle-diagnostic`
- New and only approved execution #3: [GitHub Actions run 37869721727](https://github.com/bigkl70210-cloud/tb4-public-oracle-diagnostic/actions/runs/37869721727), run number **3**, run attempt **1**.
- Trigger workflow commit: `e26f09b2ede5e47bc987e1fd611e4526dbdfd5db`; workflow blob `34928f1b828adf67a09a743590170c8bde63b275`.
- GitHub status `completed`, conclusion `failure`, runner job `113624769449`.
- Previous runs **37814221257** completed success and **37816598094** completed failure are historical CLOSED/NONREPLAY; neither was retried. The approved new one-shot is now consumed.

## What truly ran
- Linux/Docker host and public/no-model-key guards: PASS.
- Offline source checker + Inspect AST regressions: `Ran 44 tests in 0.019s`, `OK`.
- Immutable official source/pins verified: Terminal-Bench `452bf305c6daa62fc59061d22133a7cbc7c1572e`, Harbor `4b94505a91c5ddcb70b5740ac95718ddee13e5a0`, Inspect-Harbor `18230ae283a8d43f57523764ee2f744010f5f8ae`.
- Harbor `0.24.0`, Inspect-AI `0.3.277`, pinned Inspect-Harbor install/import: PASS.
- Inspect task `terminal-bench/interleaved-vigenere`, `oracle`, Docker image build PASS, Inspect eval rendered model `none/none`.
- `harbor_scorer` recorded **0.0**. Script emitted `INSPECT_NATIVE_REWARD_COMPARE interleaved-vigenere oracle: inspect=0.0 prereg_native=1.0` then fail-closed `BOUNDED_SCORE_CONTRAST_FAILED interleaved-vigenere/oracle`.
- Native Harbor Oracle 1.0 for same frozen task is from **prior** successful run 37814221257; it was not repeated in run #3.
- Remaining three Inspect arms (first-task nop; session-window-debug oracle/nop) **NOT_RUN** because the first actual score comparison failed, as predeclared fail-closed.
- No official Inspect `.eval` log was uploaded as a GitHub artifact (**artifact list empty**). GitHub job stdout includes the score and failure, but not the verifier's `Score.explanation` (e.g. test exit code and stderr). Root cause is **NOT_YET_PROVEN**.

## Mechanism-level candidate (NOT a verdict)
- The exact pinned TB4 task's `tests/test.sh` calls `pytest --ctrf /logs/verifier/ctrf.json` and writes a 0/1 reward according to the outcome.
- Its agent `environment/Dockerfile` uses Python 3.13 slim and installs certificates and `wamerican`, with **no explicit pytest installation**.
- The exact pinned Inspect-Harbor scorer runs verifier tests via `sandbox().exec` inside the **agent environment**, even for Harbor `verifier.environment_mode = "separate"`.
- Therefore missing pytest or its CTRF option/dependencies in the Inspect agent image is a **plausible high-priority cause** of the 0.0. It is *not* established, because the verifier's stderr from the Inspect EvalLog was not retained in this run. Other differences in environment/tooling remain possible.
- Score mismatch is material, but this one observation does **not** establish an LLM performance result, the causal root of the adapter failure, native-to-Inspect verifier isolation parity, artifact/error parity, or full benchmark acceptance.

## Safe corrective action without another run
- Post-run, source-only commit `97c90588295b73ac8adaf5ce2da24bd44e6ee286` adds bounded **category-only** extraction of the scorer explanation on a future score mismatch (e.g. `PYTEST_ABSENT_IN_INSPECT_SANDBOX`, `PYTEST_CTRF_OPTION_UNAVAILABLE`). It does not alter scoring, score expectations, frozen tasks, or upstream code; never emits arbitrary raw stdout/stderr.
- That source-only change does not touch `.github/workflows/tb4-native-once.yml`, so there was **no additional Action trigger**. Subsequent exact run count was **3**, with #3 completed failure.
- A hypothetical future trial must seek **fresh explicit Owner authorization**, decide whether another run has positive decision value under Ecosystem Portfolio Limit v5, capture and adjudicate the actual Inspect EvalLog/verifier explanation, and preserve the native task and scorer unchanged. Do not patch upstream tasks to force a pass, rescore into CONF, invoke paid providers, or promote a subsystem swap.
