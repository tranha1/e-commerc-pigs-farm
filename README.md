
# 📘 README – Hệ thống Wagtail + PostgreSQL

Dự án này triển khai kiến trúc **SQL làm nguồn dữ liệu gốc**, **Wagtail làm UI biên tập** cho quản trị viên low‑tech, và **API** (tuỳ chọn) cho Frontend.

Cấu trúc và quy trình được chia thành 5 phần chính:

---

## 1) CSDL SQL (nguồn gốc)

- Toàn bộ dữ liệu chính (sản phẩm, nội dung trang) lưu trong **PostgreSQL**.  
- Bảng được thiết kế chuẩn hoá, có **lookup tables**, **index**, **trigger** và **view** để tối ưu.  
- Các file định nghĩa CSDL nằm trong thư mục [`sql/`](./sql):  
  - `00_extensions.sql` – bật `pg_trgm`, `btree_gin` để hỗ trợ search & index.  
  - `10_lookups.sql` – bảng lookup: đơn vị, loại lợn, danh mục thuốc, loại nội dung…  
  - `20_core_products.sql` – bảng lõi: `product_pig`, `product_medicine`.  
  - `30_cms_content.sql` – bảng chung: `cms_content_entry` cho Liên hệ/Tin tức/Quy trình.  
  - `40_images_views_triggers.sql` – bảng nối ảnh, view công khai, trigger updated_at, singleton contact.  

> **Vai trò:** SQL là **single source of truth**. FE đọc trực tiếp từ SQL view hoặc API proxy.

---

## 2) Wagtail (UI biên tập)

- Biên tập viên thao tác qua giao diện Wagtail (`/cms/`).  
- Các file liên quan trong thư mục [`core/`](./core):  
  - `pages.py` – định nghĩa Page mỏng (form nhập liệu).  
  - `sql_models.py` – ánh xạ Django Model tới bảng SQL (`managed=False`).  
  - `sync.py` – hooks publish/unpublish/delete → **upsert** vào SQL.  
  - `signals.py` – thông báo cho dev (log/webhook) khi có thay đổi.  
  - `admin.py` – (tuỳ chọn) ModelAdmin để xem bảng SQL trong Wagtail.  
  - `apps.py` – load hooks khi app khởi động.  

> **Vai trò:** Wagtail chỉ là **UI nhập liệu**. Người dùng không đụng tới SQL trực tiếp.

---

## 3) API đọc từ SQL (tuỳ chọn, khuyến nghị)

- API layer (DRF) cho FE gọi, thay vì FE query DB trực tiếp.  
- Các endpoint gợi ý:  
  - `GET /api/medicines` → đọc từ `v_medicine_public`.  
  - `GET /api/pigs` → đọc từ `v_pig_public`.  
  - `GET /api/news` → filter `cms_content_entry` kind=news.  
- File tham khảo: [`core/api.py`](./core/api.py).  

> **Vai trò:** đảm bảo FE chỉ đọc dữ liệu đã publish, với phân trang & filter ổn định.

---

## 4) Quy trình đồng bộ (flow chuẩn)

1. Biên tập viên tạo/sửa **Page** trong Wagtail.  
2. Khi **Publish**:  
   - Hook `sync.py` chạy `upsert_*()` để INSERT/UPDATE vào SQL.  
   - Nếu Page mới → tạo row mới trong SQL + gán `external_id`.  
   - Nếu Page đã có → UPDATE đúng row (idempotent).  
   - `is_published = TRUE`, `published_at = now()`.  
3. Khi **Unpublish/Delete**: set `is_published = FALSE` (soft delete).  
4. **Trigger SQL** tự động cập nhật `updated_at`.  
5. **Dev notify** qua log hoặc webhook.  
6. **FE/API** đọc từ view SQL (`v_*_public`) để hiển thị nội dung.

---

## 5) Tự động hoá & Ops

- **Makefile** (tác vụ nhanh):  
  - `make init-sql` → áp schema SQL.  
  - `make mig` → migrate Django.  
  - `make run` → chạy server local.  
  - `make createsu` → tạo superuser.  

- **apply_all.sh** (script áp SQL lần lượt 5 file).  
- **.env.example** – cấu hình môi trường (DATABASE_URL, REDIS_URL, DEV_WEBHOOK_URL…).  
- **Healthcheck**: `/healthz` trả JSON `{ok: true}`.  
- **Logging & notify**: mọi thay đổi nội dung được log và có thể gửi về Slack/Discord.  
- **Backup**: nên cron dump Postgres hàng ngày + versioning media.  

> **Vai trò:** bảo đảm dev dễ vận hành, tránh manual lặp lại, và giám sát thay đổi.

---

## 📂 Cấu trúc thư mục

```
project/
├─ sql/                      # File SQL (schema + seed)
├─ core/                     # Django app (UI + sync)
│  ├─ sql_models.py
│  ├─ pages.py
│  ├─ sync.py
│  ├─ signals.py
│  ├─ admin.py
│  ├─ apps.py
│  └─ api.py (tuỳ chọn)
├─ app/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ manage.py
├─ requirements.txt
├─ .env.example
└─ Makefile
```

---

## 🚀 Luồng tổng thể

- SQL giữ dữ liệu thật.  
- Wagtail cung cấp form nhập liệu cho quản trị viên.  
- Hooks sync giữ cho SQL luôn mới khi publish/unpublish.  
- API/FE đọc dữ liệu từ view SQL, luôn nhanh và gọn nhãn.  

---

Hết.
