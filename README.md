# env-guard

[![PyPI](https://img.shields.io/pypi/v/env-guard-checker)](https://pypi.org/project/env-guard-checker/)
[![Python](https://img.shields.io/pypi/pyversions/env-guard-checker)](https://pypi.org/project/env-guard-checker/)
[![License](https://img.shields.io/github/license/IvanYanishevskyi/env-guard)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/IvanYanishevskyi/env-guard/ci.yml?branch=main)](https://github.com/IvanYanishevskyi/env-guard/actions)
Lightweight pre-flight checks for Python projects.

Catch missing env vars, dead services and broken endpoints  
*before* you start your app.

---

## Install

```bash
pip install env-guard-checker
```

CLI:
```bash
envguard check
```

---

## Why

Most local failures are boring:

- `.env` not loaded  
- DB not running  
- wrong API key  
- service not reachable  

You usually find out **after** the app crashes.

`env-guard` flips that:
you get a fast, clear check upfront.

---

## Example

```text
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

---

## Quickstart

```bash
envguard init
envguard check
envguard check --hints
```

- auto-detects config  
- loads `.env`  
- works in CI  

---

## Config

```yaml
name: my-app

env_vars:
  - key: OPENAI_API_KEY
    required: true
    validate: starts_with:sk-

  - key: DATABASE_URL
    required: true
    validate: contains:postgresql

tcp_ports:
  - host: localhost
    port: 5432
    label: PostgreSQL

http_endpoints:
  - url: http://localhost:8000/health
    expect_status: 200

files:
  - path: .env
    type: file
```

---

## CI example

```yaml
name: envguard

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install env-guard-checker
      - run: envguard check
```

---

## Notes

This is intentionally simple.

It’s not a security tool and not a secret scanner.  
Just a quick sanity check that saves time.

---

## License

MIT
