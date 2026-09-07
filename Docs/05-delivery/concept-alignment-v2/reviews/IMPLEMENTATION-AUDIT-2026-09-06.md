# بازبینی اجرای ایجنت‌ها — ۲۰۲۶/۰۹/۰۶

نتیجه: پیشرفت واقعی وجود دارد؛ مجموعه هنوز آمادهٔ پذیرش یکپارچه یا انتشار نیست. این گزارش بازبینی است، نه اعلام تکمیل بسته‌ها. کد محصول، وضعیت پذیرش مرکزی و تاریخچهٔ handoff در این بررسی تغییر نکردند.

## وضعیت واقعی

فهرست ماشینی همراه، HEAD و وضعیت Git چهار مخزن و SHA-256 گزارش‌های تحویل را ثبت می‌کند: [inventory](IMPLEMENTATION-AUDIT-2026-09-06.json).

| بخش | شواهد محلی | نتیجه |
|---|---|---|
| BACKEND | ۱۹ handoff؛ مدل‌ها، migrationها، API، محتوای غنی، درس، مجموعه، نسخه‌ها، preview، jobs و analytics اضافه شده‌اند | پیاده‌سازی موجود؛ نیازمند اصلاح و پذیرش یکپارچه |
| PUBLIC | CA-01 تا CA-08 و PU-SYNC-graph موجود؛ Three.js و GSAP، هیروی ادغام‌شده و پورتال gateway اضافه شده‌اند | پیشرفت واقعی؛ اتصال داده و قراردادها کامل نیست |
| PUBLIC final sync | PU-SYNC-public_BLOCKED | انجام نشده |
| ADMIN | ۶ handoff همگی BLOCKED؛ تغییر کد قابلیت‌های جدید مشاهده نشد | editor، transport، host و دو editor خانواده ساخته نشده‌اند |
| ROOT runner | runner، تنظیمات ingress و runbook اضافه شده‌اند | خطاهای مهم در مسیر حذف/انتشار؛ قابل انتشار نیست |

سه جدول ارسالی فهرست واگذاری هستند، نه شواهد اتمام. در صف مرکزی همچنان NOT_STARTED/REVISE دیده می‌شود، در حالی که کد و handoff بسیاری از بسته‌ها موجود است. وجود HANDOFF_READY به معنی پذیرش وابستگی نیست؛ توقف ایجنت ادمین در این وضعیت منطقی بوده است.

## آزمون‌های مستقل این بازبینی

| بررسی | نتیجه |
|---|---|
| BACKEND: `uv run pytest -q` | ۸۴۸ موفق، ۱۴ ناموفق |
| BACKEND: `uv run ruff check .` | موفق |
| BACKEND: `uv run python manage.py makemigrations --check --dry-run --settings=config.settings.test` | بدون migration جاافتاده؛ اثبات backout روی دادهٔ واقعی نیست |
| PUBLIC: `npm.cmd test` | ۳۴۰ موفق، ۳ ناموفق، ۶۰ فایل تست |
| PUBLIC: `npm.cmd run lint` | موفق |
| PUBLIC: `npm.cmd run validate:design` | موفق، overlay 2.1.0 |
| PUBLIC: Playwright CA-06 و CA-07، دو worker | ۲۰ موفق، ۱ skipped |
| ROOT: `python Infra/staging/test_rebuild_product.py` | ۸ موفق |

تست مرورگر resize/theme هیروی آماده به دلیل آماده‌نبودن داده skip شد. تست‌های fallback و gateway جای پذیرش بصری هیروی دارای داده را نمی‌گیرند. build محلی توسط harness آزمون انجام شد؛ staging در این بازبینی بررسی یا deploy نشد. تست کامل ADMIN اجرا نشد چون کد قابلیت‌های واگذارشده در آن وجود ندارد.

۱۴ شکست BACKEND: دو assertion قدیمی شمارش entity/فیلد، سه fixture قدیمی article/publication/project، و نه assertion مربوط به hash/shape/provenance پذیرش قبلی. این شکست‌ها عمدتاً همگام‌سازی قرارداد هستند؛ نباید با حذف آزمون یا صرفاً جایگزینی hash پنهان شوند.

سه شکست PUBLIC: ممنوعیت ماندگار Three.js در foundation:435، بررسی diff کل checkout به نام CA-01 در foundation:590، و pin قدیمی OpenAPI در public-310.contract-fixtures.test.ts:54.

## اصلاحات لازم، به ترتیب اولویت

### A01 — حذف یک مطلب نباید صفحهٔ اصلی و آرشیو را حذف کند — P1

مالک: BACKEND PU-23-invalidation + ROOT PU-07-runner، به ترتیب و با handoff رابط.

`Back-End/apps/rebuild/services.py:300` صفحهٔ اصلی را در affectedPaths تمام محتوا قرار می‌دهد؛ برای مقاله، blog و صفحهٔ جزئیات هم اضافه می‌شوند. `Infra/staging/rebuild-product.py:382` همهٔ همین مسیرها را هنگام archive وارد deny می‌کند. پس با فعال شدن deny، archive یک مقاله می‌تواند home و blog را هم 404 کند. این منع بعد از موفقیت job حذف نیز باقی می‌ماند.

