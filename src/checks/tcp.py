from __future__ import annotations
import socket
from models import CheckResult, Status, TcpPortCheck


def check_tcp_port(spec: TcpPortCheck) -> CheckResult:
    display = spec.label or f"{spec.host}:{spec.port}"
    try:
        with socket.create_connection((spec.host, spec.port), timeout=spec.timeout):
            pass
        return CheckResult(name=display, status=Status.OK,
                           message=f"{spec.host}:{spec.port} reachable")
    except ConnectionRefusedError:
        return CheckResult(name=display, status=Status.FAIL,
                           message=f"{spec.host}:{spec.port} connection refused",
                           hint=f"Service on port {spec.port} is not running.")
    except TimeoutError:
        return CheckResult(name=display, status=Status.FAIL,
                           message=f"timed out after {spec.timeout}s",
                           hint=f"Port {spec.port} not responding. Firewall?")
    except OSError as exc:
        return CheckResult(name=display, status=Status.FAIL, message=str(exc),
                           hint="Check hostname and port in envguard.yaml.")