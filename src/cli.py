from __future__ import annotations
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from loader import ConfigError, find_config, load_config
from reporter import print_report
from runner import run_checks

app = typer.Typer(name="envguard",
                  help="Pre-flight environment checks. Like Pydantic, but for your infra.",
                  add_completion=False, rich_markup_mode="rich")
console = Console()
err_console = Console(stderr=True)

# Note: We want to keep the CLI code separate from the core logic to make it easier to test and reuse.
# The `check` command is the main entry point for users, while `init` is a convenience for generating a starter config.
@app.command()
def check(
    config: Optional[Path] = typer.Option(None, "--config", "-c", show_default=False),
    hints: bool = typer.Option(False, "--hints", help="Show fix suggestions."),
) -> None:
# Validate your environment against [bold]envguard.yaml[/].
    try:
        from dotenv import load_dotenv
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file, override=False) 
    except ImportError:
        pass 
    try:
        config_path = config or find_config()
        cfg = load_config(config_path)
    except ConfigError as exc:
        err_console.print(f"\n  [bold red]Error:[/] {exc}\n")
        raise typer.Exit(code=1) from exc
    report = run_checks(cfg)
    print_report(report, show_hints=hints)
    if not report.success:
        raise typer.Exit(code=1)

# The `init` command creates a starter `envguard.yaml` with example checks. Users can customize it for their project.
@app.command()
def init(
    name: str = typer.Option("my-app", "--name", "-n", prompt="Project name"),
    output: Path = typer.Option(Path("envguard.yaml"), "--output", "-o"),
) -> None:
# Create a starter envguard.yaml config file. Run `envguard check` to validate your environment.
    if output.exists():
        if not typer.confirm(f"{output} already exists. Overwrite?", default=False):
            raise typer.Exit()
    output.write_text(f"""\
name: {name}

env_vars:
  - key: APP_SECRET_KEY
    required: true
  - key: DATABASE_URL
    required: true
    validate: contains:postgresql

tcp_ports:
  - host: localhost
    port: 5432
    label: PostgreSQL
  - host: localhost
    port: 6379
    label: Redis

http_endpoints:
  - url: http://localhost:8000/health
    expect_status: 200

files:
  - path: .env
    type: file
""", encoding="utf-8")
    console.print(f"\n  [bold green]✓[/] Created [bold]{output}[/]\n")


def main() -> None:
    app()