اقدام: مسیرهای نیازمند rebuild را از مسیرهای واقعاً revoked جدا کنید؛ قرارداد و schema این تمایز را ثبت کنند. آزمون: archive مقاله فقط جزئیات/فایل همان مقاله را مسدود کند، home/blog در دسترس بمانند، و لینک مقاله از index/search حذف شود.

### A02 — تأیید حذف در edge واقعی نیست — P1

مالک: ROOT PU-07-runner.

`EdgeDenyManager.verify_effective` در `Infra/staging/rebuild-product.py:191` فقط متن همان فایل نوشته‌شده را می‌خواند. nginx map در تنظیمات بارگذاری می‌شود؛ مسیر runner هیچ مرحلهٔ اعمال/reload تنظیمات یا probe HTTP ندارد. با این حال callback مقدار effective اعلام می‌کند.

اقدام: اعمال کنترل‌شدهٔ deny با اعتبارسنجی تنظیمات و بررسی HTTP از ingress واقعی؛ اگر reload/probe شکست خورد، effective اعلام نشود. آزمون مستقل: فایل موجود + edge بدون تغییر باید شکست بخورد. تست فعلی هشت‌تایی این رفتار واقعی را نمی‌سنجد.

### A03 — چرخهٔ runner و job هنوز یکپارچه نیست — P1

مالک: BACKEND PU-07-jobs سپس ROOT PU-07-runner.

در `Back-End/apps/rebuild/services.py:209` اجرای rebuild فوراً انجام می‌شود، حتی وقتی caller در transaction است؛ job_id به runner جدید پاس داده نمی‌شود. مسیر legacy bash باقی است و Compose مقدار REBUILD_TRIGGER_ENABLED=false دارد. در runner:376 پاسخ ناموفق transition به running نادیده گرفته می‌شود و اجرای build ادامه می‌یابد. job با revision خالی نیز release مجزای معتبر ندارد.

اقدام: dispatch/claim واقعی بعد از commit با job ID، جلوگیری از اجرای هم‌زمان/تکراری و توقف در 409؛ revision امن و غیرخالی برای هر artifact. آزمون rollback تراکنش، دو runner برای یک job، رد claim، و restart worker. موفقیت Pagefind/sitemap و artifact باید پیش از swap بررسی شود؛ وجود index.html به‌تنهایی کافی نیست.

### A04 — restore والد، نسخهٔ عمومی آن را حفظ نمی‌کند — P1

مالک: BACKEND PU-07-revisions با اصلاح allowlist برای public API و lifecycle.

snapshot در projection داستان مصرف می‌شود (`apps/composition/projection.py:271`)؛ اما public endpoint والد مثل article همچنان `Article.objects.public()` می‌خواند (`apps/api/api.py:608`). restore والد را draft می‌کند و PU-23 در admin_content:1790 برای آن removal هم enqueue می‌کند. بنابراین snapshot ذخیره‌شدهٔ والد تضمین نمی‌کند نسخهٔ منتشرشده بعد از restore باقی بماند؛ این با هدف حفظ نسخهٔ عمومی تا انتشار صریح ناسازگار است. تست موجود عمدتاً projection داستان را با snapshot دستی می‌سنجد.

اقدام: خواندن public از نسخهٔ منتشرشدهٔ والد/روابط، با archive صریح به‌عنوان عمل جدا. آزمون HTTP کامل publish → edit/restore draft → GET همان URL باید نسخهٔ منتشرشده را نشان دهد؛ publish مجدد نسخهٔ جدید را فعال کند. انتشار زمان‌بندی‌شده نیز باید snapshot یکسان بسازد.

### A05 — resolver ساخته شده ولی به Home وصل نیست — P1

مالک: PUBLIC CA-02/CA-03.

هر دو `src/pages/en/index.astro:20` و `src/pages/fa/index.astro:20` فقط `loadHeroGraph(locale)` را صدا می‌زنند. loader در `src/lib/hero-graph-content.ts:539` callback اختیاری را عبور می‌دهد؛ هیچ مصرف runtime از endpoint resolve مشاهده نشد. در نتیجه شناسه‌های مرتبط در Home به لینک کار واقعی تبدیل نمی‌شوند، حتی اگر backend آن‌ها را بشناسد.

اقدام: جمع‌آوری/dedupe شناسه‌ها، resolve دسته‌های حداکثر ۵۰تایی، نگاشت مسیر canonical با locale دقیق و fallback امن؛ سپس اتصال به loader واقعی. آزمون باید مسیر fetch تا لینک رندرشدهٔ صفحه را بسنجد، نه فقط callback مصنوعی adapter.

### A06 — قواعد CA-01 هنوز بسته‌های بعدی را می‌شکنند — P2

مالک: PUBLIC CA-01، اصلاحیهٔ R1 ناقص مانده است.

با وجود توضیح کامنت، absence assertion همچنان package.json زنده را می‌خواند و نصب مجاز Three در CA-04 را رد می‌کند. تست دیگر diff کل checkout را به CA-01 نسبت می‌دهد.

