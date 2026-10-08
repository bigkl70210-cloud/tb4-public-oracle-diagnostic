#!/usr/bin/env python3
"""One authorized no-model Inspect-Harbor v1.0.0 compatibility run.

No registry downloads, model calls, scorer edits, or trial retries.
The two upstream Terminal-Bench task directories are unchanged.
Inspect's verification sandbox differs from native Harbor separate mode;
observed score equality is NOT full verifier-isolation parity.
"""
import json
import math
import os
import sys
from pathlib import Path

from inspect_ai import eval as inspect_eval
from inspect_ai.solver import solver
from inspect_harbor import harbor, oracle

TASKS = ("interleaved-vigenere", "session-window-debug")
if os.environ.get("INSPECT_HARBOR_NO_TELEMETRY") != "1":
    raise SystemExit("Telemetry flag not disabled")
if any(os.environ.get(k) for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY")):
    raise SystemExit("Unexpected model provider credential")

@solver
def nop():
    async def solve(state, generate):
        # No generation, shell access, mutation, or external API call.
        return state
    return solve

def enforce_no_network(task):
    # This is a stricter runtime restriction than the unchanged upstream
    # task.toml. It does NOT certify full native-vs-Inspect fidelity.
    samples = list(task.dataset)
    if len(samples) != 1:
        raise RuntimeError(f"Expected one immutable sample, saw {len(samples)}")
    cfg = samples[0].sandbox.config
    if not getattr(cfg, "services", None):
        raise RuntimeError("Missing Docker Compose service definitions")
    for name, svc in cfg.services.items():
        if getattr(svc, "networks", None):
            raise RuntimeError(f"Explicit network attached: {name}")
        if getattr(svc, "ports", None):
            raise RuntimeError(f"Published port present: {name}")
        svc.network_mode = "none"
        if svc.network_mode != "none":
            raise RuntimeError(f"Network deny failed for {name}")
    print("INSPECT_COMPOSE_NETWORK_MODE_NONE_CONFIGURED", flush=True)

def inspect_score(log):
    if getattr(log, "status", None) != "success":
        raise RuntimeError(f"Inspect evaluation not successful: {log.status}")
    samples = getattr(log, "samples", None)
    if not samples or len(samples) != 1:
        raise RuntimeError("Inspect did not return exactly one sample")
    scores = samples[0].scores
    if not scores or len(scores) != 1:
        raise RuntimeError(f"Inspect scorer count indeterminate: {scores}")
    key, score = next(iter(scores.items()))
    if "harbor" not in key.lower():
        raise RuntimeError(f"Unexpected scorer identity: {key}")
    value = score.value
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise RuntimeError(f"Non-finite or non-numeric Inspect reward: {value}")
    return float(value)

def main():
    root = Path("terminal-bench-source/tasks")
    observations = []
    for slug in TASKS:
        task_dir = root / slug
        if not task_dir.is_dir():
            raise RuntimeError(f"Missing frozen task {slug}")
        for name, solver_fn, expected in (
            ("oracle", oracle, 1.0),
            ("nop", nop, 0.0),
        ):
            task = harbor(path=task_dir)
            enforce_no_network(task)
            print(f"INSPECT_START {slug} {name}", flush=True)
            logs = inspect_eval(
                task,
                solver=solver_fn(),
                log_dir=str(Path("inspect-logs") / slug / name),
                max_samples=1,
            )
            if len(logs) != 1:
                raise RuntimeError(f"Expected one Inspect log, got {len(logs)}")
            result = inspect_score(logs[0])
            observations.append({"task": slug, "agent": name,
                                 "inspect_reward": result, "expected": expected})
            print(f"INSPECT_NATIVE_REWARD_COMPARE {slug} {name}: "
                  f"inspect={result} prereg_native={expected}", flush=True)
            if result != expected:
                raise RuntimeError(f"BOUNDED_SCORE_CONTRAST_FAILED {slug}/{name}")
    Path("inspect-results.json").write_text(
        json.dumps({"inspect_harbor_pin": "18230ae283a8d43f57523764ee2f744010f5f8ae",
                    "terminal_bench_pin": os.environ["TB_PIN"],
                    "observations": observations,
                    "limits": ["Inspect separate-verifier semantics not established",
                               "Network config asserted; effective mount/secret/egress attestation incomplete",
                               "No scientific model claim or subsystem swap"]},
                   indent=2) + "\n", encoding="utf-8")
    print("INSPECT_4_ARM_REWARD_COMPATIBILITY_BOUNDED_PASS_NO_MODEL", flush=True)

if __name__ == "__main__":
    main()
