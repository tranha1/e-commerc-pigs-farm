from datetime import datetime
from unittest.mock import MagicMock, patch

from django.test import TestCase

from pig_farm.core import sync
from pig_farm.core.pages import (
    MedicineProductPage,
    NewsCategoryPage,
    PigImagePage,
    PigPage,
)


class SyncHookTests(TestCase):
    def _make_page(self, page_cls, external_id=123):
        page = page_cls(title="Test", slug="test")

        if hasattr(page, "name") and not getattr(page, "name", None):
            page.name = "Name"
        if hasattr(page, "packaging") and not getattr(page, "packaging", None):
            page.packaging = "Box"
        if hasattr(page, "price_unit") and getattr(page, "price_unit", None) is None:
            page.price_unit = 10
        if hasattr(page, "price_total") and getattr(page, "price_total", None) is None:
            page.price_total = 20
        if hasattr(page, "price") and getattr(page, "price", None) is None:
            page.price = 30
        if hasattr(page, "description") and not getattr(page, "description", None):
            page.description = "Description"
        if hasattr(page, "sort_order") and getattr(page, "sort_order", None) is None:
            page.sort_order = 1

        page.external_id = external_id
        return page

    @patch("pig_farm.core.sync.notify_dev")
    def test_after_publish_calls_expected_upsert_once(self, notify_dev):
        cases = [
            (MedicineProductPage, "upsert_medicine"),
            (PigPage, "upsert_pig"),
            (PigImagePage, "upsert_pig_image"),
            (NewsCategoryPage, "upsert_news_category"),
        ]

        for page_cls, handler_name in cases:
            with self.subTest(page=page_cls.__name__):
                page = self._make_page(page_cls)
                handler_path = f"pig_farm.core.sync.{handler_name}"
                with patch(handler_path) as handler:
                    sync.handle_after_publish(None, page)
                    handler.assert_called_once_with(page)

        notify_dev.assert_not_called()

    @patch("pig_farm.core.sync.notify_dev")
    def test_after_unpublish_updates_once(self, notify_dev):
        cases = [
            (MedicineProductPage, "Medicine"),
            (PigPage, "Pig"),
            (PigImagePage, "PigImage"),
            (NewsCategoryPage, "NewsCategory"),
        ]

        for page_cls, model_name in cases:
            with self.subTest(page=page_cls.__name__):
                page = self._make_page(page_cls)
                objects_path = f"pig_farm.core.sync.sql_models.{model_name}.objects"
                with patch(objects_path) as manager:
                    update_mock = MagicMock()
                    manager.filter.return_value = update_mock

                    sync.handle_after_unpublish(None, page)

                    manager.filter.assert_called_once_with(id=page.external_id)
                    update_mock.update.assert_called_once_with(is_published=False)
                    notify_dev.assert_called_once()
                    notify_dev.reset_mock()

    @patch("pig_farm.core.sync.timezone.now")
    @patch("pig_farm.core.sync.notify_dev")
    def test_after_delete_soft_delete_once(self, notify_dev, timezone_now):
        fake_now = datetime(2024, 1, 1, 0, 0, 0)
        timezone_now.return_value = fake_now

        cases = [
            (MedicineProductPage, "Medicine", ("product_medicine_image", "medicine_id")),
            (PigPage, "Pig", ("product_pig_image", "pig_id")),
            (PigImagePage, "PigImage", None),
            (NewsCategoryPage, "NewsCategory", None),
        ]

        for page_cls, model_name, cleanup in cases:
            with self.subTest(page=page_cls.__name__):
                page = self._make_page(page_cls)
                objects_path = f"pig_farm.core.sync.sql_models.{model_name}.objects"
                with patch(objects_path) as manager, patch(
                    "pig_farm.core.sync._clear_join_table"
                ) as clear_join:
                    update_mock = MagicMock()
                    manager.filter.return_value = update_mock

                    sync.handle_after_delete(None, page)

                    manager.filter.assert_called_once_with(id=page.external_id)
                    update_mock.update.assert_called_once_with(
                        is_published=False,
                        is_deleted=True,
                        deleted_at=fake_now,
                    )

                    if cleanup:
                        table, column = cleanup
                        clear_join.assert_called_once_with(table, column, page.external_id)
                    else:
                        clear_join.assert_not_called()

                    clear_join.reset_mock()
                    notify_dev.assert_called_once()
                    notify_dev.reset_mock()
