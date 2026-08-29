# Responsive and RTL Specification

## Required widths

Test at 320, 390, 768, 1024, 1280, and 1440 CSS pixels.

## Reflow rules

- Content must reflow without horizontal page scrolling at 320 pixels.
- Text must remain usable at 200 percent browser zoom.
- Navigation must not depend on hover.
- Touch targets remain at least 44 by 44 CSS pixels.
- Media preserves focal guidance without stretching.
- Page-family reference comparison uses the matching PF-01 through PF-08 concept and theme before a visual result is accepted.

## Direction rules

- Use logical properties for spacing and alignment.
- Keep DOM reading order meaningful in both directions.
- Isolate emails, URLs, DOIs, ORCIDs, dates, and code fragments.
- Mirror directional icons only when their meaning is directional.
- Do not reverse data order merely because the page is RTL.
