#!/usr/bin/env python3
"""
Handoff Packager Module (src/handoff_pack.py).
Packages state, modified files, and verified observables for IC handoffs.
"""
from dataclasses import dataclass, field
import json

@dataclass
class HandoffPackage:
    task_name: str
    modified_files: list[str] = field(default_factory=list)
    tests_passed: bool = True
    sha256_verified: bool = True

    def compile(self) -> dict:
        return {
            "task_name": self.task_name,
            "modified_files": self.modified_files,
            "tests_passed": self.tests_passed,
            "sha256_verified": self.sha256_verified,
            "handoff_status": "READY_FOR_IC_HANDOFF"
        }

    def to_json(self) -> str:
        return json.dumps(self.compile(), indent=2)
