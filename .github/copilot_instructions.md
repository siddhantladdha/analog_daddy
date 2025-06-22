# GitHub Copilot Instructions for analog_daddy

This file documents project-specific conventions and best practices for using GitHub Copilot and other AI coding assistants in this workspace. Please read and follow these guidelines to ensure consistency and maintainability.

## General Project Practices

- Use modern Python packaging: all dependencies and metadata are in `setup.cfg` and `pyproject.toml`.
- Do not use or reference `setup.py` or `requirements.txt` for builds or installs.
- All new features and major changes should be developed in a feature branch, then merged to `main`.
- Follow PEP8 for all Python code.
- Use clear, incremental commits and PRs for new features.
- Make all the markdown generated compliant with markdownlint rules.

## Dashboard Development

- The dashboard is a frontend for the main package and lives in `analog_daddy/dashboard/`.
- Use the following structure for scalable Dash apps:
  - `app.py`: Dash app instance
  - `layout.py`: Layout components
  - `callbacks.py`: Callbacks for interactivity (if needed)
  - `assets/`: Static files (e.g., CSS)
  - `__main__.py`: Entry point (run with `python -m analog_daddy.dashboard`)
- All custom CSS (e.g., Dracula theme) should be placed in `analog_daddy/dashboard/assets/` and use CSS variables for easy theming.
- Segment code into logical modules/files for maintainability.
- All new dashboard features should be added incrementally, with each step tested and committed separately.
- Do not use inline style properties for theming (e.g., color, background, font) in Dash layout files. All theming and color should be handled in CSS in the assets directory. Use inline styles only for layout/spacing or dynamic runtime changes.

## Testing

- Place all tests in the `tests/` directory, including dashboard tests.
- Use standard Python `unittest` or `pytest` conventions.

## Conda & PyPI

- Always clean `dist/`, `build/`, and `*.egg-info/` before building for PyPI.
- For conda-forge, maintain a plain `meta.yaml` with noarch: python and pip install script.
- Pin dependencies as needed for reproducibility.

## VS Code & Environments

- Use the VS Code Command Palette to select the correct conda environment for the workspace.
- The recommended interpreter path is set in `.vscode/settings.json`.

## Miscellaneous

- Suppress known DeprecationWarnings in Dash apps with:

  ```python
  import warnings
  warnings.filterwarnings("ignore", category=DeprecationWarning)
  ```

- Use feature branches for all major new features (e.g., dashboard) and merge only when stable.

---

_This file is intended to reduce repeated questions and ensure a smooth workflow for all contributors using Copilot or other AI tools._
