from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

class Command(BaseCommand):
    help = "Hard delete product from SQL by ID (ONLY for Developers)."

    def add_arguments(self, parser):
        parser.add_argument("--type", choices=["medicine", "pig", "news"], required=True,
                            help="Loại bản ghi: medicine|pig|news")
        parser.add_argument("--id", type=int, required=True, help="ID bản ghi SQL")

    def handle(self, *args, **opts):
        rec_type = opts["type"]
        rec_id = opts["id"]

        table = None
        fk = None
        if rec_type == "medicine":
            table = "product_medicine"
            fk = "medicine_id"
        elif rec_type == "pig":
            table = "product_pig"
            fk = "pig_id"
        elif rec_type == "news":
            table = "cms_content_entry"
        else:
            raise CommandError("Unsupported type")

        with transaction.atomic(), connection.cursor() as cur:
            # Nếu là product thì xoá các quan hệ ảnh trước
            if rec_type in ("medicine", "pig"):
                join_table = f"product_{rec_type}_image"
                cur.execute(f"DELETE FROM {join_table} WHERE {fk}=%s", [rec_id])

            # Xoá cứng bản ghi chính
            cur.execute(f"DELETE FROM {table} WHERE id=%s", [rec_id])
            if cur.rowcount == 0:
                raise CommandError(f"Không tìm thấy {rec_type} id={rec_id}")

        self.stdout.write(self.style.SUCCESS(f"Hard deleted {rec_type} id={rec_id}"))