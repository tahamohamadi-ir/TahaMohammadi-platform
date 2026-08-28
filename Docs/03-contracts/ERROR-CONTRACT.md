# Error Contract

JSON errors use this stable shape:

```json
{
  "code": "stable_machine_code",
  "message": "Safe human-readable message",
  "field_errors": {},
  "request_id": "server-generated-id"
}
```

Public messages must not expose stack traces, filesystem paths, credentials, database details, or internal identifiers.
Clients map unknown errors to a safe generic state and preserve the request identifier.
