# Owner factual-content intake

“Factual content” means every value that represents Taha, an organization, a credential, a published work, a downloadable document, or an external destination. It is distinct from design copy in concepts: a concept can demonstrate hierarchy, but it cannot prove that a sentence, date, link, title, image caption, or availability claim is true and publishable.

## What needs an approved source

| Surface | Examples of factual values | Minimum evidence |
|---|---|---|
| Identity and profile | Persian/English name form, bio, role, research statement, location, availability | Owner-approved text per locale |
| Contact and links | Email, ORCID, LinkedIn, affiliation, social links | Current URL/address and owner confirmation |
| CV and resume | File, version/date, language, download title, access policy | Final file plus owner publication approval |
| Research and publications | Title, authors, venue, date, DOI/URL, claim, abstract, status | Source record or owner-approved bibliography |
| Projects / teaching / creative work | Scope, date, collaborators, role, outcomes, media rights, caption | Owner-approved record and rights/credit evidence |
| Legal/operational | Copyright, image credit, privacy/contact notice, availability status | Owner decision or applicable policy |

## Intake format

For each record, add one row to `OWNER-CONTENT-MANIFEST.md` with its stable ID, locale, source path/URL, hash for a supplied file, approval state, publication state, translation state, and any restriction. A record may be approved for internal administration while still marked `not-public`.

## Safe defaults until supplied

- Missing profile/research text: render the documented unavailable state; do not paraphrase concepts.
- Missing translation: keep the requested locale; do not substitute the other language.
- Missing CV/document: omit the download or state that it is unavailable.
- Unverified external link or credential: omit it.
- Unverified image relationship/credit: do not attach the image to a factual record.

This intake is not a request to publish private material. It separates owner approval from publication approval so that the admin panel can prepare records without exposing them.
