
# Tài liệu triển khai: Wagtail + PostgreSQL (tích hợp với dự án đã có Frontend)

**Mục tiêu:** Bạn giữ **PostgreSQL** làm nguồn dữ liệu gốc, **Wagtail** chỉ là **UI biên tập**. Khi biên tập viên publish, dữ liệu được **upsert** vào các bảng SQL. FE sẵn có có thể đọc từ **VIEW SQL** hoặc từ API do bạn viết.

> **Lưu ý:** Theo yêu cầu, tài liệu này tập trung vào **cấu hình, setup, requirements, thư viện, ứng dụng, hệ quản trị CSDL, các bước thiết lập, lưu ý** và **giải thích chi tiết từng file**. (Bỏ các mục API, bảo mật, quy trình triển khai, checklist tổng hợp — bạn sẽ tự làm).

---

## 1) Requirements & thư viện

- **Python** 3.10+
- **Django** 4.2+
- **Wagtail** 6.0+
- **PostgreSQL** 14+ (có `pg_trgm`, `btree_gin`)
- **Redis** (khuyến nghị cho cache)
- (Tuỳ chọn) **S3/Cloud Storage** cho media

**`requirements.txt` gợi ý:**

```
Django>=4.2
wagtail>=6.0
psycopg2-binary
djangorestframework
django-environ
requests
redis
whitenoise
boto3
django-storages
```

---

## 2) Cài & setup PostgreSQL

### 2.1 Cài đặt nhanh

**Ubuntu/Debian**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo systemctl enable postgresql --now
```

**macOS (Homebrew)**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Windows**
- Cài bằng trình cài đặt từ https://www.postgresql.org/download/
- Ghi nhớ `host`, `port`, `user`, `password` và phiên bản.

### 2.2 Tạo DB & user

```sql
-- Mở psql (Linux/macOS): psql -U postgres
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydb OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

### 2.3 Bật extensions (chạy trong DB `mydb`)

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;
```

> Các extension này hỗ trợ **search mờ** và **index GIN** cho truy vấn nhanh.

### 2.4 Kiểm tra kết nối

**URL kết nối:** `postgres://myuser:mypassword@localhost:5432/mydb`

```bash
psql "postgres://myuser:mypassword@localhost:5432/mydb" -c "select now();"
```

---

## 3) Tích hợp vào dự án đã có Frontend (command từng bước)

> FE của bạn đã sẵn sàng. Chúng ta thêm BE (Django/Wagtail) làm **UI biên tập** + **đồng bộ SQL**.

### 3.1 Khởi tạo Django/Wagtail (nếu chưa có)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

django-admin startproject app .      # nếu bạn chưa có project Django
python manage.py startapp core       # tạo app 'core' chứa Wagtail pages & sync
```

### 3.2 Cấu hình `settings.py`

```python
# app/settings.py
import environ, os
env = environ.Env()
environ.Env.read_env()

DEBUG = env.bool("DEBUG", False)
SECRET_KEY = env("SECRET_KEY", default="change-me")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

DATABASES = {"default": env.db()}  # DATABASE_URL
CACHES = {"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache",
                      "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1")}}

