# Security Baseline

- No secrets in Git.
- Secure, HttpOnly, SameSite cookies in non-local environments.
- CSRF checks on state changes.
- Server-side authorization on every admin action.
- Argon2 password hashing.
- MFA support for privileged accounts.
- Upload MIME sniffing and size limits.
- Sanitized rich text.
- Published-only anonymous projections.
- Structured logs without credentials or content secrets.
- Dependency and secret scanning in CI.
