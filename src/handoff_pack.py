"""Local handoff-envelope serializer.

Verification booleans are caller assertions unless independently checked by a
separate verifier. This module does not itself authenticate files or test runs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

EVIDENCE_STATE = "LOCAL_OPERATOR_HYGIENE_NOT_XAI_GROK_OR_AGENT_RUNTIME_AUTHORITY"


@dataclass
class HandoffPackage:
    task_name: str
    modified_files: list[str] = field(default_factory=list)
    tests_passed: bool = False
    sha256_verified: bool = False

    def __post_init__(self) -> None:
        if not self.task_name:
            raise ValueError("task_name is required")
        if not all(isinstance(path, str) and path for path in self.modified_files):
            raise ValueError("modified_files must contain non-empty strings")
        if not isinstance(self.tests_passed, bool) or not isinstance(
            self.sha256_verified, bool
        ):
            raise TypeError("verification flags must be booleans")

    def compile(self) -> dict:
        ready = self.tests_passed and self.sha256_verified
        return {
            "task_name": self.task_name,
            "modified_files": list(self.modified_files),
            "tests_passed_claim": self.tests_passed,
            "sha256_verified_claim": self.sha256_verified,
            "handoff_status": "CALLER_ASSERTS_READY"
            if ready
            else "EVIDENCE_INCOMPLETE",
            "verification_source": "CALLER_SUPPLIED",
            "evidence_state": EVIDENCE_STATE,
            "operational_authority": False,
        }

    def to_json(self) -> str:
        return json.dumps(self.compile(), indent=2, sort_keys=True)
