# AGENTS.md - Agent Workflow Guidelines & Code Conventions

This document provides instructions and tips for automated agents working on the Project G-Assist repository.

## GitHub Workflow Instructions

1. **Automated PR Creation**: All changes should be proposed via a Pull Request. Provide a concise, descriptive branch name and commit message.
2. **Auto Squash and Merge**: When a PR is approved and all checks pass, use the "Squash and merge" option to keep the commit history clean.
3. **Delete Branch on Completion**: After a PR is successfully merged, the source branch must be automatically or manually deleted to avoid clutter.

## General Coding Conventions

- **Performance Optimization PRs**: Must be prefixed with `⚡` and include `What`, `Why`, and `Measured Improvement` sections in the PR description.
- **Language**: This project implements "AI Chinese Mode", a System Workflow Agent based on NVIDIA G-Assist Protocol V2 and uses Model Context Protocol (MCP) for tool integration. Follow existing code patterns carefully.

## Testing Instructions & Environment Notes

- **Windows Dependencies (`gassist_sdk`)**: The `gassist_sdk` library located in `ai_chinese_mode/libs/gassist_sdk` utilizes `ctypes.windll`, which is a Windows-specific dependency.
- **Linux Testing Setup**:
  - Because automated testing often occurs on Linux environments, direct imports of `gassist_sdk` will fail with an `ImportError: cannot import name 'windll' from 'ctypes'`.
  - When writing or running tests on Linux, you **must mock `gassist_sdk` and `gassist_sdk.mcp`** before importing module dependencies in tests.

## Running Tests

Navigate to `ai_chinese_mode` and execute:
```bash
python test_plugin.py
```
*(Note: Expect failures on Linux environments unless the Windows dependencies are appropriately mocked.)*
