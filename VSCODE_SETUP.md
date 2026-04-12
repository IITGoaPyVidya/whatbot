# VSCode Setup Guide

## Recommended Extensions

Install these extensions from the VSCode Extensions panel (`Ctrl+Shift+X`):

| Extension | ID | Purpose |
|-----------|-----|---------|
| Python | `ms-python.python` | Python language support |
| Pylance | `ms-python.vscode-pylance` | Type checking & IntelliSense |
| REST Client | `humao.rest-client` | Test API endpoints with `.http` files |
| Docker | `ms-azuretools.vscode-docker` | Docker integration |
| GitLens | `eamodio.gitlens` | Enhanced Git UI |
| DotENV | `mikestead.dotenv` | Syntax highlighting for `.env` files |

---

## Workspace Settings

Create `.vscode/settings.json` in the project root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "venv/": true
  }
}
```

> **Windows users:** Change the interpreter path to:
> `"${workspaceFolder}/venv/Scripts/python.exe"`

---

## Debugging Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI (uvicorn)",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      "jinja": true,
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/", "-v"],
      "justMyCode": true
    }
  ]
}
```

With this configuration, press **F5** to start the FastAPI server with the VSCode debugger attached.

---

## Testing API Endpoints with REST Client

The file `examples/test_requests.http` contains ready-to-use HTTP requests.

1. Open `examples/test_requests.http` in VSCode
2. Click **"Send Request"** above any request block
3. The response appears in a side panel

---

## Terminal Tips (VSCode Integrated Terminal)

```bash
# Activate virtual environment
source venv/bin/activate         # macOS/Linux
.\venv\Scripts\Activate.ps1      # Windows PowerShell

# Start dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v

# Run a single test file
pytest tests/test_webhook.py -v
```
