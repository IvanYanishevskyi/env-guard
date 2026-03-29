from __future__ import annotations
from pathlib import Path
from typing import Union
import yaml
from models import (
    EnvGuardConfig, EnvVarCheck, FileCheck, HttpEndpointCheck, TcpPortCheck,
)


class ConfigError(Exception):
    pass


def load_config(path: Union[str, Path]) -> EnvGuardConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Failed to parse YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError("Config must be a YAML mapping at the top level.")
    return EnvGuardConfig(
        name=raw.get("name", config_path.stem),
        env_vars=[EnvVarCheck.from_dict(e) for e in raw.get("env_vars", [])],
        tcp_ports=[TcpPortCheck.from_dict(e) for e in raw.get("tcp_ports", [])],
        http_endpoints=[HttpEndpointCheck.from_dict(e) for e in raw.get("http_endpoints", [])],
        files=[FileCheck.from_dict(e) for e in raw.get("files", [])],
    )


def find_config(start: Union[str, Path, None] = None) -> Path:
    candidates = ["envguard.yaml", "envguard.yml", ".envguard.yaml"]
    current = Path(start or Path.cwd()).resolve()
    for directory in [current, *current.parents]:
        for name in candidates:
            candidate = directory / name
            if candidate.exists():
                return candidate
    raise ConfigError(
        "No envguard.yaml found. Run `envguard init` to create one."
    )