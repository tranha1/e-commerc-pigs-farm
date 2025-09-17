from django.db import models
from .news_models import NewsIndexPage, NewsPage

# Create your models here.

# Import Wagtail page models to register them
__all__ = ['NewsIndexPage', 'NewsPage']
