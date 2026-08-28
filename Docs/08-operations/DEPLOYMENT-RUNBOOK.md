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
