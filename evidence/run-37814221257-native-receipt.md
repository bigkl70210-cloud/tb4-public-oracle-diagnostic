# Native TB4 oracle / nop receipt — GitHub Actions 37814221257

**Status:** CLOSED / COMMITTED / NONREPLAY. No second attempt is authorized by this receipt.

- Public GitHub Actions run: https://github.com/bigkl70210-cloud/tb4-public-oracle-diagnostic/actions/runs/37814221257
- Run attempt: **1**; workflow conclusion: **success**
- Job: `native-diagnostic` ID `113438560165`; all declared steps success
- Runner: official `ubuntu-24.04`, Docker daemon reachable, **4 CPUs**, Docker memory **16,770,748,416 bytes**
- Frozen Terminal-Bench upstream git commit: `452bf305c6daa62fc59061d22133a7cbc7c1572e`
- Frozen Harbor upstream git commit: `4b94505a91c5ddcb70b5740ac95718ddee13e5a0` (version 0.24.0)
- Sources were fetched directly from official public repositories and git SHA-checked. The original two task directories and their tests/verifier were not edited.
- Native execution: `harbor run --path <task> --agent <oracle|nop> --env docker --n-attempts 1 --max-retries 0 --n-concurrent 1`
- Native verifier mode recorded in each trial result: `separate`.
- All 4 trial results had `exception_info=None`; exactly one `reward` entry per trial.

| Task | Oracle native reward | nop native reward |
| --- | ---: | ---: |
| `interleaved-vigenere` | 1.0 | 0.0 |
| `session-window-debug` | 1.0 | 0.0 |

The source of each reward is the official Harbor native trial JSON. The checked-in inspection script **does not assign or recompute reward**. The exact result lines are visible in the public run job log under each corresponding step.

## Precisely what this run does **not** establish

- No model or provider was evaluated and no scientific performance or model-selection claim is authorized.
- **Inspect-Harbor v1.0.0** adapter paired execution and detailed parity **NOT_RUN**; Inspect parity cannot be inferred from native reward success.
- Preregistered **upstream Harbor hello-alpine Oracle smoke** **NOT_RUN**: a generic Docker `python:3.12-slim` smoke ran instead. Thus the exact all-gates completion criterion remains **PARTIAL**.
- Actual built Docker image digests, strict agent/verifier egress enforcement, and full mount/secret exposure checks were **not independently attested** by this workflow; do not treat them as passed gates.
- No model/provider API keys supplied, no paid model invocation, no unrelated private documents/repositories mounted.
- A workflow success is only a bounded native-substrate observation; no generic runner/adapter replacement, no benchmark acceptance, and no loss of frozen prior evidence.

**Disposition:** The native Oracle/nop result is a durable, independently auditable **PASS_BOUNDED**; inspect parity and remaining preregistered completion gates remain open. Any new execution is a **new attempt** and requires separately tracked Owner authorization. NEVER rerun this job to obtain a different score.
