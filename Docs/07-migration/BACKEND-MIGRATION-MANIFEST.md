# Backend Migration Manifest

## COPY-AS-IS baseline

The exact tracked contents of legacy `apps/cms/` were copied to the backend repository root.
This includes Django apps, settings, migrations, scripts, tests, `pyproject.toml`, and `uv.lock`.

## EXCLUDED

- `.venv/`
- `.pytest_cache/`
- `.ruff_cache/`
- `__pycache__/`
- `dev.sqlite3`
- `media/`
- ignored build output
- ignored `node_modules/`
- secrets and local environment files

## COPY-THEN-REFACTOR

- Settings that assume the legacy monorepo
- Rebuild integration that assumes `apps/web`
- SPA-serving routes under `/admin/`
- Caddy, Compose, deployment, and timer files in `Infra/legacy-monorepo/`

## Preservation rule

Do not squash or recreate migrations before a clean PostgreSQL migration test passes.
Do not remove compatibility routes before both new frontend consumers pass contract tests.