INSTALLED_APPS += [
    "rest_framework",
    "core",                   # app bạn tạo
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
DEV_WEBHOOK_URL = env("DEV_WEBHOOK_URL", default=None)
```

**`.env` mẫu**

```
DEBUG=True
SECRET_KEY=change-me
DATABASE_URL=postgres://myuser:mypassword@localhost:5432/mydb
REDIS_URL=redis://127.0.0.1:6379/1
ALLOWED_HOSTS=localhost,127.0.0.1
DEV_WEBHOOK_URL=   # nếu muốn nhận webhook khi có thay đổi
```

### 3.3 Đăng ký URL

```python
# app/urls.py
from django.urls import path, include
from django.http import JsonResponse
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

def healthz(_): return JsonResponse({"ok": True})

urlpatterns = [
    path("cms/", include(wagtailadmin_urls)),   # Wagtail admin
    path("docs/", include(wagtaildocs_urls)),   # Wagtail documents
    path("healthz", healthz),
    path("", include(wagtail_urls)),            # routing Page
]
```

### 3.4 Áp schema SQL

Bạn đã có **5 file SQL** trong thư mục `sql/`. Chạy theo thứ tự:

```bash
psql "$DATABASE_URL" -f sql/00_extensions.sql
psql "$DATABASE_URL" -f sql/10_lookups.sql
psql "$DATABASE_URL" -f sql/20_core_products.sql
psql "$DATABASE_URL" -f sql/30_cms_content.sql
psql "$DATABASE_URL" -f sql/40_images_views_triggers.sql
# (tuỳ) seed lookup
for f in sql/seed/*.sql; do psql "$DATABASE_URL" -f "$f"; done
```

### 3.5 Kích hoạt Wagtail & tạo superuser

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Truy cập **http://localhost:8000/cms/** để vào Wagtail Admin.

---

## 4) Hướng dẫn sử dụng từng file & vai trò

### 4.1 **SQL — file-by-file**

#### `00_extensions.sql`
- Bật `pg_trgm`, `btree_gin`.
- **Vai trò:** tăng tốc tìm kiếm mờ (`ILIKE`/trgm) và index GIN hỗ trợ các truy vấn list/search.

#### `10_lookups.sql`
Tạo các bảng **lookup** để tránh trùng lặp chuỗi và tối ưu join:
- `lu_unit(id, code, label)`: đơn vị bán (*con, hộp, chai…*).
- `lu_dose_unit(id, code, label)`: đơn vị liều (*ml, viên, g…*).
- `lu_medicine_category(id, slug, name)`: nhóm thuốc (*kháng sinh tiêm, bột…*).
- `lu_medicine_line(id, name)`: dòng thuốc.
- `lu_pig_type(id, code, label)`: loại lợn (*breeding/sow*).
- `lu_pig_breed_line(id, name)`: dòng/giống lợn.
- `lu_content_kind(id, code, label)`: loại nội dung (*contact/news/process*).

**Vai trò:** chuẩn hoá dữ liệu (không nhập trùng “Hộp/hộp/box…”), giảm kích thước index, filter nhanh hơn.

#### `20_core_products.sql`
Bảng lõi cho **sản phẩm**:

- `product_pig`  
  - **Cột chính:**  
    - `pig_type_id` → `lu_pig_type` (*breeding/sow*)  
    - `name`, `breed_line_id` → `lu_pig_breed_line`, `unit_id` → `lu_unit`, `price`, `note`  
    - `is_featured`, `cover_image_id` (ID ảnh Wagtail), `slug`  
    - `is_published`, `published_at`, `created_at`, `updated_at`  
  - **Ràng buộc:** `uq_pig_type_name (pig_type_id, LOWER(name))` (tránh trùng sản phẩm cùng loại)  
  - **Index:** `idx_pig_pub`, `idx_pig_name_trgm`

- `product_medicine`  
  - **Cột chính:**  
    - `name`, `category_id` → `lu_medicine_category`, `line_id` → `lu_medicine_line`  
    - `ingredients`, `indications`, `packaging`  
    - `unit_id` → `lu_unit`, `price_unit`, `price_total`  
    - `dose_unit_id` → `lu_dose_unit`, `price_per_dose`, `support_price_per_dose`  
    - `is_featured`, `cover_image_id`, `slug`, `is_published`, `published_at`…  
  - **Ràng buộc:** `uq_med_name (LOWER(name))`  
  - **Index:** `idx_med_pub_time`, `idx_med_name_trgm`, `idx_med_pack_trgm`

**Vai trò:** chứa dữ liệu sản phẩm phục vụ FE; `is_published/published_at` hỗ trợ phân trang ổn định.

#### `30_cms_content.sql`
Bảng chung cho **Liên hệ / Tin tức / Quy trình**:
- `cms_content_entry(kind_id, slug, title, summary, body_json, body_html, video_url, external_url, cover_image_id, author_name, seo_*, is_published, published_at, updated_at)`
- **Unique:** `(kind_id, slug)` tránh lẫn dữ liệu giữa các trang.
- **Index:** `idx_cms_kind_pub_time`, `idx_cms_slug_trgm`, `idx_cms_title_trgm`.

**Vai trò:** một nguồn dữ liệu chung để quản lý ba loại nội dung; gắn `kind_id` để phân loại.

#### `40_images_views_triggers.sql`
- **Bảng nối ảnh:**  
  - `product_pig_image(pig_id, image_id, sort)`  
  - `product_medicine_image(medicine_id, image_id, sort)`  
  - Index `(entity_id, sort)` để lấy gallery theo thứ tự.

- **VIEWs công khai cho FE:**  
  - `v_pig_public`: join lookup để xuất `pig_type`, `breed_line`, `unit` dưới dạng **nhãn**.  
  - `v_medicine_public`: join lookup để xuất `category`, `product_line`, `unit`, `dose_unit` **đã resolve**.

- **TRIGGER:**  
  - `touch_updated_at()` + `trg_touch_*`: tự cập nhật `updated_at` trước `UPDATE`.  
  - `enforce_singleton_contact()` + triggers: bảo đảm **chỉ 1** bản ghi `contact` được publish.

**Vai trò:** giảm JOIN phía FE, tăng tốc, giữ **fresh cache** dựa vào `updated_at`, đảm bảo ràng buộc nghiệp vụ (singleton contact).

---

### 4.2 **Wagtail UI — file-by-file**

> Các file này nằm trong `core/`.

#### `core/sql_models.py` (Managed=False)
- Map Django models tới **bảng SQL gốc** (`db_table=...`, `managed=False`), ví dụ:
  - `Medicine` → `product_medicine`
  - `Pig` → `product_pig`
  - `CmsContentEntry` → `cms_content_entry`
- **Vai trò:** Cho phép code Python **đọc/ghi** các bảng SQL **mà không** để Django tạo/migrate bảng.

#### `core/pages.py`
- Định nghĩa các **Page mỏng** (form nhập liệu cho low-tech), ví dụ:
  - `MedicineProductPage(name, packaging, price_unit, price_total, external_id)`
  - `PigPage(name, price, external_id)`
- Trường `external_id` dùng để **liên kết** Page ↔ **row SQL** đã upsert (idempotent).  
- **Vai trò:** Biên tập viên thao tác trên UI Wagtail; không cần biết SQL.

#### `core/sync.py`
- **Hooks** Wagtail:
  - `after_publish_page` → `upsert_*()` → ghi/đổi `is_published/published_at` trong SQL.
  - `after_unpublish_page` / `after_delete_page` → **soft-unpublish** trong SQL.
- **Idempotent**: nếu `external_id` đã có → `UPDATE`; nếu chưa → `INSERT` + gắn `external_id`.
- Dùng `transaction.atomic()` và `select_for_update()` (khi update) để tránh race condition.
- **Vai trò:** Cầu nối “Page → SQL”, bảo đảm dữ liệu nhất quán.

#### `core/signals.py`
- `notify_dev(message)`: ghi log + gửi webhook (Slack/Discord/Teams) nếu cấu hình `DEV_WEBHOOK_URL`.
- **Vai trò:** Thông báo cho dev khi nội dung thay đổi (giúp theo dõi/giám sát).

#### `core/admin.py` (tuỳ chọn)
- Đăng ký **ModelAdmin** cho bảng SQL để xem nhanh trong Wagtail admin.
- **Vai trò:** Quan sát dữ liệu SQL từ giao diện Wagtail; có thể chỉnh sửa nếu bạn cho phép.

#### `core/apps.py`
- Đảm bảo load `sync.py` khi app khởi động:
  ```python
  from django.apps import AppConfig
  class CoreConfig(AppConfig):
      name = "core"
      def ready(self):
          from . import sync  # noqa: F401
  ```

---

## 5) Luồng vận hành (tóm tắt ngắn)

1. Biên tập viên tạo/sửa **Page** → **Publish** trong Wagtail.
2. Hook **upsert** Page vào bảng SQL (insert/update), đặt `is_published=True`.
3. **Triggers SQL** tự động cập nhật `updated_at` (hỗ trợ cache invalidate).
4. Dev nhận **thông báo** (log/webhook) về thay đổi.
5. FE (đã có) có thể đọc từ **VIEW SQL** hoặc API bạn tự triển khai.

---

## 6) Lưu ý & mẹo tối ưu

- Giữ **một nguồn sự thật**: SQL là gốc; Page chỉ là form + workflow.
- Đảm bảo **unique** (tên/slug) ở **SQL**; code sync tuân thủ (bắt lỗi trùng).  
- Phân trang ổn định với `ORDER BY published_at DESC, id DESC`.  
- Dùng **lookup tables** để chuẩn hoá và filter nhanh.  
- `external_id` trên Page giúp **idempotent** (publish nhiều lần không tạo trùng).  
- Với ảnh: nếu cần gallery, dùng bảng nối `product_*_image` và lưu `image_id` từ Wagtail Images.  
- (Prod) Nên bật Redis cache, CDN cho media, backup DB hằng ngày.

---

### Phụ lục: Lệnh nhanh (copy/paste)

```bash
# 1) Cài gói
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) DB & Schema
export DATABASE_URL=postgres://myuser:mypassword@localhost:5432/mydb
psql "$DATABASE_URL" -f sql/00_extensions.sql
psql "$DATABASE_URL" -f sql/10_lookups.sql
psql "$DATABASE_URL" -f sql/20_core_products.sql
psql "$DATABASE_URL" -f sql/30_cms_content.sql
psql "$DATABASE_URL" -f sql/40_images_views_triggers.sql

# 3) Django/Wagtail
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# → mở http://localhost:8000/cms/ (tạo Page, Publish, dữ liệu sẽ upsert sang SQL)
```

> Hết.
