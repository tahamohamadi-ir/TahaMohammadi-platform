# Deployment Runbook

Production deployment is not authorized until R8 passes.

Required deployment order:

1. Verify tagged commits and artifact hashes.
2. Back up the production database and media.
3. Deploy backward-compatible backend changes.
4. Apply reviewed migrations.
5. Deploy the admin panel.
6. Deploy the public site.
7. Run production smoke tests.
8. Record the result and rollback readiness.

---

**Status 2026-09-16:** the R8 precondition above has been met — owner sign-off 2026-09-15
([`R8-F01-OWNER-SIGNOFF-2026-09-15.md`](../10-tracking/R8-F01-OWNER-SIGNOFF-2026-09-15.md)),
the documented production promotion performed (`taha-web-prod:prod-457b7fe7`), and the final
publication concern (the apex DNS record) verified healthy from the authoritative path. The ordered
procedure and rollback steps below remain the operative policy. Final record:
[`HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md`](../10-tracking/HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md).