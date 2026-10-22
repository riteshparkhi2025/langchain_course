# LangChain Documentation Helper

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
these commands from the project directory:

```powershell
uv sync
```

This creates the `.venv` environment and installs the dependencies pinned in
`uv.lock`, including the Jupyter kernel dependency. In VS Code, select the
project's `.venv` Python interpreter as the notebook kernel.

Add any required API credentials to a local `.env` file. Do not commit that
file.

Run Python commands in the project environment with:

```powershell
uv run python your_script.py
```