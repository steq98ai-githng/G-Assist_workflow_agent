# AI Agent Workflow Instructions (v4.0.4)

## Architecture Paradigm
* **Layered Design:** The code is strictly divided into `/core`, `/mcp`, `/vision`, `/config`, and `/intents`. Do not merge these responsibilities into monolithic files.
* **No Global State:** Instantiate objects and manage dependencies explicitly. Avoid global clients or variables.

## Coding Conventions
* **Language:** Python 3.10+
* **Typing:** Use type hints extensively (`typing.Dict`, `typing.List`, `typing.Optional`, etc.).
* **Logging:** Use the built-in `logging` module. Do not use `print()` for critical execution flows; `plugin.stream` is strictly for user-facing UI updates.

## Testing Instructions
* **Framework:** All tests must be written using `pytest`.
* **Mocking Linux execution:** For GitHub Actions or Linux dev environments, `ctypes.windll` must be mocked in test files before importing `gassist_sdk` or plugin logic.
  ```python
  import ctypes
  from unittest.mock import MagicMock
  ctypes.windll = MagicMock()
  ```
* **Run command:** `pytest tests/`

## Deployment & Verification
* Run `install.bat` on Windows to deploy to `C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent`.
* Ensure `config.json` schema validation is enforced natively or using robust logic in `config/loader.py`.
* Always clean up pycache and test artifacts before packaging using `package_v4.py`.
