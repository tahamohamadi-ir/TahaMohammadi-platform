# R7 Contact Delivery Evidence (staging)

**Status: DELIVERY ACCEPTED — owner receipt confirmation pending.**
Owner approved one real test message on 2026-09-10.

**Release:** `stage-601b2294-f1cfa37d-9c2c7045` (endpoint unchanged through the
current deployment).

## Probes

| Probe                                        | Request                                                                                                    | Result                                              |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| JSON delivery (browser-like same-origin)     | `POST /api/contact` with `Origin: https://staging.tahamohamadi.ir`, JSON `{name,email,locale,message}`     | **200** `{"ok": true}` — provider accepted the send |
| Cross-origin rejection                       | same body with `Origin: https://evil.example`                                                              | **400** `{"ok": false, "error": "cross-origin submissions are rejected"}` |

No message body is persisted by design (non-persistence policy in
`Back-End/apps/api/public_contact.py`); backend tests cover the HTML/JSON,
cross-origin and non-persistence contracts.

## Recipient note (needs owner attention)

`_recipient_email()` resolves `CONTACT_FORM_TO` first, then the published
`SiteSettings.contact_email`. The public staging payload currently reports
`contact.email = taha.mohammadi@shahed.ac.ir`, so the delivered message most
likely went to that address unless `CONTACT_FORM_TO` in the staging `.env.stage`
overrides it (owner-controlled; value not visible from here).

If the owner wanted the test at `taha95mohammadi@gmail.com`, update
`CONTACT_FORM_TO` (or the published contact email) in the staging configuration
and re-run one probe; the endpoint response is the delivery acknowledgement,
and inbox receipt remains the owner's confirmation.

**PASS assessment:** API/proxy delivery and rejection paths proven; final
delivery confirmation is the owner's inbox check at the configured recipient.
