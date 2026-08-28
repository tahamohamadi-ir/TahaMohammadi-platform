# Backup and Restore Runbook

A valid backup includes PostgreSQL data, media, configuration inventory, and artifact versions.

A backup is not accepted until it restores into an isolated environment.
The restore check compares database objects, media hashes, public projections, and application startup.

Production restore commands must be added only after the new infrastructure paths are accepted.
