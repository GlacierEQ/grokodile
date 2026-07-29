#!/usr/bin/env python3
"""
Tool Allowlist Module (src/tool_allowlist.py).
Provides pro-code gated tool surface authorization for Grok operator execution.
"""
from dataclasses import dataclass, field

DEFAULT_ALLOWLIST = {
    "view_file",
    "replace_file_content",
    "multi_replace_file_content",
    "write_to_file",
    "run_command",
    "list_dir",
    "grep_search",
    "manage_task"
}

@dataclass
class ToolGate:
    allowlist: set[str] = field(default_factory=lambda: set(DEFAULT_ALLOWLIST))

    def is_allowed(self, tool_name: str) -> bool:
        return tool_name in self.allowlist

    def authorize(self, tool_name: str, params: dict) -> dict:
        if not self.is_allowed(tool_name):
            return {
                "tool_name": tool_name,
                "authorized": False,
                "reason": f"Tool '{tool_name}' is not in grokodile allowlist"
            }
        return {
            "tool_name": tool_name,
            "authorized": True,
            "reason": "APPROVED"
        }
