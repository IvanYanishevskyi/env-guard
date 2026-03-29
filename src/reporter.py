from __future__ import annotations
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from rich import box
from rich.text import Text
from models import CheckResult, Status
from runner import RunReport

console = Console()

_STATUS_ICON = {Status.OK: "[bold green]✓[/]", Status.FAIL: "[bold red]✗[/]", Status.SKIP: "[dim]–[/]"}
_STATUS_COLOR = {Status.OK: "green", Status.FAIL: "red", Status.SKIP: "dim"}
_SECTION_LABELS = {"env_vars": "ENV VARS", "tcp_ports": "TCP PORTS",
                   "http_endpoints": "HTTP ENDPOINTS", "files": "FILES"}


def print_report(report: RunReport, show_hints: bool = False) -> None:
    console.print()
    console.print(Rule(f"[bold cyan]{report.config_name}[/] — pre-flight check", style="cyan"))
    console.print()
    sections = {"env_vars": report.env_vars, "tcp_ports": report.tcp_ports,
                "http_endpoints": report.http_endpoints, "files": report.files}
    for key, results in sections.items():
        if not results:
            continue
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        table.add_column(width=2)
        table.add_column(min_width=24)
        table.add_column()
        for r in results:
            table.add_row(
                _STATUS_ICON[r.status],
                Text(r.name, style="bold" if r.status == Status.FAIL else ""),
                Text(r.message, style=_STATUS_COLOR[r.status]),
            )
        console.print(f"  [bold white]{_SECTION_LABELS[key]}[/]")
        console.print(table)
    console.print(Rule(style="dim"))
    fails = len(report.failed)
    if report.success:
        console.print(f"  [bold green]All {report.total} checks passed.[/] [dim]Ready to deploy.[/]\n")
    else:
        console.print(f"  [bold red]{fails} check{'s' if fails != 1 else ''} failed[/], "
                      f"[green]{len(report.passed)} passed[/], [dim]{report.total} total[/]")
        if show_hints:
            console.print()
            console.print("  [bold yellow]HINTS[/]")
            for r in report.failed:
                if r.hint:
                    console.print(f"  [red]✗ {r.name}[/]")
                    console.print(f"    [dim]{r.hint}[/]\n")
        else:
            console.print("  [dim]Run with [/][bold]--hints[/][dim] for suggestions.[/]")
        console.print()