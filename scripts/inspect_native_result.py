#!/usr/bin/env python3
"""Read-only inspection of native Harbor trial result JSON. NOT a scorer."""
import json
import sys
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("Usage: inspect_native_result.py JOB_DIR AGENT EXPECTED_REWARD")

folder = Path(sys.argv[1])
agent = sys.argv[2]
expected = int(sys.argv[3])
if agent not in ("oracle", "nop") or expected not in (0, 1):
    raise SystemExit("Invalid preregistered arm")
results = []
for path in folder.rglob("result.json"):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        continue
    if isinstance(data, dict) and "trial_name" in data:
        results.append((path, data))
if len(results) != 1:
    print(f"NATIVE_RESULT_INDETERMINATE: expected one trial, found {len(results)}")
    raise SystemExit(4)
_, data = results[0]
exception = data.get("exception_info")
verifier = data.get("verifier_result")
mode = data.get("verifier_environment_mode")
agent_info = data.get("agent_info") or {}
actual_agent = agent_info.get("name")
rewards = verifier.get("rewards") if isinstance(verifier, dict) else None
print(f"TRIAL_AGENT={actual_agent} SEPARATE_VERIFIER={mode}")
print(f"EXCEPTION_TYPE={exception.get('exception_type') if isinstance(exception, dict) else 'NONE'}")
print(f"NATIVE_REWARDS={rewards}")
if actual_agent != agent or mode != "separate" or exception is not None:
    raise SystemExit("NATIVE_RESULT_INDETERMINATE_OR_ERROR")
if not isinstance(rewards, dict) or len(rewards) != 1:
    raise SystemExit("NATIVE_REWARD_MISSING_OR_AMBIGUOUS")
value = next(iter(rewards.values()))
if not isinstance(value, (int, float)) or float(value) != float(expected):
    raise SystemExit(f"NATIVE_REWARD_DID_NOT_MATCH_PREREG_EXPECTED_{expected}")
print("NATIVE_ARM_OBSERVED_EXPECTED_REWARD; NOT SCIENTIFIC_AUTHORITY")
