import logging
from typing import Callable, Dict, Optional, Tuple, Type

from django.core.exceptions import PermissionDenied
from django.db import DatabaseError, connection, transaction
from django.utils import timezone
from wagtail import hooks

from . import sql_models
from .pages import (
    MedicineProductPage,
    NewsCategoryPage,
    PigImagePage,
    PigPage,
)
from .signals import notify_dev


logger = logging.getLogger(__name__)


def _get_or_create_for_update(model, external_id: Optional[int]):
    """Return existing model instance or a new one inside a transaction."""

    if external_id:
        try:
            return model.objects.select_for_update().get(id=external_id), True
        except model.DoesNotExist:
            logger.warning(
                "%s with id=%s not found. Creating a fresh record.",
                model.__name__,
                external_id,
            )
            return model(), False
    return model(), False


def _sync_medicine_images(medicine_id: int, page: MedicineProductPage) -> None:
    """Synchronise the join table storing medicine-gallery relations."""

    with connection.cursor() as cur:
        cur.execute(
            "DELETE FROM product_medicine_image WHERE medicine_id=%s",
            [medicine_id],
        )

        sort = 0
        for item in page.images.order_by("sort_order").all():
            if getattr(item, "image_id", None):
                cur.execute(
                    "INSERT INTO product_medicine_image (medicine_id, image_id, sort) VALUES (%s, %s, %s)",
                    [medicine_id, item.image_id, sort],
                )
                sort += 1


def _sync_pig_images(pig_id: int, page: PigPage) -> None:
    """Synchronise the join table storing pig-gallery relations."""

    with connection.cursor() as cur:
        cur.execute("DELETE FROM product_pig_image WHERE pig_id=%s", [pig_id])

        sort = 0
        for item in page.images.order_by("sort_order").all():
            if getattr(item, "image_id", None):
                cur.execute(
                    "INSERT INTO product_pig_image (pig_id, image_id, sort) VALUES (%s, %s, %s)",
                    [pig_id, item.image_id, sort],
                )
                sort += 1


def _clear_join_table(table: str, column: str, external_id: int) -> None:
    """Utility used by soft-delete handlers to clear join tables."""

    with connection.cursor() as cur:
        cur.execute(
            f"DELETE FROM {table} WHERE {column}=%s",
            [external_id],
        )


def upsert_medicine(page: MedicineProductPage) -> None:
    """Sync a medicine page into the SQL mirror table."""

    try:
        with transaction.atomic():
            obj, found = _get_or_create_for_update(sql_models.Medicine, page.external_id)
            if not found:
                page.external_id = None

            obj.name = page.name
            obj.packaging = page.packaging or None
            obj.price_unit = page.price_unit
            obj.price_total = page.price_total
            obj.is_published = True
            obj.published_at = timezone.now()
            if hasattr(obj, "is_deleted"):
                obj.is_deleted = False
            if hasattr(obj, "deleted_at"):
                obj.deleted_at = None
            obj.save()

            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])

            _sync_medicine_images(obj.id, page)

        notify_dev(
            f"✅ [Wagtail] Medicine upserted → SQL: {page.title} (id={page.external_id})"
        )
    except DatabaseError as exc:
        logger.error("Medicine sync failed for %s: %s", page.title, exc)
        notify_dev(
            f"❌ [Wagtail] Medicine sync failed: {page.title} - {exc}"
        )


def upsert_pig(page: PigPage) -> None:
    """Sync a pig page into the SQL mirror table."""

    try:
        with transaction.atomic():
            obj, found = _get_or_create_for_update(sql_models.Pig, page.external_id)
            if not found:
                page.external_id = None

            obj.name = page.name
            obj.price = page.price
            obj.is_published = True
            obj.published_at = timezone.now()
            if hasattr(obj, "is_deleted"):
                obj.is_deleted = False
            if hasattr(obj, "deleted_at"):
                obj.deleted_at = None
            obj.save()

            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])

            _sync_pig_images(obj.id, page)

        notify_dev(
            f"✅ [Wagtail] Pig upserted → SQL: {page.title} (id={page.external_id})"
        )
    except DatabaseError as exc:
        logger.error("Pig sync failed for %s: %s", page.title, exc)
        notify_dev(
            f"❌ [Wagtail] Pig sync failed: {page.title} - {exc}"
        )


