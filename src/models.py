from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Status(Enum):
    OK = "ok"
    FAIL = "fail"
    SKIP = "skip"


@dataclass
class CheckResult:
    name: str
    status: Status
    message: str
    hint: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.status == Status.OK


@dataclass
class EnvVarCheck:
    key: str
    required: bool = True
    validate: Optional[str] = None
    label: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "EnvVarCheck":
        return cls(key=data["key"], required=data.get("required", True),
                   validate=data.get("validate"), label=data.get("label"))


@dataclass
class TcpPortCheck:
    host: str
    port: int
    label: Optional[str] = None
    timeout: float = 3.0

    @classmethod
    def from_dict(cls, data: dict) -> "TcpPortCheck":
        return cls(host=data["host"], port=int(data["port"]),
                   label=data.get("label"), timeout=float(data.get("timeout", 3.0)))


@dataclass
class HttpEndpointCheck:
    url: str
    expect_status: int = 200
    label: Optional[str] = None
    timeout: float = 5.0
    method: str = "GET"

    @classmethod
    def from_dict(cls, data: dict) -> "HttpEndpointCheck":
        return cls(url=data["url"], expect_status=int(data.get("expect_status", 200)),
                   label=data.get("label"), timeout=float(data.get("timeout", 5.0)),
                   method=data.get("method", "GET").upper())


@dataclass
class FileCheck:
    path: str
    type: str = "file"
    label: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "FileCheck":
        return cls(path=data["path"], type=data.get("type", "file"), label=data.get("label"))


@dataclass
class EnvGuardConfig:
    name: str
    env_vars: list[EnvVarCheck] = field(default_factory=list)
    tcp_ports: list[TcpPortCheck] = field(default_factory=list)
    http_endpoints: list[HttpEndpointCheck] = field(default_factory=list)
    files: list[FileCheck] = field(default_factory=list)