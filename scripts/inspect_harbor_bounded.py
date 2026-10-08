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

def enforce_no_network(task, expected_task_name):
    """Static Compose guard on the exactly pinned one-service public task.

    This config check cannot attest image digests, effective Docker mounts,
    runtime egress, secret exposure, or native verifier isolation.
    """
    samples = list(task.dataset)
    if len(samples) != 1:
        raise RuntimeError(f"Expected one frozen task sample, saw {len(samples)}")
    sample = samples[0]
    metadata = getattr(sample, "metadata", None) or {}
    if (
        getattr(sample, "id", None) != expected_task_name
        or not isinstance(metadata, dict)
        or metadata.get("task_name") != expected_task_name
    ):
        raise RuntimeError("INSPECT_FROZEN_SAMPLE_IDENTITY_MISMATCH")
    spec = getattr(sample, "sandbox", None)
    if getattr(spec, "name", None) != "docker":
        raise RuntimeError("INSPECT_SANDBOX_NOT_DOCKER")
    cfg = getattr(spec, "config", None)
    services = getattr(cfg, "services", None)
    if not services or len(services) != 1:
        raise RuntimeError("INSPECT_UNEXPECTED_SERVICE_TOPOLOGY")
    for name, svc in services.items():
        for attr in (
            "volumes", "volumes_from", "devices", "privileged", "cap_add",
            "secrets", "env_file", "extra_hosts", "ports", "networks",
        ):
            if getattr(svc, attr, None):
                raise RuntimeError(f"INSPECT_UNAPPROVED_COMPOSE_FIELD:{name}:{attr}")
        if getattr(svc, "network_mode", None) not in (None, "bridge", "none"):
            raise RuntimeError(f"INSPECT_UNEXPECTED_NETWORK_MODE:{name}")
        svc.network_mode = "none"
        if svc.network_mode != "none":
            raise RuntimeError(f"INSPECT_NETWORK_CONFIG_DENY_FAILED:{name}")
    print("INSPECT_COMPOSE_ONE_SERVICE_NETWORK_NONE_CONFIG_ONLY", flush=True)

def inspect_score(log, expected_task_name):
    if getattr(log, "status", None) != "success":
        raise RuntimeError(f"Inspect evaluation not successful: {log.status}")
    samples = getattr(log, "samples", None)
    if not samples or len(samples) != 1:
        raise RuntimeError("Inspect did not return exactly one sample")
    sample = samples[0]
    if getattr(sample, "id", None) != expected_task_name:
        raise RuntimeError("INSPECT_LOG_SAMPLE_IDENTITY_MISMATCH")
    scores = sample.scores
    if not scores or set(scores) != {"harbor_scorer"}:
        raise RuntimeError(f"INSPECT_SCORER_IDENTITY_MISMATCH: {list(scores) if scores else scores}")
    score = scores["harbor_scorer"]
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
            enforce_no_network(task, "terminal-bench/" + slug)
            print(f"INSPECT_START {slug} {name}", flush=True)
            logs = inspect_eval(
                task,
                solver=solver_fn(),
                log_dir=str(Path("inspect-logs") / slug / name),
                max_samples=1,
            )
            if len(logs) != 1:
                raise RuntimeError(f"Expected one Inspect log, got {len(logs)}")
            result = inspect_score(logs[0], "terminal-bench/" + slug)
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
