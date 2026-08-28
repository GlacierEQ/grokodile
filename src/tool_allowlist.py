"""Deterministic local tool-name allowlist.

This module classifies caller-supplied names only. It does not execute tools or
provide an OS/process sandbox.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EVIDENCE_STATE = "LOCAL_OPERATOR_HYGIENE_NOT_XAI_GROK_OR_AGENT_RUNTIME_AUTHORITY"
DEFAULT_ALLOWLIST = frozenset(
    {
        "view_file",
        "replace_file_content",
        "multi_replace_file_content",
        "write_to_file",
        "run_command",
        "list_dir",
        "grep_search",
        "manage_task",
    }
)


@dataclass
class ToolGate:
    allowlist: set[str] = field(default_factory=lambda: set(DEFAULT_ALLOWLIST))

    def __post_init__(self) -> None:
        if not all(isinstance(name, str) and name for name in self.allowlist):
            raise ValueError("allowlist entries must be non-empty strings")

    def is_allowed(self, tool_name: str) -> bool:
        if not isinstance(tool_name, str) or not tool_name:
            return False
        return tool_name in self.allowlist

    def authorize(self, tool_name: str, params: dict) -> dict:
        if not isinstance(params, dict):
            raise TypeError("params must be a dictionary")
        authorized = self.is_allowed(tool_name)
        return {
            "tool_name": tool_name,
            "authorized": authorized,
            "reason": "ALLOWLIST_MATCH" if authorized else "TOOL_NOT_ALLOWLISTED",
            "evidence_state": EVIDENCE_STATE,
            "executes_tool": False,
            "operational_authority": False,
        }
