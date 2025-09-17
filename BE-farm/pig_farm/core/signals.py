
import logging
import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.signals import page_published, page_unpublished
from . import pages, sql_models
import logging

logger = logging.getLogger(__name__)

def notify_dev(message: str):
    """Gửi thông báo cho dev khi có thay đổi dữ liệu.
    - Ghi log
    - Gọi webhook (Slack/Discord/Teams) nếu DEV_WEBHOOK_URL được cấu hình.
    """
    logger.info(message)
    webhook_url = getattr(settings, "DEV_WEBHOOK_URL", None)
    if webhook_url:
        try:
            requests.post(webhook_url, json={"text": message}, timeout=5)
        except Exception as e:
            logger.warning(f"Webhook send failed: {e}")


@receiver(page_published)
def sync_page_to_sql_on_publish(sender, **kwargs):
    """Sync Wagtail Page to SQL when published"""
    instance = kwargs['instance']
    
    if isinstance(instance, pages.MedicineProductPage):
        sync_medicine_to_sql(instance)
    elif isinstance(instance, pages.PigPage):
        sync_pig_to_sql(instance)

@receiver(page_unpublished)
def sync_page_to_sql_on_unpublish(sender, **kwargs):
    """Mark SQL record as unpublished when page unpublished"""
    instance = kwargs['instance']
    
    if isinstance(instance, pages.MedicineProductPage):
        unpublish_medicine_in_sql(instance)
    elif isinstance(instance, pages.PigPage):
        unpublish_pig_in_sql(instance)

def sync_medicine_to_sql(medicine_page):
    """Sync MedicineProductPage to product_medicine table"""
    try:
        # Update or create SQL record
        medicine, created = sql_models.Medicine.objects.update_or_create(
            id=medicine_page.external_id,
            defaults={
                'name': medicine_page.name,
                'packaging': medicine_page.packaging,
                'price_unit': medicine_page.price_unit,
                'price_total': medicine_page.price_total,
                'is_published': True,
                'published_at': medicine_page.first_published_at,
            }
        )
        
        # Update page with SQL ID if new
        if created:
            medicine_page.external_id = medicine.id
            medicine_page.save_revision(update_fields=['external_id'])
            
        logger.info(f"✅ Synced Medicine Page '{medicine_page.name}' to SQL ID {medicine.id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to sync Medicine Page {medicine_page.id}: {str(e)}")

def sync_pig_to_sql(pig_page):
    """Sync PigPage to product_pig table"""
    try:
        pig, created = sql_models.Pig.objects.update_or_create(
            id=pig_page.external_id,
            defaults={
                'name': pig_page.name,
                'price': pig_page.price,
                'is_published': True,
                'published_at': pig_page.first_published_at,
            }
        )
        
        if created:
            pig_page.external_id = pig.id
            pig_page.save_revision(update_fields=['external_id'])
            
        logger.info(f"✅ Synced Pig Page '{pig_page.name}' to SQL ID {pig.id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to sync Pig Page {pig_page.id}: {str(e)}")

def unpublish_medicine_in_sql(medicine_page):
    """Mark medicine as unpublished in SQL"""
    if medicine_page.external_id:
        try:
            medicine = sql_models.Medicine.objects.get(id=medicine_page.external_id)
            medicine.is_published = False
            medicine.save(update_fields=['is_published', 'updated_at'])
            logger.info(f"📝 Unpublished Medicine SQL ID {medicine.id}")
        except sql_models.Medicine.DoesNotExist:
            logger.warning(f"⚠️ Medicine SQL ID {medicine_page.external_id} not found")

def unpublish_pig_in_sql(pig_page):
    """Mark pig as unpublished in SQL"""
    if pig_page.external_id:
        try:
            pig = sql_models.Pig.objects.get(id=pig_page.external_id)
            pig.is_published = False
            pig.save(update_fields=['is_published', 'updated_at'])
            logger.info(f"📝 Unpublished Pig SQL ID {pig.id}")
        except sql_models.Pig.DoesNotExist:
            logger.warning(f"⚠️ Pig SQL ID {pig_page.external_id} not found")