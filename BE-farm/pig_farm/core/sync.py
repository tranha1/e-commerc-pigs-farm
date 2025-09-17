
from django.db import transaction, DatabaseError
from wagtail import hooks
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
import logging
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from . import sql_models
from .pages import MedicineProductPage, PigPage, PigImagePage, NewsCategoryPage
from .signals import notify_dev

logger = logging.getLogger(__name__)

def upsert_medicine(page: MedicineProductPage):
    """Sync MedicineProductPage to SQL medicine table."""
    try:
        with transaction.atomic():
            if page.external_id:
                try:
                    obj = sql_models.Medicine.objects.get(id=page.external_id)
                except sql_models.Medicine.DoesNotExist:
                    obj = sql_models.Medicine()
                    page.external_id = None
            else:
                obj = sql_models.Medicine()
            obj.name = page.name
            obj.packaging = page.packaging or None
            obj.price_unit = page.price_unit
            obj.price_total = page.price_total
            obj.is_published = True
            obj.published_at = timezone.now()
            obj.is_deleted = False
            obj.deleted_at = None
            obj.save()
            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])
        notify_dev(f"✅ [Wagtail] Medicine upserted → SQL: {page.title} (id={page.external_id})")
    except DatabaseError as e:
        logger.error(f"Medicine sync failed for {page.title}: {e}")
        notify_dev(f"❌ [Wagtail] Medicine sync failed: {page.title} - {str(e)}")

def upsert_pig(page: PigPage):
    """Sync PigPage to SQL pig table."""
    try:
        with transaction.atomic():
            if page.external_id:
                try:
                    obj = sql_models.Pig.objects.get(id=page.external_id)
                except sql_models.Pig.DoesNotExist:
                    obj = sql_models.Pig()
                    page.external_id = None
            else:
                obj = sql_models.Pig()
            obj.name = page.name
            obj.price = page.price
            obj.is_published = True
            obj.published_at = timezone.now()
            obj.is_deleted = False
            obj.deleted_at = None
            obj.save()
            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])
        notify_dev(f"✅ [Wagtail] Pig upserted → SQL: {page.title} (id={page.external_id})")
    except DatabaseError as e:
        logger.error(f"Pig sync failed for {page.title}: {e}")
        notify_dev(f"❌ [Wagtail] Pig sync failed: {page.title} - {str(e)}")


def upsert_pig_image(page: PigImagePage):
    """Sync PigImagePage to SQL pig_images table"""
    try:
        with transaction.atomic():
            if page.external_id:
                try:
                    obj = sql_models.PigImage.objects.get(id=page.external_id)
                except sql_models.PigImage.DoesNotExist:
                    obj = sql_models.PigImage()
                    page.external_id = None
            else:
                obj = sql_models.PigImage()
            
            obj.title = page.title
            obj.description = page.description or None
            obj.image_url = page.image.file.url if page.image else None
            obj.pig_id = page.pig_reference.external_id if page.pig_reference and page.pig_reference.external_id else None
            obj.image_type = page.image_type
            obj.file_size = page.file_size
            obj.width = page.width
            obj.height = page.height
            obj.is_published = True
            obj.published_at = timezone.now()
            obj.is_deleted = False
            obj.deleted_at = None
            obj.save()
            
            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])
                
        notify_dev(f"✅ [Wagtail] PigImage upserted → SQL: {page.title} (id={obj.id})")
        
    except sql_models.PigImage.DoesNotExist:
        logger.error(f"PigImage with id={page.external_id} not found for {page.title}")
        notify_dev(f"❌ [Wagtail] PigImage not found for {page.title} (id={page.external_id})")
    except DatabaseError as e:
        logger.error(f"Database error during PigImage sync for {page.title}: {e}")
        notify_dev(f"❌ [Wagtail] Database error for {page.title}: {str(e)}")


