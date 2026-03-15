# analog_daddy Copilot/Claude-Code Instructions

## Project context
- Repository: `analog_daddy`
- Type: Python data-processing library for analog transistor sizing and analysis
- Python: `>=3.14`
- Tooling defaults: prefer `uv` and `uv_build` for environment, build, and packaging workflows
- Key libraries: `pydantic`, `polars`, `scipy`, `xarray`, `plotly`, `quantiphy`, `hypothesis`

## Core architecture
1. Data pipeline: CSV -> Polars DataFrame -> lazy transformations -> populate ndarray via xarray.
2. `look_up` utility: retrieve array data using domain-specific Python keywords.
3. Utility scripts: provide syntactic sugar for commonly used `look_up` operations.

## Communication style
- Be concise by default; elaborate only when asked.
- Ask clarifying questions first when requirements are ambiguous.
- Prefer incremental updates over full rewrites.
- If tools/frameworks/language are not specified, ask before proceeding.

## Working rules
- Do not generate or edit code unless the user explicitly says `implement` or `write code`.
- Frame clarification prompts as Yes/No, with no more than 2 nested levels.
- When you are ready for code generation, ask a Y/n question.
- End non-trivial responses with exactly one Yes/No alignment-check question.
- Always include concrete sources by default:
  - Repo claims: `path:line` citations.
  - Web claims: direct links.
- For Polars API or behavior questions, prefer the `ask_polars` MCP server (configured in `.vscode/mcp.json`) before general web search.

## Python specific Instructions
- Use python hints at every function boundary.
- Strong follow PEP8 conventions, including but not limited to
    - Docstrings (they will be part of the documentation strategy)
    - Line length limits
    - 4 spaces for indentation.
- The code will be tested with `ruff` for linting.

## User shorthand
- `y/n` = yes/no
- `src` = provide sources
- `rdt` = Reddit
- `hn` = Hacker News
