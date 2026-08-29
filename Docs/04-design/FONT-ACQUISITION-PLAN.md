# Font Acquisition Plan

## Recommended technical direction

| Locale | Display | Body/UI | License target |
|---|---|---|---|
| English | Newsreader Variable | Inter Variable | SIL OFL 1.1 |
| Persian | Estedad Variable | Vazirmatn Variable | SIL OFL 1.1 |

`Vazirmatn` is the recommended primary Persian text/UI face because its official project supplies web-oriented variable files, multiple weights, and SIL OFL 1.1. `Estedad` is the recommended Persian display option: it is an Arabic-Latin variable family under OFL 1.1. This preserves a readable body face while giving headings a more distinctive, contemporary character. The owner selects the final pair when pinned binaries are added.

## Deliberately excluded until licensed

| Candidate | Decision |
|---|---|
| IRANSans | Do not add from any copied/downloaded package. It is proprietary; obtain a project-specific Fontiran license and preserve the supplied `FontLicense.txt` and required CSS license marker before reconsidering. |
| Kalameh / کلمه | Do not add based on a marketplace copy or an unverified claim of unlimited use. Add only after the owner supplies the original licensed webfont package and terms that permit this website deployment. |

## Source and provenance

- Vazirmatn: official [project repository](https://github.com/rastikerdar/vazirmatn) and `OFL.txt`; use a release-pinned variable WOFF2 source.
- Estedad: official [project repository](https://github.com/aminabedi68/Estedad) and OFL 1.1.
- English families: acquire from their official upstream/release sources and preserve their license files alongside the binaries.

## Gate before adding binaries

1. Download from the approved upstream source recorded in the authority provenance; preserve the license notice.
2. Record upstream version, SHA-256, weight/axis coverage, and source URL in the implementation handoff.
3. Create reviewed WOFF2 subsets covering the published Persian and Latin character ranges; do not claim a subset supports a character range without a fixture.
4. Define `font-display`, fallback stack, preload candidates, and font metric fallback behavior.
5. Verify computed family per locale, 200% zoom, Persian diacritics, mixed-direction strings, and layout shift within the performance budget.

No font file is currently part of this workspace. After the owner selects the final pair, the next implementation action is to add the selected open-font families with pinned version, license, checksum, and WOFF2 coverage evidence. Do not substitute IRANSans or Kalameh without the license evidence above.