def upsert_news_category(page: NewsCategoryPage):
    """Sync NewsCategoryPage to SQL news_categories table"""
    try:
        with transaction.atomic():
            if page.external_id:
                try:
                    obj = sql_models.NewsCategory.objects.get(id=page.external_id)
                except sql_models.NewsCategory.DoesNotExist:
                    obj = sql_models.NewsCategory()
                    page.external_id = None
            else:
                obj = sql_models.NewsCategory()
            
            obj.name = page.title
            obj.slug = page._slug_value()
            obj.description = page.description or None
            obj.color = page.color
            obj.icon = page.icon
            obj.parent_id = page.parent_category.external_id if page.parent_category and page.parent_category.external_id else None
            obj.sort_order = page.sort_order
            obj.is_published = True
            obj.published_at = timezone.now()
            obj.is_deleted = False
            obj.deleted_at = None
            obj.save()
            
            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])
                
        notify_dev(f"✅ [Wagtail] NewsCategory upserted → SQL: {page.title} (id={obj.id})")
        
    except sql_models.NewsCategory.DoesNotExist:
        logger.error(f"NewsCategory with id={page.external_id} not found for {page.title}")
        notify_dev(f"❌ [Wagtail] NewsCategory not found for {page.title} (id={page.external_id})")
    except DatabaseError as e:
        logger.error(f"Database error during NewsCategory sync for {page.title}: {e}")
        notify_dev(f"❌ [Wagtail] Database error for {page.title}: {str(e)}")

@hooks.register("after_delete_page")
def on_delete(request, page):
    if isinstance(page, MedicineProductPage) and page.external_id:
        # Soft delete cho admin
        sql_models.Medicine.objects.filter(id=page.external_id).update(is_deleted=True, is_published=False)
        notify_dev(f"[Wagtail] Medicine soft-deleted: {page.title} (id={page.external_id})")
    if isinstance(page, PigPage) and page.external_id:
        sql_models.Pig.objects.filter(id=page.external_id).update(is_deleted=True, is_published=False)
        notify_dev(f"[Wagtail] Pig soft-deleted: {page.title} (id={page.external_id})")

@hooks.register("after_publish_page")
def on_publish(request, page):
    if isinstance(page, MedicineProductPage):
        upsert_medicine(page)
    elif isinstance(page, PigPage):
        upsert_pig(page)
    elif isinstance(page, PigImagePage):
        upsert_pig_image(page)
    elif isinstance(page, NewsCategoryPage):
        upsert_news_category(page)


@hooks.register("after_unpublish_page")
def on_unpublish(request, page):
    """Mark SQL record as unpublished."""
    try:
        model_mapping = {
            MedicineProductPage: (sql_models.Medicine, "Medicine"),
            PigPage: (sql_models.Pig, "Pig"),
            PigImagePage: (sql_models.PigImage, "PigImage"),
            NewsCategoryPage: (sql_models.NewsCategory, "NewsCategory"),
        }
        model, model_name = model_mapping.get(type(page), (None, None))
        if model and page.external_id:
            model.objects.filter(id=page.external_id).update(is_published=False)
            notify_dev(f"📤 [Wagtail] {model_name} unpublished: {page.title} (id={page.external_id})")
    except DatabaseError as e:
        logger.error(f"Unpublish failed for {page.title}: {e}")
        notify_dev(f"❌ [Wagtail] Unpublish failed: {page.title} - {str(e)}")


@hooks.register("before_delete_page")
def prevent_hard_delete_and_log(request, page):
    """
    Block all hard deletes, including for superusers.
    Only developers can delete directly in the database.
    """
    # Log delete attempt đầu tiên
    logger.info(f"🔍 DELETE ATTEMPT: {page.__class__.__name__} '{page.title}' by {request.user.username}")
    notify_dev(f"🔍 [DEBUG] Delete attempt: {page.__class__.__name__} '{page.title}' by {request.user.username}")
    
    if isinstance(page, (MedicineProductPage, PigPage, PigImagePage, NewsCategoryPage)):
        logger.info(f"🚫 Blocking hard delete for {page.title} by user {request.user.username} (superuser: {request.user.is_superuser})")
        
        raise PermissionDenied(
            f"⛔ DELETE BLOCKED! "
            f"Cannot delete '{page.title}'. "
            f"Only developers can delete directly in the database. "
            f"Please use 'Unpublish' instead."
        )


