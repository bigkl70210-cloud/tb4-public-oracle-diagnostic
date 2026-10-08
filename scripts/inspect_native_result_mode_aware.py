#!/usr/bin/env python3
"""Read-only Harbor trial contract validator. Does not compute a score.

Pass an explicit task-derived verifier mode; never assume all tasks use separate.
Ambiguous or invalid evidence fails closed; no model/provider calls.
"""
import argparse
import json
import math
from pathlib import Path

def inspect(job_dir: Path, agent: str, expected_reward: int, expected_mode: str) -> dict:
    if agent not in ("oracle", "nop") or expected_reward not in (0, 1):
        raise ValueError("CHECKER_INVALID_EXPECTATION")
    if expected_mode not in ("shared", "separate"):
        raise ValueError("CHECKER_INVALID_EXPECTED_MODE")
    if not job_dir.is_dir():
        raise ValueError("CHECKER_JOB_DIR_MISSING")
    trial_results = []
    for path in sorted(job_dir.rglob("result.json")):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            raise ValueError(f"CHECKER_CORRUPT_RESULT_JSON:{path}") from exc
        if isinstance(parsed, dict) and "trial_name" in parsed:
            trial_results.append((path, parsed))
    if len(trial_results) != 1:
        raise ValueError(f"CHECKER_TRIAL_COUNT_INDETERMINATE:{len(trial_results)}")
    _, result = trial_results[0]
    info = result.get("agent_info")
    if not isinstance(info, dict) or info.get("name") != agent:
        raise ValueError("CHECKER_WRONG_AGENT")
    if result.get("verifier_environment_mode") != expected_mode:
        raise ValueError("CHECKER_VERIFIER_MODE_MISMATCH")
    if result.get("exception_info") is not None:
        raise ValueError("CHECKER_TRIAL_EXCEPTION")
    verifier = result.get("verifier_result")
    rewards = verifier.get("rewards") if isinstance(verifier, dict) else None
    if not isinstance(rewards, dict) or len(rewards) != 1:
        raise ValueError("CHECKER_REWARD_ABSENT_OR_AMBIGUOUS")
    reward = next(iter(rewards.values()))
    if isinstance(reward, bool) or not isinstance(reward, (int, float)) or not math.isfinite(reward):
        raise ValueError("CHECKER_REWARD_INVALID_TYPE")
    if float(reward) != float(expected_reward):
        raise ValueError("CHECKER_REWARD_EXPECTATION_MISMATCH")
    return {"agent": agent, "mode": expected_mode, "reward": float(reward),
            "evidence": "HARBOR_NATIVE_TRIAL_JSON", "scientific_authority": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("agent", choices=["oracle", "nop"])
    parser.add_argument("expected_reward", type=int, choices=[0, 1])
    parser.add_argument("expected_mode", choices=["shared", "separate"])
    args = parser.parse_args()
    result = inspect(args.job_dir, args.agent, args.expected_reward, args.expected_mode)
    print(json.dumps(result, sort_keys=True))
    print("CHECKER_CONTRACT_PASS_NONSCIENTIFIC", flush=True)

if __name__ == "__main__":
    main()
