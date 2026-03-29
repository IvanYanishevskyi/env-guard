from __future__ import annotations
from pathlib import Path
from models import CheckResult, FileCheck, Status


def check_file(spec: FileCheck) -> CheckResult:
    display = spec.label or spec.path
    path = Path(spec.path).expanduser()
    if spec.type == "directory":
        if path.is_dir():
            return CheckResult(name=display, status=Status.OK, message=f"directory exists ({path})")
        if path.exists():
            return CheckResult(name=display, status=Status.FAIL,
                               message=f"exists but is not a directory: {path}")
        return CheckResult(name=display, status=Status.FAIL,
                           message=f"directory not found: {path}",
                           hint=f"Create it with `mkdir -p {path}`.")
    if path.is_file():
        return CheckResult(name=display, status=Status.OK, message=f"file exists ({path})")
    if path.exists():
        return CheckResult(name=display, status=Status.FAIL,
                           message=f"exists but is not a file: {path}")
    return CheckResult(name=display, status=Status.FAIL,
                       message=f"file not found: {path}",
                       hint=f"Expected a file at {path}.")