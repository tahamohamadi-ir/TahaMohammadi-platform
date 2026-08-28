# Authentication Contract

- Public read endpoints do not require authentication.
- Admin endpoints use secure session authentication.
- State-changing requests require CSRF protection.
- Server-side permission checks are mandatory.
- MFA remains available for privileged access.
- Recovery codes are hashed and shown only during generation.
- Authentication failures return a stable error envelope without sensitive detail.
