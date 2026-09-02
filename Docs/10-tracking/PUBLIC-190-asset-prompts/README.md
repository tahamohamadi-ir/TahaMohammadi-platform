# PUBLIC-190 — Asset generation prompt pack

**وضعیت:** `PUBLIC-190` هنوز **`REVISE`** — این پرامپت‌ها فقط برای تولید/بازتولید **آرت تزئینی** هستند؛ محتوای CMS (عنوان، تاریخ، نام، لینک) را از این تصاویر استخراج نکنید.

## خلاصه (فارسی)

این پوشه برای هر **گپ بصری مشخص** یک فایل پرامپت انگلیسی دارد. خروجی را در Nano Banana یا ChatGPT ImageGen بسازید و فایل PNG اصلی را طبق مسیر drop-in هر فایل برگردانید. پس از تأیید شما، تیم در `ASSET-PROMOTION-LEDGER.md` ثبت و در `Front-End/public-site/src/assets/media/` promote می‌کند.

**اولویت‌ها**

| سطح | معنی | اقدام |
|---|---|---|
| **P0** | هیرو، backplate، constellation، thumbnail اصلی — مقایسه compare-report ضعیف | تولید فوری |
| **P1** | پروژه/مسیر یادگیری/تماس/About — fidelity متوسط | بعد از P0 |
| **P2** | placeholder صریح «کار آینده» — هرگز به slug واقعی وصل نشود | فقط UI صادق |

**فرآیند**

1. فایل پرامپت را باز کنید → پرامپت اصلی + negative را کپی کنید.
2. اگر concept reference دارد، همان PNG را به عنوان reference image بدهید.
3. خروجی: PNG بدون متن (مگر concept صریح متن داشته باشد — در runtime ما overlay HTML داریم).
4. نام فایل و مسیر drop-in را **دقیق** از همان فایل پرامپت بگیرید.
5. SHA-256 و ابعاد را برای ledger یادداشت کنید.

**اسناد مرتبط**

- [PUBLIC-190-VISUAL-QA.md](../PUBLIC-190-VISUAL-QA.md)
- [PUBLIC-190-VISUAL-REMEDIATION-PLAN.md](../PUBLIC-190-VISUAL-REMEDIATION-PLAN.md)
- [PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md](../PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md)
- [ASSET-PROMOTION-LEDGER.md](../../04-design/ASSET-PROMOTION-LEDGER.md)

---

## Prompt index

| Priority | Asset ID | File | Used on |
|:---:|:---|:---|:---|
| P0 | `portal-orbit-light` | [portal-orbit-light.md](./portal-orbit-light.md) | Home hero atmosphere (light) |
| P0 | `portal-orbit-dark` | [portal-orbit-dark.md](./portal-orbit-dark.md) | Home hero atmosphere (dark) |
| P0 | `portal-centered-light` | [portal-centered-light.md](./portal-centered-light.md) | Gateway + contact atmosphere (light) |
| P0 | `portal-centered-dark` | [portal-centered-dark.md](./portal-centered-dark.md) | Gateway + contact atmosphere (dark) |
| P0 | `home-graph-backplate-light` | [home-graph-backplate-light.md](./home-graph-backplate-light.md) | Home graph + PF-05 constellation (light) |
| P0 | `home-graph-backplate-dark` | [home-graph-backplate-dark.md](./home-graph-backplate-dark.md) | Home graph + PF-05 constellation (dark) |
| P0 | `gallery-ivory-forms` | [gallery-ivory-forms.md](./gallery-ivory-forms.md) | PF-01 creative hero / grid previews |
| P0 | `blog-coral-stairs` | [blog-coral-stairs.md](./blog-coral-stairs.md) | PF-03 writing hero / rail |
| P0 | `learning-sage-library` | [learning-sage-library.md](./learning-sage-library.md) | PF-06 teaching hero / library rows |
| P1 | `project-data-architecture` | [project-data-architecture.md](./project-data-architecture.md) | PF-04 projects hero / row thumbs |
| P1 | `project-dashboard-systems` | [project-dashboard-systems.md](./project-dashboard-systems.md) | Home + PF-04 project server illustration |
| P1 | `project-visual-communication-network` | [project-visual-communication-network.md](./project-visual-communication-network.md) | Deferred project cover (promotion pending) |
| P1 | `pf-creative-hero-editorial-light` | [pf-creative-hero-editorial-light.md](./pf-creative-hero-editorial-light.md) | PF-01 tall hero panel (new slot) |
| P1 | `pf-contact-atmosphere-dark` | [pf-contact-atmosphere-dark.md](./pf-contact-atmosphere-dark.md) | PF-08 contact hero glow (new slot) |
| P1 | `pf-about-identity-abstract-light` | [pf-about-identity-abstract-light.md](./pf-about-identity-abstract-light.md) | PF-07 About portrait placeholder |
| P1 | `pf-teaching-path-ribbon-dark` | [pf-teaching-path-ribbon-dark.md](./pf-teaching-path-ribbon-dark.md) | PF-06 featured path band |
| P2 | `project-placeholder-ivory-stairs` | [project-placeholder-ivory-stairs.md](./project-placeholder-ivory-stairs.md) | Honest future-work placeholder only |
