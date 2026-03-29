from __future__ import annotations
import requests
from requests.exceptions import ConnectionError, SSLError, Timeout
from models import CheckResult, HttpEndpointCheck, Status


def check_http_endpoint(spec: HttpEndpointCheck) -> CheckResult:
    display = spec.label or spec.url
    try:
        response = requests.request(spec.method, spec.url,
                                    timeout=spec.timeout, allow_redirects=True)
    except SSLError as exc:
        return CheckResult(name=display, status=Status.FAIL, message=f"SSL error — {exc}")
    except ConnectionError:
        return CheckResult(name=display, status=Status.FAIL,
                           message="connection refused or DNS failed",
                           hint=f"Is {spec.url} running and reachable?")
    except Timeout:
        return CheckResult(name=display, status=Status.FAIL,
                           message=f"timed out after {spec.timeout}s")
    except Exception as exc:
        return CheckResult(name=display, status=Status.FAIL, message=str(exc))

    if response.status_code == spec.expect_status:
        return CheckResult(name=display, status=Status.OK,
                           message=f"{response.status_code} {response.reason}")
    return CheckResult(name=display, status=Status.FAIL,
                       message=f"expected {spec.expect_status}, got {response.status_code}",
                       hint=f"Check {spec.url} manually.")