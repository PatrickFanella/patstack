## Runtime Dependencies

Before running any bundled script, call `load_workspace_dependencies`. Set `PYTHON` to the exact Python executable path returned by that tool and use `"$PYTHON"` for every command below. The bundled runtime includes Pillow, which these scripts require. Do not use a bare system `python`; if workspace dependencies are unavailable, stop and report that the bundled runtime is required.
