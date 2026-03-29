# envguard

Pre-flight environment validation for Python projects.  
Checks env vars, TCP ports, HTTP endpoints and files — before you deploy.

```
pip install envguard
```

---

```
───────────────  pre-flight check ───────────────

  ENV VARS
  ✓  OPENAI_API_KEY       present
  ✓  REDIS_URL            present
  ✗  DATABASE_URL         missing

  TCP PORTS
  ✓  Redis                localhost:6379 reachable
  ✗  PostgreSQL           localhost:5432 connection refused

  HTTP ENDPOINTS
  ✓  OpenAI reachable     200 OK
  ✗  App health           connection refused

─────────────────────────────────────────────────────────────
  3 checks failed, 2 passed, 5 total
  Run with --hints for suggestions.
```

## Contents

- [Installation](#installation)
- [Quickstart](#quickstart)
- [Config reference](#config-reference)
- [CLI](#cli)
- [Makefile / CI](#makefile--ci)
- [Contributing](#contributing)
- [Known issues](#known-issues)

---

## Installation

```bash
pip install envguard
```

Requires Python 3.9+.

## Quickstart

```bash
# generate a starter envguard.yaml
envguard init

# run checks
envguard check

# show fix suggestions for failures
envguard check --hints
```

envguard walks up the directory tree looking for `envguard.yaml` automatically.  
If a `.env` file exists in the current directory, it's loaded before checks run.

## Config reference

```yaml
name: my-app

env_vars:
  - key: OPENAI_API_KEY
    required: true
    validate: starts_with:sk-

  - key: DATABASE_URL
    required: true
    validate: contains:postgresql

  - key: DEBUG
    required: false        # skipped if missing, won't fail

tcp_ports:
  - host: localhost
    port: 5432
    label: PostgreSQL      # shown in output instead of host:port
    timeout: 3.0           # seconds, default 3.0

http_endpoints:
  - url: http://localhost:8000/health
    expect_status: 200
    timeout: 5.0

files:
  - path: .env
    type: file
  - path: ./data
    type: directory
```

### `validate` rules for env vars

| Rule | Example | Description |
|---|---|---|
| `starts_with:<s>` | `starts_with:sk-` | value must start with `s` |
| `ends_with:<s>` | `ends_with:.local` | value must end with `s` |
| `contains:<s>` | `contains:postgresql` | value must contain `s` |
| `min_length:<n>` | `min_length:32` | value length must be ≥ n |

## CLI

```
envguard check                     run all checks
envguard check --hints             show hints for failed checks
envguard check -c path/to/file     use a specific config file
envguard init                      generate a starter config
envguard init --name my-app        set project name
```

Exit code: `0` if all checks pass, `1` if any fail.

## Makefile / CI

```makefile
deploy:
	envguard check || exit 1
	docker compose up -d
```

```yaml
# .github/workflows/deploy.yml
- name: Pre-flight check
  run: envguard check
```

---

## Contributing

Issues and pull requests are welcome.

### Reporting a bug

Before opening an issue, check [existing issues](../../issues) to avoid duplicates.

A good bug report includes:
- envguard version (`pip show envguard`)
- Python version and OS
- your `envguard.yaml` (redact secrets)
- full output with `envguard check`
- what you expected to happen

### Suggesting a feature

Open an issue with the `enhancement` label.  
Describe the use case, not just the feature — it helps figure out the right solution.

### Sending a pull request

```bash
git clone https://github.com/IvanYanishevskyi/env-guard§
cd envguard
pip install -e ".[dev]"
```

A few ground rules:

- one PR per feature or fix
- add a test for new behavior
- don't bump the version — that happens on release
- if you're fixing a bug, reference the issue number in the PR description

Not sure if a change is in scope? Open an issue first and ask.

### Adding a new check type

Check implementations live in `envguard/checks/`.  
Each check is a function that takes a spec dataclass and returns a `CheckResult`.  
See `envguard/checks/tcp.py` for a minimal example.

To add a new check type end-to-end:
1. add a dataclass to `models.py`
2. implement the check in `checks/your_check.py`
3. wire it into `runner.py` and `loader.py`
4. add it to the reporter sections in `reporter.py`
5. write tests in `tests/`

---

## Known issues

- **HTTP redirects** — followed by default, no config option to disable yet
- **Windows** — not tested; path handling in file checks may have edge cases
- **`min_length` with non-integer arg** — fails silently instead of raising a clear error

If you hit something not listed here, please [open an issue](../../issues/new).

---

## License

[MIT](LICENSE)
