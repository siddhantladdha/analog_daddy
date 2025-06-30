---
applyTo: '**'
---

# Instructions

Coding standards, domain knowledge, and preferences that AI should follow.
This file documents project-specific conventions and best practices for using
GitHub Copilot and other AI coding assistants in this workspace.
Please read and follow these guidelines to ensure consistency and maintainability.

## General Project Practices

- Use modern Python packaging: all dependencies and metadata are in `setup.cfg` and `pyproject.toml`.
- Do not use or reference `setup.py` or `requirements.txt` for builds or installs.
- All new features and major changes should be developed in a feature branch, then merged to `main`.
- Follow PEP8 for all Python code.
- Use clear, incremental commits and PRs for new features.
- Make all the markdown generated compliant with markdownlint rules.

## Dashboard Development

- Keep the code modular — prefer functions over inline logic.
- All components should be usable from app.py.
- Dashboard will be built using Streamlit.
- Use Streamlit’s layout primitives. When absolutely needed ask if the user
wants to use custom HTML/CSS to achieve the task.
- Group related widgets into functions (e.g., def filter_controls(): ...)
- Use type hints and docstrings for all functions and classes.
- The dashboard is a frontend for the main package and lives in `analog_daddy/dashboard/` directory.
- Use the following structure for scalable streamlit apps:
  - app.py: Streamlit app entry point
  - data_loader.py: Functions to load and preprocess data
  - assets/: Static files (e.g., CSS)
  - ui_components.py: Functions to render widgets or layout blocks
  - plotter.py: Functions for generating visualizations
  - utils.py: Miscellaneous utility functions (specific to the dashboard)
- If at all CSS is used for theming, all custom CSS (e.g., Dracula theme) should be placed in `analog_daddy/dashboard/assets/`
and use CSS variables for easy configurable theming.
- Do not use inline style properties for theming (e.g., color, background, font) in files.
- Use inline CSS styles only when absolutely needed and its use must be justified in the code.

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

## Streamlit specific Instructions

- Browse the latest [Streamlit documentation](https://docs.streamlit.io/) for the latest features and best practices.
- Include st.cache_data or st.cache_resource where needed
- Don't include Flask, Django, or non-Streamlit frameworks.
- Don't include HTML unless explicitly required
- Use plotly for visualizations unless otherwise specified.

## Lookup and analog_daddy specific Instructions

- Use the `analog_daddy` package for all data processing and analysis tasks.
- Refer the files in `docs/` for how to use the `look_up` function and how to load the LUT and
for referencing the plotting functions as well.
- To understand the `.npy` structure of the LUT, refer to the `docs/usage_demo.ipynb` notebook.

_This file is intended to reduce repeated questions and ensure a smooth workflow for all contributors using Copilot or other AI tools._
