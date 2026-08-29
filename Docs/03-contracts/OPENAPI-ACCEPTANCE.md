# OpenAPI Acceptance — scaffold foundation

Status: **accepted for frontend scaffold foundation only**.

This acceptance locks the reviewed, source-generated snapshot for type generation and API-adapter foundation work. It does not approve owner facts, promoted media, fonts, production deployment, or a future breaking API change.

## Locked evidence

| Item | Value |
|---|---|
| Backend commit | `82e3984520154b60146009ae4a0d21eb5c30373e` |
| Settings used to generate | `config.settings.development` |
| Public schema | `docs/contracts/openapi/current/public-openapi.json` — SHA-256 `0f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5` — 40 paths — version `0.4.0` |
| Admin schema | `docs/contracts/openapi/current/admin-openapi.json` — SHA-256 `1328f8244c5541f225648082891a0a1244961c0dead6692488992ac8c7606f09` — 47 paths — version `0.1.0` |
| Endpoint inventory | `docs/contracts/openapi/current/endpoint-inventory.md` — SHA-256 `618ab18826875a5f27357ab87a3917082291d2e8610959b18aa2f936a7f3aa96` — 103 operations |
| Access evidence | `tests/test_public_openapi.py` and `tests/test_admin_openapi.py`: 9 passing checks for anonymous public and verified staff-plus-OTP admin access |

## Binding client scope

- Public client base remains `/api/`; it must use the canonical endpoint families in `API-CONTRACT.md`.
- Admin client base remains `/api/v1/admin/`; admin docs/schema remain staff-plus-OTP protected.
- About fetches only `/api/profiles/{locale}/about` and renders an unavailable state when no published record exists.
- Locale-sensitive site text never comes from unlocalized `/api/site`.
- Search remains local-index only; Rebuild/Health is excluded from admin v1.

## Change control

Any schema or backend-source change that changes one of these hashes immediately reopens PS-05. Regenerate the snapshots, run the public/admin OpenAPI access tests, update the review report, and create a new acceptance record before regenerated client types are adopted.
