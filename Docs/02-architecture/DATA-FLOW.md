# Data Flow

## Public content

1. An administrator saves a draft through the admin API.
2. The backend validates and stores the draft.
3. The administrator previews the draft with an authorized token.
4. The administrator publishes the approved record.
5. The public API exposes the published projection.
6. The public-site build validates and renders the projection.

## Contact message

1. The public site submits an allowed payload.
2. The backend validates rate, size, and fields.
3. The backend sends through the configured provider.
4. The backend returns a non-sensitive status.

Public clients never receive draft records, secrets, recovery codes, or internal audit data.