@hooks.register("after_delete_page")
def handle_soft_delete_fallback(request, page):
    """
    Fallback handler - nếu somehow page vẫn bị delete, thực hiện soft delete
    """
    if isinstance(page, (MedicineProductPage, PigPage, PigImagePage, NewsCategoryPage)):
        logger.warning(f"🚨 FALLBACK: Page was deleted despite prevention: {page.title}")
        
        try:
            current_time = timezone.now()
            
            # Thực hiện soft delete trong SQL database
            if isinstance(page, MedicineProductPage) and page.external_id:
                sql_models.Medicine.objects.filter(id=page.external_id).update(
                    is_published=False,
                    is_deleted=True,
                    deleted_at=current_time
                )
                notify_dev(f"🗑️ [FALLBACK SOFT DELETE] Medicine: {page.title} (id={page.external_id})")
                
            elif isinstance(page, PigPage) and page.external_id:
                sql_models.Pig.objects.filter(id=page.external_id).update(
                    is_published=False,
                    is_deleted=True,
                    deleted_at=current_time
                )
                notify_dev(f"🗑️ [FALLBACK SOFT DELETE] Pig: {page.title} (id={page.external_id})")
                
            elif isinstance(page, PigImagePage) and page.external_id:
                sql_models.PigImage.objects.filter(id=page.external_id).update(
                    is_published=False,
                    is_deleted=True,
                    deleted_at=current_time
                )
                notify_dev(f"🗑️ [FALLBACK SOFT DELETE] PigImage: {page.title} (id={page.external_id})")
                
            elif isinstance(page, NewsCategoryPage) and page.external_id:
                sql_models.NewsCategory.objects.filter(id=page.external_id).update(
                    is_published=False,
                    is_deleted=True,
                    deleted_at=current_time
                )
                notify_dev(f"🗑️ [FALLBACK SOFT DELETE] NewsCategory: {page.title} (id={page.external_id})")
                
        except Exception as e:
            logger.error(f"Fallback soft delete failed for {page.title}: {e}")
            notify_dev(f"❌ [FALLBACK] Soft delete failed: {page.title} - {str(e)}")



from django.db import transaction, connection
from wagtail import hooks
from django.utils import timezone
from . import sql_models
from .pages import MedicineProductPage, PigPage

def _sync_medicine_images(external_id: int, page: MedicineProductPage):
    """Đồng bộ bảng nối product_medicine_image từ InlinePanel images."""
    # Xoá các liên kết cũ rồi chèn lại theo thứ tự
    with connection.cursor() as cur:
        cur.execute("DELETE FROM product_medicine_image WHERE medicine_id=%s", [external_id])
        # Insert theo thứ tự sort_index của Orderable
        sort = 0
        for item in page.images.all():
            if item.image_id:
                cur.execute(
                    "INSERT INTO product_medicine_image (medicine_id, image_id, sort) VALUES (%s, %s, %s)",
                    [external_id, item.image_id, sort],
                )
                sort += 1

def _sync_pig_images(external_id: int, page: PigPage):
    """Đồng bộ bảng nối product_pig_image từ InlinePanel images."""
    with connection.cursor() as cur:
        cur.execute("DELETE FROM product_pig_image WHERE pig_id=%s", [external_id])
        sort = 0
        for item in page.images.all():
            if item.image_id:
                cur.execute(
                    "INSERT INTO product_pig_image (pig_id, image_id, sort) VALUES (%s, %s, %s)",
                    [external_id, item.image_id, sort],
                )
                sort += 1

def upsert_medicine(page: MedicineProductPage):
    with transaction.atomic():
        if page.external_id:
            obj = sql_models.Medicine.objects.select_for_update().get(id=page.external_id)
        else:
            obj = sql_models.Medicine()
        obj.name = page.name
        obj.packaging = page.packaging or None
        obj.price_unit = page.price_unit
        obj.price_total = page.price_total
        obj.is_published = True
        obj.published_at = timezone.now()
        obj.save()
        if not page.external_id:
            page.external_id = obj.id
            page.save(update_fields=["external_id"])

        # Đồng bộ ảnh sang bảng nối
        _sync_medicine_images(page.external_id, page)

    notify_dev(f"[Wagtail] Medicine upserted → SQL: {page.title} (id={page.external_id})")

