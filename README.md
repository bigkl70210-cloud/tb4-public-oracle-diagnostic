# TB4 public native Docker diagnostic (one-shot)

This repository contains **public-only diagnostics** for unmodified official Terminal-Bench v4.0.0 task sources and the pinned official Harbor runtime. It does **not** contain private benchmark/META assets, credentials, model API calls, proprietary adapters, or user files.

## Frozen upstream inputs
- Official Terminal-Bench commit: `452bf305c6daa62fc59061d22133a7cbc7c1572e`
- Official Harbor v0.24.0 commit: `4b94505a91c5ddcb70b5740ac95718ddee13e5a0`
- Unmodified tasks: `interleaved-vigenere`, `session-window-debug`
- Native agents: built-in `oracle` (expect reward 1) and `nop` (expect reward 0), each **one attempt, zero retries**
- Native Harbor Docker environment and **separate** verifier as encoded in the original task TOMLs

## Governance / interpretation
Only the official native Harbor verifier creates a reward. The tiny Python inspector reads its `result.json` and rejects absent, ambiguous, exceptional or nonmatching results; it is **not** an alternative scorer. This workflow is a substrate/oracle/nop diagnostic, **not a model benchmark, scientific authority, native parity proof, or authorization to retry a prior run**. No result is promoted to a benchmark conclusion.

Runs are limited to a standard `ubuntu-24.04` GitHub-hosted runner for a **public repository**. No secrets, tokens for hosted models, external paid compute, third-party model APIs, or uploads of private files are required. No Actions artifact uploads or caches are configured.

The workflow is restricted to the one commit that initially adds its workflow file; there is no scheduled trigger. **Do not rerun a failed or indeterminate workflow without an explicit new authorization.**

## Local PC
The Owner's Windows PC is excluded from this diagnostic. Its earlier `VirtualMachinePlatform` change needs rollback on a successful Windows boot; nothing in this repository runs on that PC.
