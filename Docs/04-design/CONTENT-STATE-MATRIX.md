# Content State Matrix

| State | Meaning | Required presentation |
|---|---|---|
| `loading` | A bounded request is active | Named region and non-blocking status |
| `ready` | Valid content is available | Normal template |
| `empty` | Query succeeded with no records | Honest message and valid next action |
| `untranslated` | Alternate locale is unpublished | Link to available locale when authorized |
| `unavailable` | A known dependency is absent | Safe explanation without fabricated data |
| `error` | Request or validation failed | Recovery action and stable error message |
| `no-results` | Search or filter has no matches | Clear query reset action |
| `unauthorized` | Authentication is required | Sign-in path without leaking data |
| `forbidden` | User lacks permission | Safe denial and navigation recovery |
| `rate-limited` | Server accepted identity but rejected frequency | Safe wait/retry explanation without exposing limits or internal data |
| `conflict` | A revision changed after the editor opened it | Preserve unsaved work, show conflict state, and offer explicit refresh/compare recovery |

Decorative empty-state art must not replace the state message.
Icons must have bounded computed dimensions.
Form submissions distinguish transport failure, server validation, authorization, rate limit, and success; no generic success state is shown before backend confirmation.
