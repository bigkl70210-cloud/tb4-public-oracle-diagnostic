"""Dependency-free unit checks for the dormant Inspect-Harbor bounded comparator.

Extract only the two pure functions with AST so Inspect-AI, Docker, models and
provider credentials are not loaded. These are local contract tests, not
evidence of Inspect-Harbor execution or runtime security.
"""
import ast
import math
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

PATH = Path(__file__).with_name("inspect_harbor_bounded.py")
TREE = ast.parse(PATH.read_text(encoding="utf-8"), filename=str(PATH))
NAMES = {"enforce_no_network", "inspect_score"}
PURE = [n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
if {n.name for n in PURE} != NAMES:
    raise RuntimeError("PURE_CONTRACT_FUNCTIONS_MISSING")
NAMESPACE = {"math": math}
exec(compile(ast.Module(body=PURE, type_ignores=[]), str(PATH), "exec"), NAMESPACE)
enforce_no_network = NAMESPACE["enforce_no_network"]
inspect_score = NAMESPACE["inspect_score"]
NAME = "terminal-bench/interleaved-vigenere"


def task(**service_fields):
    service = NS(network_mode="bridge", **service_fields)
    sample = NS(id=NAME, metadata={"task_name": NAME},
                sandbox=NS(type="docker", config=NS(services={"default": service})))
    return NS(dataset=[sample]), service


def log(value=1, *, status="success", sample_id=NAME,
        scorer="harbor_scorer"):
    return NS(status=status, samples=[NS(id=sample_id,
               scores={scorer: NS(value=value)})])


class InspectStaticContractTests(unittest.TestCase):
    def test_01_frozen_single_docker_service_network_disabled(self):
        obj, service = task()
        enforce_no_network(obj, NAME)
        self.assertEqual(service.network_mode, "none")

    def test_02_sample_id_cannot_swap(self):
        obj, _ = task()
        obj.dataset[0].id = "terminal-bench/another-task"
        with self.assertRaisesRegex(RuntimeError, "SAMPLE_IDENTITY_MISMATCH"):
            enforce_no_network(obj, NAME)

    def test_03_metadata_identity_cannot_swap(self):
        obj, _ = task()
        obj.dataset[0].metadata["task_name"] = "foreign"
        with self.assertRaisesRegex(RuntimeError, "SAMPLE_IDENTITY_MISMATCH"):
            enforce_no_network(obj, NAME)

    def test_04_sandbox_must_be_docker(self):
        obj, _ = task()
        obj.dataset[0].sandbox.type = "local"
        with self.assertRaisesRegex(RuntimeError, "NOT_DOCKER"):
            enforce_no_network(obj, NAME)

    def test_05_multiple_services_rejected(self):
        obj, svc = task()
        obj.dataset[0].sandbox.config.services["sidecar"] = svc
        with self.assertRaisesRegex(RuntimeError, "SERVICE_TOPOLOGY"):
            enforce_no_network(obj, NAME)

    def test_06_host_volumes_rejected(self):
        obj, _ = task(volumes=["/host:/container"])
        with self.assertRaisesRegex(RuntimeError, "UNAPPROVED_COMPOSE_FIELD"):
            enforce_no_network(obj, NAME)

    def test_07_host_ports_rejected(self):
        obj, _ = task(ports=["8000:8000"])
        with self.assertRaisesRegex(RuntimeError, "UNAPPROVED_COMPOSE_FIELD"):
            enforce_no_network(obj, NAME)

    def test_08_privileged_rejected(self):
        obj, _ = task(privileged=True)
        with self.assertRaisesRegex(RuntimeError, "UNAPPROVED_COMPOSE_FIELD"):
            enforce_no_network(obj, NAME)

    def test_09_extra_network_mode_rejected(self):
        obj, service = task()
        service.network_mode = "host"
        with self.assertRaisesRegex(RuntimeError, "UNEXPECTED_NETWORK_MODE"):
            enforce_no_network(obj, NAME)

    def test_10_missing_sample_rejected(self):
        obj, _ = task()
        obj.dataset.clear()
        with self.assertRaisesRegex(RuntimeError, "one frozen task sample"):
            enforce_no_network(obj, NAME)

    def test_11_native_identity_scorer_reward_one(self):
        self.assertEqual(inspect_score(log(), NAME), 1.0)

    def test_12_native_identity_scorer_reward_zero(self):
        self.assertEqual(inspect_score(log(value=0), NAME), 0.0)

    def test_13_foreign_log_sample_id_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "LOG_SAMPLE_IDENTITY_MISMATCH"):
            inspect_score(log(sample_id="other"), NAME)

    def test_14_substring_spoofed_scorer_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "SCORER_IDENTITY_MISMATCH"):
            inspect_score(log(scorer="some_harbor_scorer_alias"), NAME)

    def test_15_eval_failure_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "not successful"):
            inspect_score(log(status="error"), NAME)

    def test_16_boolean_reward_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Non-finite or non-numeric"):
            inspect_score(log(value=True), NAME)

    def test_17_nan_reward_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Non-finite or non-numeric"):
            inspect_score(log(value=float("nan")), NAME)

    def test_18_multiple_scorers_rejected(self):
        x = log()
        x.samples[0].scores["other"] = NS(value=1)
        with self.assertRaisesRegex(RuntimeError, "SCORER_IDENTITY_MISMATCH"):
            inspect_score(x, NAME)

    def test_19_no_eval_samples_rejected(self):
        x = log()
        x.samples = []
        with self.assertRaisesRegex(RuntimeError, "exactly one sample"):
            inspect_score(x, NAME)


if __name__ == "__main__":
    unittest.main()