def upsert_pig_image(page: PigImagePage) -> None:
    """Sync a pig image page into the SQL mirror table."""

    try:
        with transaction.atomic():
            obj, found = _get_or_create_for_update(sql_models.PigImage, page.external_id)
            if not found:
                page.external_id = None

            obj.title = page.title
            obj.description = page.description or None
            obj.image_url = page.image.file.url if page.image else None
            obj.pig_id = (
                page.pig_reference.external_id
                if page.pig_reference and page.pig_reference.external_id
                else None
            )
            obj.image_type = page.image_type
            obj.file_size = page.file_size
            obj.width = page.width
            obj.height = page.height
            obj.is_published = True
            obj.published_at = timezone.now()
            if hasattr(obj, "is_deleted"):
                obj.is_deleted = False
            if hasattr(obj, "deleted_at"):
                obj.deleted_at = None
            obj.save()

            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])

        notify_dev(
            f"✅ [Wagtail] PigImage upserted → SQL: {page.title} (id={page.external_id})"
        )
    except DatabaseError as exc:
        logger.error("PigImage sync failed for %s: %s", page.title, exc)
        notify_dev(
            f"❌ [Wagtail] PigImage sync failed: {page.title} - {exc}"
        )
    except Exception as exc:
        logger.error("PigImage sync error for %s: %s", page.title, exc)
        notify_dev(
            f"❌ [Wagtail] PigImage sync error: {page.title} - {exc}"
        )


def upsert_news_category(page: NewsCategoryPage) -> None:
    """Sync a news category page into the SQL mirror table."""

    try:
        with transaction.atomic():
            obj, found = _get_or_create_for_update(
                sql_models.NewsCategory,
                page.external_id,
            )
            if not found:
                page.external_id = None

            obj.name = page.title
            obj.slug = page._slug_value()
            obj.description = page.description or None
            obj.color = page.color
            obj.icon = page.icon
            obj.parent_id = (
                page.parent_category.external_id
                if page.parent_category and page.parent_category.external_id
                else None
            )
            obj.sort_order = page.sort_order
            obj.is_published = True
            obj.published_at = timezone.now()
            if hasattr(obj, "is_deleted"):
                obj.is_deleted = False
            if hasattr(obj, "deleted_at"):
                obj.deleted_at = None
            obj.save()

            if not page.external_id:
                page.external_id = obj.id
                page.save(update_fields=["external_id"])

        notify_dev(
            f"✅ [Wagtail] NewsCategory upserted → SQL: {page.title} (id={page.external_id})"
        )
    except DatabaseError as exc:
        logger.error("NewsCategory sync failed for %s: %s", page.title, exc)
        notify_dev(
            f"❌ [Wagtail] NewsCategory sync failed: {page.title} - {exc}"
        )


PUBLISH_HANDLERS: Dict[Type, Callable] = {
    MedicineProductPage: upsert_medicine,
    PigPage: upsert_pig,
    PigImagePage: upsert_pig_image,
    NewsCategoryPage: upsert_news_category,
}


@hooks.register("after_publish_page")
def handle_after_publish(request, page, **kwargs):
    """Dispatch publish events to the correct sync helper exactly once."""

    for page_type, handler in PUBLISH_HANDLERS.items():
        if isinstance(page, page_type):
            handler(page)
            break


UNPUBLISH_MODELS: Dict[Type, Tuple] = {
    MedicineProductPage: (sql_models.Medicine, "Medicine"),
    PigPage: (sql_models.Pig, "Pig"),
    PigImagePage: (sql_models.PigImage, "PigImage"),
    NewsCategoryPage: (sql_models.NewsCategory, "NewsCategory"),
}


