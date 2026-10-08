"""Offline regression tests for the bounded, non-scoring Harbor result checker."""
import json
import tempfile
import unittest
from pathlib import Path
from inspect_native_result_mode_aware import inspect, expected_verifier_mode

def trial(reward=1, mode="shared", agent="oracle", exception=None):
    return {"trial_name": "one", "agent_info": {"name": agent},
            "verifier_environment_mode": mode, "exception_info": exception,
            "verifier_result": {"rewards": {"reward": reward}}}

class ModeAwareCheckerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.write(trial())
    def write(self, obj, name="one/result.json"):
        path = self.folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj), encoding="utf-8")
    def fails(self, reason, *, agent="oracle", reward=1, mode="shared"):
        with self.assertRaisesRegex(ValueError, reason):
            inspect(self.folder, agent, reward, mode)
    def test_01_hello_shared_pass(self):
        self.assertEqual(inspect(self.folder, "oracle", 1, "shared")["reward"], 1)
    def test_02_tb4_separate_pass(self):
        self.write(trial(mode="separate"))
        self.assertEqual(inspect(self.folder, "oracle", 1, "separate")["mode"], "separate")
    def test_03_nop_zero_pass(self):
        self.write(trial(reward=0, mode="separate", agent="nop"))
        self.assertEqual(inspect(self.folder, "nop", 0, "separate")["reward"], 0)
    def test_04_wrong_mode_fails(self):
        self.fails("VERIFIER_MODE_MISMATCH", mode="separate")
    def test_05_wrong_agent_fails(self):
        self.fails("WRONG_AGENT", agent="nop")
    def test_06_wrong_reward_fails(self):
        self.fails("EXPECTATION_MISMATCH", reward=0)
    def test_07_duplicate_trial_fails(self):
        self.write(trial(), "two/result.json")
        self.fails("TRIAL_COUNT_INDETERMINATE")
    def test_08_malformed_json_fails(self):
        (self.folder / "one/result.json").write_text("{broken")
        self.fails("CORRUPT_RESULT_JSON")
    def test_09_missing_trial_fails(self):
        (self.folder / "one/result.json").unlink()
        self.fails("TRIAL_COUNT_INDETERMINATE")
    def test_10_reported_exception_fails(self):
        self.write(trial(exception={"exception_type": "RuntimeError"}))
        self.fails("TRIAL_EXCEPTION")
    def test_11_nan_reward_fails(self):
        self.write(trial(reward=float("nan")))
        self.fails("REWARD_INVALID_TYPE")
    def test_12_bool_reward_fails(self):
        self.write(trial(reward=True))
        self.fails("REWARD_INVALID_TYPE")
    def test_13_multiple_reward_keys_fail(self):
        self.write({**trial(), "verifier_result": {"rewards": {"a": 1, "b": 0}}})
        self.fails("ABSENT_OR_AMBIGUOUS")
    def test_14_aggregate_plus_trial_pass(self):
        self.write({"trials": []}, "result.json")
        self.assertEqual(inspect(self.folder, "oracle", 1, "shared")["reward"], 1)
    def test_15_invalid_expected_mode_fails(self):
        self.fails("INVALID_EXPECTED_MODE", mode="unknown")
    def test_16_corrupt_extra_json_fails(self):
        self.write(trial(), "two/result.json")
        (self.folder / "two/result.json").write_text("{broken")
        self.fails("CORRUPT_RESULT_JSON")
    def test_21_nonreward_key_rejected(self):
        self.write({**trial(), "verifier_result": {"rewards": {"other_key": 1}}})
        self.fails("ABSENT_OR_AMBIGUOUS")
    def test_22_unknown_frozen_task_rejected(self):
        p = self.folder / "unknown.toml"
        p.write_text('[task]\nname = "unknown/task"\n[verifier]\n')
        with self.assertRaisesRegex(ValueError, "CHECKER_UNKNOWN_FROZEN_TASK"):
            expected_verifier_mode(p)
    def test_23_wrong_mode_for_known_task_rejected(self):
        p = self.folder / "mode.toml"
        p.write_text('[task]\nname = "harbor/hello-alpine"\n[verifier]\nenvironment_mode = "separate"\n')
        with self.assertRaisesRegex(ValueError, "CHECKER_FROZEN_TASK_MODE_CONFLICT"):
            expected_verifier_mode(p)
    def test_24_missing_source_identity_rejected(self):
        p = self.folder / "missing.toml"
        p.write_text('[verifier]\n')
        with self.assertRaisesRegex(ValueError, "CHECKER_UNKNOWN_FROZEN_TASK"):
            expected_verifier_mode(p)

    def test_17_task_source_default_shared(self):
        p = self.folder / "hello.toml"
        p.write_text('[task]\nname = "harbor/hello-alpine"\n[verifier]\ntimeout_sec = 120\n')
        self.assertEqual(expected_verifier_mode(p), "shared")
    def test_18_task_source_explicit_separate(self):
        p = self.folder / "tb4.toml"
        p.write_text('[task]\nname = "terminal-bench/interleaved-vigenere"\n[verifier]\nenvironment_mode = "separate"\n')
        self.assertEqual(expected_verifier_mode(p), "separate")
    def test_19_invalid_source_toml_fails(self):
        p = self.folder / "bad.toml"
        p.write_text("broken = [")
        with self.assertRaisesRegex(ValueError, "CHECKER_SOURCE_TOML_INVALID"):
            expected_verifier_mode(p)
    def test_20_unsupported_source_mode_fails(self):
        p = self.folder / "bad_mode.toml"
        p.write_text('[task]\nname = "harbor/hello-alpine"\n[verifier]\nenvironment_mode = "nonsense"\n')
        with self.assertRaisesRegex(ValueError, "CHECKER_UNSUPPORTED_SOURCE_MODE"):
            expected_verifier_mode(p)

if __name__ == "__main__":
    unittest.main()
