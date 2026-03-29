from __future__ import annotations
import os
from models import CheckResult, EnvVarCheck, Status


def _validate_format(value: str, rule: str) -> tuple[bool, str]:
    if ":" not in rule:
        return False, f"Unknown rule: '{rule}'"
    op, arg = rule.split(":", 1)
    match op:
        case "starts_with":
            ok = value.startswith(arg)
            return ok, "" if ok else f"must start with '{arg}'"
        case "ends_with":
            ok = value.endswith(arg)
            return ok, "" if ok else f"must end with '{arg}'"
        case "contains":
            ok = arg in value
            return ok, "" if ok else f"must contain '{arg}'"
        case "min_length":
            n = int(arg)
            ok = len(value) >= n
            return ok, "" if ok else f"must be at least {n} characters"
        case _:
            return False, f"Unknown rule: '{op}'"


def check_env_var(spec: EnvVarCheck) -> CheckResult:
    display = spec.label or spec.key
    value = os.environ.get(spec.key)
    if value is None:
        if spec.required:
            return CheckResult(name=display, status=Status.FAIL, message="missing",
                               hint=f"Add {spec.key} to your .env file.")
        return CheckResult(name=display, status=Status.SKIP, message="not set (optional)")
    if spec.validate:
        ok, error = _validate_format(value, spec.validate)
        if not ok:
            return CheckResult(name=display, status=Status.FAIL,
                               message=f"present but invalid — {error}",
                               hint=f"Check value of {spec.key}: rule is '{spec.validate}'.")
    return CheckResult(name=display, status=Status.OK, message="present")