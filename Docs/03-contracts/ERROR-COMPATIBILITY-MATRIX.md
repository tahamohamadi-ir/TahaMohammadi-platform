# Error Compatibility Matrix

## Current backend shapes

| Surface | Observed shape | Client rule |
|---|---|---|
| Admin `AdminError` | `{ "code", "message", "fields"? }` | Preserve `code`; map optional `fields` to field errors; do not assume `request_id`. |
| Public profile not found | `{ "detail": "profile not found" }` with 404 | Show public unavailable/not-found state; do not expose raw backend text as owner content. |
| Public contact JSON failure | `{ "ok": false, "error": "..." }` | Map to form-level safe failure and preserve entered values where appropriate. |
| Public contact form failure | HTML response with 422 | Submit as progressive form navigation or use an accepted JSON adapter; never parse HTML as JSON. |
| Django/Ninja validation or unhandled error | Framework-specific response | Treat as unknown safe failure until captured in accepted OpenAPI/compatibility fixtures. |

## Target normalization

The target envelope is not current implementation fact. After compatibility review, new versioned endpoints may adopt:

```json
{
  "code": "stable_machine_code",
  "message": "Safe human-readable message",
  "field_errors": {},
  "request_id": "optional-server-generated-id"
}
```

Adoption requires backend tests, public/admin consumer fixtures, documented compatibility behavior, and a versioning decision. Until then, each client normalizes the observed shapes above into its own safe UI state without fabricating fields.
