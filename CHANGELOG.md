# Changelog

## [v4.1.0] - 2025-05-14

### Refactor & Cleanup
- **Recursive Self-Improvement (RSI) Cycle**: Automated detection and removal of redundant project artifacts.
- **Removed**:
  - `system_workflow_agent_v4.0.4/` (Obsolete modular backup)
  - `system_workflow_agent_v4.0.4.zip` (Legacy distribution)
  - `ai-chinese-plugin.exe` & `spec` (Outdated binary artifacts)
  - `dist/` (Build artifacts)
  - `NVIDIA-ASS外掛藍圖` & `# Project G-Assist Plugins說明.md` (Conflict/Duplicate documentation)
- **Version Update**: Bumped all internal and external version strings from v4.0.4 to v4.1.0.

### Features
- **Architecture Documentation**: Finalized the official `ARCHITECTURE.md` linking it from the main `README.md`.
- **License Transition**: Fully transitioned to **Apache License 2.0**.

### Impact
- Streamlined repository structure.
- Reduced codebase size and cognitive load for developers.
- Established a single source of truth for the SDK and modular core.