def upsert_pig(page: PigPage):
    with transaction.atomic():
        if page.external_id:
            obj = sql_models.Pig.objects.select_for_update().get(id=page.external_id)
        else:
            obj = sql_models.Pig()
        obj.name = page.name
        obj.price = page.price
        obj.is_published = True
        obj.published_at = timezone.now()
        obj.save()
        if not page.external_id:
            page.external_id = obj.id
            page.save(update_fields=["external_id"])

        # Đồng bộ ảnh sang bảng nối
        _sync_pig_images(page.external_id, page)

    notify_dev(f"[Wagtail] Pig upserted → SQL: {page.title} (id={page.external_id})")

@hooks.register("after_publish_page")
def on_publish(request, page):
    if isinstance(page, MedicineProductPage):
        upsert_medicine(page)
    elif isinstance(page, PigPage):
        upsert_pig(page)

@hooks.register("after_unpublish_page")
def on_unpublish(request, page):
    if isinstance(page, MedicineProductPage) and page.external_id:
        sql_models.Medicine.objects.filter(id=page.external_id).update(is_published=False)
        notify_dev(f"[Wagtail] Medicine unpublished: {page.title} (id={page.external_id})")
    if isinstance(page, PigPage) and page.external_id:
        sql_models.Pig.objects.filter(id=page.external_id).update(is_published=False)
        notify_dev(f"[Wagtail] Pig unpublished: {page.title} (id={page.external_id})")

@hooks.register("after_delete_page")
def on_delete(request, page):
    if isinstance(page, MedicineProductPage) and page.external_id:
        # Soft delete + clear gallery
        sql_models.Medicine.objects.filter(id=page.external_id).update(is_published=False, is_deleted=True)
        with connection.cursor() as cur:
            cur.execute("DELETE FROM product_medicine_image WHERE medicine_id=%s", [page.external_id])
        notify_dev(f"[Wagtail] Medicine deleted (soft): {page.title} (id={page.external_id})")
    if isinstance(page, PigPage) and page.external_id:
        sql_models.Pig.objects.filter(id=page.external_id).update(is_published=False, is_deleted=True)
        with connection.cursor() as cur:
            cur.execute("DELETE FROM product_pig_image WHERE pig_id=%s", [page.external_id])
        notify_dev(f"[Wagtail] Pig deleted (soft): {page.title} (id={page.external_id})")


# core/sync.py
from django.db import transaction, connection
from django.utils import timezone
from wagtail import hooks

from . import sql_models
from .pages import MedicineProductPage, PigPage
from .signals import notify_dev


# ---------- Helpers: sync image join tables ----------

def _sync_medicine_images(medicine_id: int, page: MedicineProductPage) -> None:    
    with connection.cursor() as cur:
        # Clear old relations
        cur.execute(
            "DELETE FROM product_medicine_image WHERE medicine_id=(%s)",
            [medicine_id]
        )

        # Re-insert by current order in UI
        sort = 0
        for item in page.images.order_by("sort_order").all():
            # item.image là Wagtail Image, dùng ID để tham chiếu lỏng
            if item.image_id:
                cur.execute(
                    "INSERT INTO product_medicine_image (medicine_id, image_id, sort) VALUES (%s, %s, %s)",
                    [medicine_id, item.image_id, sort],
                )
                sort += 1


def _sync_pig_images(pig_id: int, page: PigPage) -> None:

    with connection.cursor() as cur:
        cur.execute("DELETE FROM product_pig_image WHERE pig_id=%s", [pig_id])

        sort = 0
        for item in page.images.order_by("sort_order").all():
            if item.image_id:
                cur.execute(
                    "INSERT INTO product_pig_image (pig_id, image_id, sort) VALUES (%s, %s, %s)",
                    [pig_id, item.image_id, sort],
                )
                sort += 1


