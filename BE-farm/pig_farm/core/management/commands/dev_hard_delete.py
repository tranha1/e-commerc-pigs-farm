from django.core.management.base import BaseCommand
from django.utils import timezone
from core.pages import MedicineProductPage, PigPage, PigImagePage, NewsCategoryPage
from core import sql_models
import os


class Command(BaseCommand):
    """
    🚨 DEVELOPER ONLY COMMAND - Hard delete records
    
    CHẤP NHẬN RỦI RO: Command này xóa hoàn toàn dữ liệu không thể khôi phục
    Chỉ dành cho Developer khi thực sự cần xóa data
    """
    help = '🚨 DANGER: Hard delete records from both SQL and Wagtail (DEVELOPER ONLY)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['medicine', 'pig', 'pig_image', 'news_category'],
            required=True,
            help='Type of record to delete'
        )
        parser.add_argument(
            '--id',
            type=int,
            required=True,
            help='ID of the SQL record to delete'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Required confirmation flag'
        )
        parser.add_argument(
            '--i-understand-this-is-permanent',
            action='store_true',
            help='Additional safety confirmation'
        )

    def handle(self, *args, **options):
        record_type = options['type']
        record_id = options['id']
        
        # Safety checks
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR('❌ Missing --confirm flag. This operation is dangerous.')
            )
            return
            
        if not options['i_understand_this_is_permanent']:
            self.stdout.write(
                self.style.ERROR('❌ Missing --i-understand-this-is-permanent flag.')
            )
            return
        
        # Additional safety: check if running in production
        if os.environ.get('DJANGO_ENV') == 'production':
            self.stdout.write(
                self.style.ERROR('🚫 BLOCKED: Cannot run hard delete in production environment!')
            )
            return
        
        self.stdout.write("🚨" * 20)
        self.stdout.write(
            self.style.WARNING(
                f"⚠️  DANGER: About to PERMANENTLY DELETE {record_type} with ID {record_id}"
            )
        )
        self.stdout.write("🚨" * 20)
        
        # Confirm one more time
        confirm = input("\nType 'DELETE' to confirm (case-sensitive): ")
        if confirm != 'DELETE':
            self.stdout.write(self.style.SUCCESS("✅ Operation cancelled. No data was deleted."))
            return
        
        try:
            if record_type == 'medicine':
                self.delete_medicine(record_id)
            elif record_type == 'pig':
                self.delete_pig(record_id)
            elif record_type == 'pig_image':
                self.delete_pig_image(record_id)
            elif record_type == 'news_category':
                self.delete_news_category(record_id)
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error during deletion: {e}")
            )
            raise

    def delete_medicine(self, record_id):
        """Hard delete Medicine record and associated Wagtail page"""
        # Delete SQL record
        sql_record = sql_models.Medicine.objects.filter(id=record_id).first()
        if not sql_record:
            self.stdout.write(self.style.ERROR(f"❌ Medicine with ID {record_id} not found in SQL"))
            return
        
        medicine_name = sql_record.name
        sql_record.delete()
        self.stdout.write(f"🗑️ Deleted SQL Medicine: {medicine_name} (ID: {record_id})")
        
        # Delete associated Wagtail page (if exists)
        wagtail_page = MedicineProductPage.objects.filter(external_id=record_id).first()
        if wagtail_page:
            # Remove user context to bypass our protection
            if hasattr(wagtail_page, '_deleting_user'):
                delattr(wagtail_page, '_deleting_user')
            wagtail_page.delete()
            self.stdout.write(f"🗑️ Deleted Wagtail MedicineProductPage: {wagtail_page.title}")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Medicine {medicine_name} completely deleted"))

    def delete_pig(self, record_id):
        """Hard delete Pig record and associated Wagtail page"""
        sql_record = sql_models.Pig.objects.filter(id=record_id).first()
        if not sql_record:
            self.stdout.write(self.style.ERROR(f"❌ Pig with ID {record_id} not found in SQL"))
            return
        
        pig_name = sql_record.name
        sql_record.delete()
        self.stdout.write(f"🗑️ Deleted SQL Pig: {pig_name} (ID: {record_id})")
        
        wagtail_page = PigPage.objects.filter(external_id=record_id).first()
        if wagtail_page:
            if hasattr(wagtail_page, '_deleting_user'):
                delattr(wagtail_page, '_deleting_user')
            wagtail_page.delete()
            self.stdout.write(f"🗑️ Deleted Wagtail PigPage: {wagtail_page.title}")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Pig {pig_name} completely deleted"))

    def delete_pig_image(self, record_id):
        """Hard delete PigImage record and associated Wagtail page"""
        sql_record = sql_models.PigImage.objects.filter(id=record_id).first()
        if not sql_record:
            self.stdout.write(self.style.ERROR(f"❌ PigImage with ID {record_id} not found in SQL"))
            return
        
        image_title = sql_record.title
        sql_record.delete()
        self.stdout.write(f"🗑️ Deleted SQL PigImage: {image_title} (ID: {record_id})")
        
        wagtail_page = PigImagePage.objects.filter(external_id=record_id).first()
        if wagtail_page:
            if hasattr(wagtail_page, '_deleting_user'):
                delattr(wagtail_page, '_deleting_user')
            wagtail_page.delete()
            self.stdout.write(f"🗑️ Deleted Wagtail PigImagePage: {wagtail_page.title}")
        
        self.stdout.write(self.style.SUCCESS(f"✅ PigImage {image_title} completely deleted"))

    def delete_news_category(self, record_id):
        """Hard delete NewsCategory record and associated Wagtail page"""
        sql_record = sql_models.NewsCategory.objects.filter(id=record_id).first()
        if not sql_record:
            self.stdout.write(self.style.ERROR(f"❌ NewsCategory with ID {record_id} not found in SQL"))
            return
        
        category_name = sql_record.name
        sql_record.delete()
        self.stdout.write(f"🗑️ Deleted SQL NewsCategory: {category_name} (ID: {record_id})")
        
        wagtail_page = NewsCategoryPage.objects.filter(external_id=record_id).first()
        if wagtail_page:
            if hasattr(wagtail_page, '_deleting_user'):
                delattr(wagtail_page, '_deleting_user')
            wagtail_page.delete()
            self.stdout.write(f"🗑️ Deleted Wagtail NewsCategoryPage: {wagtail_page.title}")
        
        self.stdout.write(self.style.SUCCESS(f"✅ NewsCategory {category_name} completely deleted"))