@hooks.register("after_unpublish_page")
def handle_after_unpublish(request, page, **kwargs):
    """Mark SQL records as unpublished when a Wagtail page is unpublished."""

    external_id = getattr(page, "external_id", None)
    if not external_id:
        return

    for page_type, (model, label) in UNPUBLISH_MODELS.items():
        if isinstance(page, page_type):
            try:
                model.objects.filter(id=external_id).update(is_published=False)
                notify_dev(
                    f"📤 [Wagtail] {label} unpublished: {page.title} (id={external_id})"
                )
            except DatabaseError as exc:
                logger.error("Unpublish failed for %s: %s", page.title, exc)
                notify_dev(
                    f"❌ [Wagtail] Unpublish failed: {page.title} - {exc}"
                )
            break


DELETE_HANDLERS: Dict[Type, Tuple] = {
    MedicineProductPage: (
        sql_models.Medicine,
        "Medicine",
        lambda external_id: _clear_join_table(
            "product_medicine_image",
            "medicine_id",
            external_id,
        ),
    ),
    PigPage: (
        sql_models.Pig,
        "Pig",
        lambda external_id: _clear_join_table(
            "product_pig_image",
            "pig_id",
            external_id,
        ),
    ),
    PigImagePage: (sql_models.PigImage, "PigImage", None),
    NewsCategoryPage: (sql_models.NewsCategory, "NewsCategory", None),
}


@hooks.register("after_delete_page")
def handle_after_delete(request, page, **kwargs):
    """Fallback soft-delete for supported pages if deletion slips through."""

    external_id = getattr(page, "external_id", None)
    if not external_id:
        return

    for page_type, (model, label, cleanup) in DELETE_HANDLERS.items():
        if isinstance(page, page_type):
            try:
                current_time = timezone.now()
                update_fields = {"is_published": False}
                model_fields = {field.name for field in model._meta.get_fields()}
                if "is_deleted" in model_fields:
                    update_fields["is_deleted"] = True
                if "deleted_at" in model_fields:
                    update_fields["deleted_at"] = current_time

                model.objects.filter(id=external_id).update(**update_fields)

                if cleanup:
                    cleanup(external_id)

                notify_dev(
                    f"🗑️ [Wagtail] {label} soft-deleted: {page.title} (id={external_id})"
                )
            except DatabaseError as exc:
                logger.error("Soft delete failed for %s: %s", page.title, exc)
                notify_dev(
                    f"❌ [Wagtail] Soft delete failed: {page.title} - {exc}"
                )
            except Exception as exc:  # pragma: no cover - defensive programming
                logger.error("Soft delete cleanup error for %s: %s", page.title, exc)
                notify_dev(
                    f"❌ [Wagtail] Soft delete cleanup failed: {page.title} - {exc}"
                )
            break


@hooks.register("before_delete_page")
def prevent_hard_delete_and_log(request, page):
    """Block hard deletes to enforce soft-delete policy."""

    logger.info(
        "🔍 DELETE ATTEMPT: %s '%s' by %s",
        page.__class__.__name__,
        page.title,
        getattr(request.user, "username", "<unknown>"),
    )
    username = getattr(request.user, "username", "<unknown>")
    notify_dev(
        f"🔍 [DEBUG] Delete attempt: {page.__class__.__name__} '{page.title}' by {username}"
    )

    if isinstance(page, (MedicineProductPage, PigPage, PigImagePage, NewsCategoryPage)):
        logger.info(
            "🚫 Blocking hard delete for %s by user %s (superuser: %s)",
            page.title,
            username,
            getattr(request.user, "is_superuser", False),
        )
        raise PermissionDenied(
            f"⛔ DELETE BLOCKED! Cannot delete '{page.title}'. "
            "Only developers can delete directly in the database. "
            "Please use 'Unpublish' instead."
        )
