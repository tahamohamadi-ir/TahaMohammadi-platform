# Authentication Contract

- Public read endpoints do not require authentication.
- Admin endpoints use secure session authentication.
- State-changing requests require CSRF protection.
- Server-side permission checks are mandatory.
- MFA remains available for privileged access.
- Recovery codes are hashed and shown only during generation.
- Authentication failures use the current safe response mapping in `ERROR-COMPATIBILITY-MATRIX.md` until a normalized envelope is adopted.
- The accepted pre-scaffold topology is same-origin reverse-proxy delivery. Cross-origin cookies, CORS, or API hosting require a separate accepted topology decision and browser evidence.
