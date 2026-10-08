# TB4 public-only Inspect source preflight — 2026-10-09

Disposition: **SOURCE_PREFLIGHT_PASS_BOUNDED / RUNTIME_NOT_RUN / OWNER_APPROVAL_CONSUMED_NONREPLAY**.

## Hard source witnesses
- Prior native Terminal-Bench frozen run **37814221257** remains completed success with 2 tasks Oracle 1 / Nop 0, NONREPLAY.
- Later GH run **37816598094** remains completed failure; native Harbor official `hello-alpine` Oracle actually reward 1, exceptions 0, verifier mode shared. The legacy checker hard-coded separate and produced a false negative; Inspect four-arm stage never ran. One-shot approval consumed.
- Pinned source: TB4 `452bf305c6daa62fc59061d22133a7cbc7c1572e`; Harbor `4b94505a91c5ddcb70b5740ac95718ddee13e5a0`; Inspect-Harbor `18230ae283a8d43f57523764ee2f744010f5f8ae`.
- Pinned Inspect-Harbor `src/inspect_harbor/_harbor/scorer.py` executes verifier tests in the agent sandbox, not a native Harbor separate-verifier Docker environment. Same reward is **bounded score compatibility only**, not native error/artifact/isolation parity.
- Official Inspect `SandboxEnvironmentSpec` field is `type`, not `name` (checked against official Inspect API source).
- Official Inspect eval documentation permits explicit `model=None` to disable the default `INSPECT_EVAL_MODEL`; our dormant Inspect script now opts out.

## Actual non-triggering source repair
- `scripts/inspect_harbor_bounded.py` latest source commit `55c03e8f279a2d8ab9c71037df86ca9dfd06332f` after identity/security fixes `939fd5b7651207798e3f6e22d105051433531240`, `238ea73b4fb8ff5024f28bbd6002617a4c6c03af`.
- Fail-closed identity checks: one pinned sample, matching sample ID and metadata task name; Docker `spec.type`; one Compose service; deny host volumes/devices/privileged/secret/env_file/extra-host/ports/networks; configure `network_mode='none'`. This is **config-only**, not runtime network or mount attestation.
- Fail-closed log checks: evaluation status success; one sample with same frozen ID; exactly named `harbor_scorer`; numeric, finite, non-boolean reward. Explicit `model=None`; no model/provider calls authorized.
- `scripts/test_inspect_harbor_static_contract.py` latest commit `2d150b6725ef2fd8da5f1c16a09aca805c75b55e`: **20 dependency-free AST/mock cases authored and GitHub readback inspected, not yet executed on GitHub runner**. No claim of 20/20 execution pass. Existing mode-aware native checker tests 24/24 had passed earlier locally and are unchanged.
- Source readback on this cutoff: 9 static invariants PASS, including source/test exact fields; workflow SHA `a1ac25030b293b150ec0fc8f28876ffde305ac9d` unchanged.
- GitHub runs count exact readback: **2**, IDs 37814221257 (completed/success) and 37816598094 (completed/failure), no third run.

## Gating limitations and safe next
- Existing `.github/workflows/tb4-native-once.yml` still invokes the **legacy** checker and is bound to `github.run_number == 2`. This trigger-bearing file MUST NOT be edited or dispatched under bare continuation; future run requires specific new Owner approval and a guarded workflow plan.
- Inspect v1.0.0 current implementation cannot establish complete native separate-verifier isolation by reward agreement. Artifact/error/isolation parity, image/mount/credential/egress runtime attestations remain OPEN. No subsystem swap, production promotion, benchmark science claim, provider dispatch, paid spend, retry or rescore.
- Additional source-only testing can be run locally if source is materialized; GitHub static tests remain NOT_RUN until executable test surface is available. Do not conflate tests being checked in with tests passing.
