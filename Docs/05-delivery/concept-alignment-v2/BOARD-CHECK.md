# Review-board browser check

2026-09-05 — checks apply to **REVIEW.html only**, not product runtime acceptance.

- Opened the local review board in the Codex in-app browser and inspected desktop rendering at requested 1280×900.
- Selected schematic nodes 3, 5 and 1; visible status text updated with the selected node, without navigation.
- Toggled light/dark, desktop/mobile layout and English/Persian layout direction; observed the corresponding state/name/layout changes.
- Changed comparison to Research; both live and reference images loaded with nonzero natural dimensions. Initial Home Dark pair was visibly loaded; all static image paths also passed filesystem validation.
- At requested 390×844, document client width and scroll width were both 375px (scrollbar excluded): no horizontal overflow. Inspected the mobile schematic and selected-node panel.
- Returned the board to Persian, dark, desktop composition and the Home Dark comparison. Removed temporary viewport override and marked the tab as a deliverable.
- The first hidden preview process did not remain reachable; a managed loopback server resolved this. The stale browser error tab could not be selected due to its data-URL policy; a fresh allowed HTTP tab displayed the document successfully. No browser security warning or policy was bypassed.

Preview: `http://127.0.0.1:8768/Docs/05-delivery/concept-alignment-v2/REVIEW.html`. This is a temporary local document server, not a deployed product. Open REVIEW.html directly with its relative references intact if the server has stopped.

Saved review evidence: [desktop schematic](../../10-tracking/concept-alignment-2026-09-05/review-board-desktop.png). No final Three.js render, Figma file, product six-width matrix, independent QA or owner acceptance is implied.