# ---------- Upsert main rows + image relations ----------

def upsert_medicine(page: MedicineProductPage) -> None:

    with transaction.atomic():
        if page.external_id:
            obj = sql_models.Medicine.objects.select_for_update().get(id=page.external_id)
        else:
            obj = sql_models.Medicine()

        # Map các field tối thiểu (mở rộng theo schema của bạn)
        obj.name = page.name
        obj.packaging = page.packaging or None
        obj.price_unit = page.price_unit
        obj.price_total = page.price_total
        obj.is_published = True
        # Nếu bạn có cột is_deleted trong model map:
        if hasattr(obj, "is_deleted"):
            obj.is_deleted = False
        obj.published_at = timezone.now()
        obj.save()

        # Gắn external_id nếu là insert lần đầu
        if not page.external_id:
            page.external_id = obj.id
            page.save(update_fields=["external_id"])

        # Sync gallery relations
        _sync_medicine_images(page.external_id, page)

    notify_dev(f"[Wagtail] Medicine upserted → SQL: {page.title} (id={page.external_id})")


def upsert_pig(page: PigPage) -> None:
    
    with transaction.atomic():
        if page.external_id:
            obj = sql_models.Pig.objects.select_for_update().get(id=page.external_id)
        else:
            obj = sql_models.Pig()

        obj.name = page.name
        obj.price = page.price
        obj.is_published = True
        if hasattr(obj, "is_deleted"):
            obj.is_deleted = False
        obj.published_at = timezone.now()
        obj.save()

        if not page.external_id:
            page.external_id = obj.id
            page.save(update_fields=["external_id"])

        _sync_pig_images(page.external_id, page)

    notify_dev(f"[Wagtail] Pig upserted → SQL: {page.title} (id={page.external_id})")


# ---------- Hooks ----------

@hooks.register("after_publish_page")
def on_publish(request, page, **kwargs):
    if isinstance(page, MedicineProductPage):
        upsert_medicine(page)
    elif isinstance(page, PigPage):
        upsert_pig(page)


@hooks.register("after_unpublish_page")
def on_unpublish(request, page, **kwargs):
    # Unpublish: chỉ ẩn trên web, KHÔNG xoá ảnh; giữ quan hệ ảnh (tuỳ bạn).
    if isinstance(page, MedicineProductPage) and page.external_id:
        sql_models.Medicine.objects.filter(id=page.external_id).update(is_published=False)
        notify_dev(f"[Wagtail] Medicine unpublished: {page.title} (id={page.external_id})")

    if isinstance(page, PigPage) and page.external_id:
        sql_models.Pig.objects.filter(id=page.external_id).update(is_published=False)
        notify_dev(f"[Wagtail] Pig unpublished: {page.title} (id={page.external_id})")


@hooks.register("after_delete_page")
def on_delete(request, page, **kwargs):
    if isinstance(page, MedicineProductPage) and page.external_id:
        # Soft delete main row
        update_fields = {"is_published": False}
        if "is_deleted" in [f.name for f in sql_models.Medicine._meta.get_fields()]:
            update_fields["is_deleted"] = True
        sql_models.Medicine.objects.filter(id=page.external_id).update(**update_fields)

        # Clear join relations (giữ file ảnh)
        with connection.cursor() as cur:
            cur.execute("DELETE FROM product_medicine_image WHERE medicine_id=%s", [page.external_id])

        notify_dev(f"[Wagtail] Medicine deleted (soft): {page.title} (id={page.external_id})")

    if isinstance(page, PigPage) and page.external_id:
        update_fields = {"is_published": False}
        if "is_deleted" in [f.name for f in sql_models.Pig._meta.get_fields()]:
            update_fields["is_deleted"] = True
        sql_models.Pig.objects.filter(id=page.external_id).update(**update_fields)

        with connection.cursor() as cur:
            cur.execute("DELETE FROM product_pig_image WHERE pig_id=%s", [page.external_id])

        notify_dev(f"[Wagtail] Pig deleted (soft): {page.title} (id={page.external_id})")