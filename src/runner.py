from __future__ import annotations
from dataclasses import dataclass, field
from checks.env import check_env_var
from checks.files import check_file
from checks.http import check_http_endpoint
from checks.tcp import check_tcp_port
from models import CheckResult, EnvGuardConfig, Status


@dataclass
class RunReport:
    config_name: str
    env_vars: list[CheckResult] = field(default_factory=list)
    tcp_ports: list[CheckResult] = field(default_factory=list)
    http_endpoints: list[CheckResult] = field(default_factory=list)
    files: list[CheckResult] = field(default_factory=list)

    @property
    def all_results(self) -> list[CheckResult]:
        return self.env_vars + self.tcp_ports + self.http_endpoints + self.files

    @property
    def failed(self) -> list[CheckResult]:
        return [r for r in self.all_results if r.status == Status.FAIL]

    @property
    def passed(self) -> list[CheckResult]:
        return [r for r in self.all_results if r.status == Status.OK]

    @property
    def total(self) -> int:
        return len(self.all_results)

    @property
    def success(self) -> bool:
        return len(self.failed) == 0


def run_checks(config: EnvGuardConfig) -> RunReport:
    report = RunReport(config_name=config.name)
    report.env_vars = [check_env_var(spec) for spec in config.env_vars]
    report.tcp_ports = [check_tcp_port(spec) for spec in config.tcp_ports]
    report.http_endpoints = [check_http_endpoint(spec) for spec in config.http_endpoints]
    report.files = [check_file(spec) for spec in config.files]
    return report