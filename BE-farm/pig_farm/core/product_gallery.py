
# core/product_gallery.py
from django.db import models
from wagtail.models import Orderable
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalKey
from .pages import MedicineProductPage, PigPage

class MedicineImageItem(Orderable):
    """Ảnh gắn với MedicineProductPage. Sẽ đồng bộ sang product_medicine_image."""
    page = ParentalKey(MedicineProductPage, related_name="images", on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    caption = models.CharField(max_length=200, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

class PigImageItem(Orderable):
    """Ảnh gắn với PigPage. Sẽ đồng bộ sang product_pig_image."""
    page = ParentalKey(PigPage, related_name="images", on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    caption = models.CharField(max_length=200, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]
