> Latest review: CA-02 and PU-04-catalog are REVISE. See [catalog/graph evidence](reviews/CATALOG-GRAPH-REVIEW-2026-09-06.md); live counts and ready_for_revision are in RECONCILIATION-CHECK.json. Older counts below are historical.

> Current coordinator review: see [verification](reviews/COORDINATOR-REVIEW-2026-09-06.md). Live states and eligibility are in execution-tasks.json and RECONCILIATION-CHECK.json. Earlier counts and initial-dispatch prose are historical.

# طراحی و اجرای سایت — نسخهٔ ۲٫۱

وضعیت: **مشخصات و بسته‌های اجرا یکپارچه شدند؛ کدنویسی و پذیرش باز است.**

شروع واگذاری از **[EXECUTION.md](EXECUTION.md)** است. این صف جای جدول‌های مستقل و متداخل قبلی را می‌گیرد. هر بسته فایل‌های دقیق، مالک مخزن، وابستگی و معیار پذیرش دارد.

## اسناد اصلی

- [مشخصات ۱۵ خانوادهٔ صفحه و UI/UX](PRODUCT-SPEC.md)
- [ادمین و ویرایش محتوا](CMS-SPEC.md)
- [پوشش واقعی کد و API](COVERAGE.md)
- [قرارداد نهایی رابط‌ها و مسیرهای هدف](../../03-contracts/PRODUCT-INTERFACES-V2.md)
- [صف اجرا](EXECUTION.md) و [نسخهٔ ماشینی](execution-tasks.json)
- [نتیجهٔ یکپارچه‌سازی و کنترل](RECONCILIATION.md)
- [مشخصات هیرو و حرکت](DESIGN-SPEC.md) و [تابلوی مرور](REVIEW.html)
- [ابزارهای کاهش توکن](TOOLING.md)

## تصمیم طراحی

هویت واحد پژوهش‌محور؛ گراف در هیروی خانه، پورتال فقط در صفحهٔ انتخاب زبان. متن و کنترل‌ها HTML، صحنه Three.js و حرکت محدود GSAP. هر اثر مستقل صفحهٔ مفصل و قابل‌اشتراک دارد. محتوای روزمره، ترجمه، رسانه، رابطه و تنظیمات صفحه از ادمین مدیریت می‌شوند.

CA-01 تا CA-08 حفظ شدند. CA-09 تا CA-16 در بسته‌های خانواده ادغام شدند و جداگانه اجرا نمی‌شوند. CA-17 و PU-25-review پذیرش‌های مستقل‌اند. منابع تصویری و گزارش‌های DELIVERY-CHECK/BOARD-CHECK/EVIDENCE، شواهد تاریخ‌دارِ مرحلهٔ قبلی هستند.

PU-01، PU-02 و PU-19 در سطح مستندات تکمیل شده‌اند. باقی بسته‌ها هنوز اجرا نشده‌اند. نخستین انتخاب‌ها CA-01 و PU-03-resolver هستند؛ وابستگی‌های روز را همیشه از execution-tasks.json بخوان.

هیچ commit، push، deploy، محتوای عمومی جدید یا پیاده‌سازی Figma در این تحویل انجام نشده است.
