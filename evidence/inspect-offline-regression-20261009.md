# Inspect-Harbor offline regression closure — 2026-10-09

## Disposition
**OFFLINE_STATIC_CONTRACT_VALIDATED / NO_RUNTIME_PARITY / NO_GHA_REPLAY / NO_PROVIDER_MODEL / NO_SUBSYSTEM_SWAP**

- Read the exact tracked GitHub source using the connected GitHub integration and independently reconstructed the two files in the offline Python 3.13.5 container; verified byte-identical Git blob SHA-1 values before running tests:
  - `scripts/inspect_harbor_bounded.py`: blob `0c4352e2f4c9cb86b7d6249bcda3835d7e4e362e` (5,894 bytes).
  - `scripts/test_inspect_harbor_static_contract.py`: blob `5cf78ae146bf5704582c4f3ca2adbde844c82eea` (5,950 bytes).
- Executed actual `python -m unittest -v test_inspect_harbor_static_contract.py` against those byte-identical files. **20 tests run; 20 PASS; 0 failures / 0 errors.** The test uses Python AST extraction of two pure comparator functions; it did not import Inspect/Docker/Harbor, launch a container, or make a provider call.
- Mutant checks use the same 20-case suite, one source mutation at a time: `spec.type -> spec.name`, network denial replaced with `bridge`, exact scorer-name check weakened to substring matching, explicit `model=None` replaced by a model string. **4/4 disruptive mutants KILLED** (test suite exited nonzero).
- Neutral comment-only mutation **PASS**, distinguishing behavioral failure from ordinary file change.
- Official Inspect AI current `src/inspect_ai/_eval/eval.py` docs for `eval(model=None)` explicitly say that None disables ambient `INSPECT_EVAL_MODEL` default, leaving model use to custom tasks. The no-op and oracle solvers do not invoke model generation, but provider-independent runtime execution is still NOT ATTESTED.
- Existing native result checker 24 offline tests were already reported PASS in the predecessor repair and are not the same as these 20 new tests.
- The pinned Inspect-Harbor v1.0.0 scorer performs verifier commands in the agent sandbox, and its selective worktree reset is not equivalent to an independent native separate verifier. Even future Inspect reward matches could show **bounded score compatibility only**, not error/artifact/isolation parity.
- Last observed GitHub Actions execution count: **2**, run 37814221257 completed success NONREPLAY; run 37816598094 completed failure due to a checker false-negative (native official `hello-alpine` Oracle reward 1.0, no exception), NONREPLAY. Inspect four-arm runtime **NOT RUN**.
- Existing trigger-bearing `.github/workflows/tb4-native-once.yml` remains unchanged and bound to run_number 2; current source repairs are **dormant** and not integrated into a live workflow. A new Actions execution requires fresh explicit Owner authorization; bare `ㄱㄱ` is not authorization.
- Network/mount/secret checks remain config-only, not verified Docker runtime properties. No model, model ranking, scientific scorer/bank authority, or subsystem replacement promoted.

## Next authorized no-spend route
No further generic static framework expansion merely to increase test count. Retain new tests and the existing native receipt. When a new one-shot external execution is explicitly authorized, first separately and safely wire the new source and offline tests to the intended workflow with an exact future-run gate, then verify official pinned Docker+Inspect runtime and its actual evidence limits. Do not replay old run IDs or Issue88 authority.
