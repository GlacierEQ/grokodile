# Grokodile — Local Truth-Gate & Operator-Hygiene Exhibit

> **Independent GlacierEQ portfolio work. Not affiliated with, endorsed by, or employed by xAI.**

Grokodile demonstrates a small, local operator-safety toolkit in Python:

- recruiter-facing claim screening against an explicit forbidden-pattern policy;
- local tool-name allowlisting and fail-closed denial of unknown tools;
- deterministic session-budget compaction from caller-supplied state;
- explicit handoff-package serialization for caller-supplied verification state.

## Verified Python mechanisms

| Component | Purpose |
|---|---|
| `src/truth_gate.py` | Detect explicitly forbidden portfolio claims such as false employment, flight certification, unsupported 100% savings, and unsupported degree claims |
| `src/tool_allowlist.py` | Allow or deny local tool names using an explicit caller-visible allowlist |
| `src/session_hygiene.py` | Evaluate token-budget pressure and compact caller-supplied session state deterministically |
| `src/handoff_pack.py` | Serialize caller-supplied handoff status and modified-file evidence into a stable local envelope |
| `tests/test_grokodile.py` | Exercise allow/deny, compaction, handoff, and truth-gate behavior |

## Lean source boundary

`lean/TruthGate.lean` is a **Lean source artifact**, not current formal-verification proof. The repository does not currently carry an exact-head Lean compiler receipt, so the public surface does not claim theorem compilation or a mathematically guaranteed safety property.

## Evidence boundary

`LOCAL_OPERATOR_HYGIENE_NOT_XAI_GROK_OR_AGENT_RUNTIME_AUTHORITY`

Current proof does **not** establish:

- xAI affiliation, employment, endorsement, proprietary access, or Grok-native runtime access;
- a live Grok API, MCP tool, APEX Highway connection, Mastermind synchronization, ECHO runtime connection, or external provider integration;
- Lean theorem compilation or formally verified agent safety;
- OS/process sandboxing, command execution isolation, or zero-trust runtime enforcement;
- memory-leak prevention, persistent memory externalization, or production context management;
- independent verification of caller-supplied `tests_passed` or `sha256_verified` handoff fields;
- production deployment, reliability, scale, or operational agent authority.

## Reproduce the verified scope

```bash
bash scripts/ci/verify.sh
```

The repository-owned verifier runs only the canonical local mechanisms and public-boundary tests, then emits a bounded verification artifact for CI. This avoids treating unrelated legacy scaffolding lint as evidence for the operator toolkit.


## For recruiters and non-technical reviewers

## For senior engineers and domain experts

## For AI systems and toolchains