اقدام: کنترل عدم تغییر dependency در تحویل CA-01 را به artifact/diff همان بسته محدود کنید؛ آن را invariant دائمی محصول نگذارید. قواعد portal/order/hash تاریخی و سناریوهای مثبت/منفی validator محفوظ بمانند. اجرای کامل PUBLIC باید سبز شود.

### A07 — قراردادهای تولیدشده و مصرف‌کنندگان ناهماهنگ‌اند — P2

مالک: BACKEND contract reconciliation → PUBLIC/ADMIN sync.

اقدام: پس از اصلاحات رفتاری، export جدید از source، مقایسهٔ معنایی schema با baseline، fixtureهای پاسخ واقعی، پذیرش snapshot با hash دقیق، سپس تولید types و هماهنگی pinها. historical acceptance را پاک نکنید؛ نسخهٔ پذیرش جدید ثبت کنید. ۱۴ شکست BACKEND و شکست hash PUBLIC باید با بررسی تفاوت‌های مجاز رفع شوند.

پس از این مرحله PU-SYNC-admin و PU-SYNC-public قابل ادامه‌اند؛ سپس transport → editor → host → editorهای خانواده. تغییر برچسب NOT_STARTED به COMPLETE بدون شواهد این مشکل را حل نمی‌کند.

### A08 — bulk archive زبان‌ها را مخلوط می‌کند — P2

مالک: BACKEND PU-23-invalidation.

`apps/content/services/lifecycle.py:185` تمام مسیرها را در یک job جمع می‌کند و locale را از آخرین item می‌گیرد؛ برخلاف گزارش تحویل، گروه‌بندی به ازای locale انجام نمی‌شود.

اقدام: یک job مستقل برای هر locale یا job چندزبانهٔ صریح در قرارداد؛ آزمون bulk شامل fa و en و بررسی مسیر/locale هر job.

### A09 — analytics فقط شکل رشته را بررسی می‌کند — P2

مالک: BACKEND PU-20-events.

در `apps/analytics/api.py` pagePath فقط slash/فاصله/query/طول و target فقط regex بررسی می‌شوند؛ مسیر ثبت‌نشده یا نام اکشن دلخواه با شکل مجاز پذیرفته می‌شود. این با I07 که canonical path و registered action ID می‌خواهد متفاوت است. خطاهای endpoint جدید نیز با HttpError به شکل قدیمی برمی‌گردند.

اقدام: registry اکشن، validator مسیر canonical همراه locale، envelope جدید و آزمون مقصد ناشناخته/زبان متناقض/خطا. سخت‌گیری اندازهٔ payload و same-origin نیز با موارد منفی سنجیده شود؛ صرف ذخیره‌نکردن visitor ID کافی نیست.

### A10 — ثبت nonce پیش از صحت امضا — P2

مالک: BACKEND PU-07-jobs.

در `apps/rebuild/services.py:166` nonce پیش از بررسی HMAC در خط 180 در دیتابیس نوشته می‌شود. درخواست با امضای غلط می‌تواند state ایجاد کند و nonce را مصرف کند.

اقدام: بررسی امضا پیش از ثبت اتمیک nonce؛ آزمون امضای نامعتبر هیچ nonce نسازد، و replay درخواست معتبر رد شود. دسترسی واقعی خارجی به endpoint داخلی در این بازبینی ارزیابی نشده است.

## ترتیب ادامه و محدودیت پذیرش

1. A01–A04 و A08/A10 را در بسته‌های کوچک با مالکیت فایل روشن اصلاح کنید؛ jobs/services بین چند بسته مشترک‌اند و هم‌زمان ویرایش نشوند.
2. A05/A06 در PUBLIC و A09 در BACKEND انجام شوند؛ آزمون‌های regression موارد بالا به تست‌های بسته اضافه شوند.
3. A07 قراردادها را تثبیت کند؛ سپس صف مرکزی، TASK-LIST مخزن و handoffها با وضعیت واقعی بازبینی هماهنگ شوند.
4. ادمین از PU-SYNC-admin ادامه یابد؛ گزارش‌های BLOCKED فعلی نباید اجرای editor تلقی شوند. صفحات جزئیات خانواده‌ها نیز هنوز تکمیل این موج نیستند.
5. برای هیروی دارای دادهٔ واقعی، FA/EN و light/dark در موبایل/دسکتاپ، انتخاب گره، لینک اثر، no-JS و WebGL failure را بررسی بصری کنید. CA-08 عمدتاً یک اصلاح accessible name بوده، نه شاهد بازطراحی کامل shell مطابق کانسپت.

این گزارش بررسی خط‌به‌خط تمامی ۱۹ بستهٔ بک‌اند یا تأیید امنیت/مهاجرت/طراحی کل پروژه نیست. یافته‌های بالا از آزمون‌های اجراشده و مسیرهای کد ذکرشده‌اند؛ rollout واقعی، migration روی کپی داده و پذیرش بصری هنوز باز هستند. هیچ commit/push/deploy در این بازبینی انجام نشد.
