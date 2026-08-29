# Error Contract

The stable envelope below is a target for new compatible endpoints, not a statement about every migrated response today. The current backend response shapes and consumer mappings are normative in `ERROR-COMPATIBILITY-MATRIX.md` until a tested normalization packet is accepted.

Target envelope:

```json
{
  "code": "stable_machine_code",
  "message": "Safe human-readable message",
  "field_errors": {},
  "request_id": "server-generated-id"
}
```

Public messages must not expose stack traces, filesystem paths, credentials, database details, or internal identifiers.
Clients map unknown errors to a safe generic state. A request identifier is preserved only when the server actually provides one.
