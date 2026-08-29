#!/usr/bin/env python3
import json, sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("jsonschema is required: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

here = Path(__file__).resolve().parent
schema = json.loads((here / "content-model.schema.json").read_text(encoding="utf-8"))
package = json.loads((here / "content-records.json").read_text(encoding="utf-8"))

errors = []
seen = set()

for idx, record in enumerate(package["records"]):
    try:
        jsonschema.validate(record, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"record[{idx}] {record.get('content_id')}: {e.message}")
    cid = record["content_id"]
    if cid in seen:
        errors.append(f"duplicate content_id: {cid}")
    seen.add(cid)

    status = record["status"]
    if status["publication_state"] == "published":
        if status["approval_state"] != "approved":
            errors.append(f"{cid}: published but not approved")
        if status["visibility"] != "public":
            errors.append(f"{cid}: published but visibility is not public")

    if record["locale"] == "fa" and status["translation_state"] == "untranslated":
        errors.append(f"{cid}: fa record cannot be marked untranslated")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print(f"PASS: {len(package['records'])} records validated; {len(seen)} unique content IDs.")
