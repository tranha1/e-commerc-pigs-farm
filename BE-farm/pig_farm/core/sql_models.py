
from django.db import models


class CmsNewsEntry(models.Model):
    """Unmanaged model cho bảng cms_content_entry với kind='news' - bài viết tin tức từ Wagtail"""
    class Meta:
        db_table = "cms_content_entry"
        managed = False

    id = models.BigAutoField(primary_key=True)
    kind_id = models.SmallIntegerField()  # = 2 for 'news'
    slug = models.TextField()
    title = models.TextField()
    summary = models.TextField(null=True, blank=True)
    body_json = models.JSONField(null=True, blank=True)  # StreamField data from Wagtail
    body_html = models.TextField(null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)
    external_url = models.TextField(null=True, blank=True)
    cover_image_id = models.BigIntegerField(null=True, blank=True)
    author_name = models.TextField(null=True, blank=True)
    seo_title = models.TextField(null=True, blank=True)
    seo_desc = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title or f"CmsNewsEntry #{self.id}"

    def get_tags_list(self):
        """Extract tags from body_json if exists"""
        if self.body_json:
            # Look for tags in body_json structure
            tags = []
            if isinstance(self.body_json, list):
                for block in self.body_json:
                    if isinstance(block, dict) and block.get('type') == 'tags':
                        tags.extend(block.get('value', []))
            return tags
        return []

    def get_read_time(self):
        """Estimate read time based on content"""
        if self.body_html:
            # Rough estimate: 200 words per minute
            word_count = len(self.body_html.split())
            return max(1, word_count // 200)
        elif self.summary:
            word_count = len(self.summary.split())
            return max(1, word_count // 200)
        return 1

    def get_content_text(self):
        """Get plain text content for display"""
        if self.body_html:
            return self.body_html
        elif self.summary:
            return self.summary
        return ""

    def get_featured_image_url(self):
        """Get featured image URL if cover_image_id exists"""
        # This would need integration with Wagtail images
        # For now, return None
        return None

    @classmethod
    def get_news_queryset(cls):
        """Get queryset filtered for news articles only"""
        return cls.objects.filter(kind_id=2, is_deleted=False)  # kind_id=2 is 'news'


class Medicine(models.Model):
    class Meta:
        db_table = "product_medicine"
        managed = False

    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    packaging = models.TextField(null=True, blank=True)
    price_unit = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    price_total = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto update on save
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp when deleted
    
    def __str__(self):
        return self.name or f"Medicine #{self.id}"


class Pig(models.Model):
    class Meta:
        db_table = "product_pig"
        managed = False

    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto update on save
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp when deleted
    
    def __str__(self):
        return self.name or f"Pig #{self.id}"


class CmsContentEntry(models.Model):
    class Meta:
        db_table = "cms_content_entry"
        managed = False

    id = models.BigAutoField(primary_key=True)
    kind_id = models.SmallIntegerField()
    slug = models.TextField(null=True, blank=True)
    title = models.TextField()
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto update on save
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp when deleted
    
    def __str__(self):
        return self.title or f"Content #{self.id}"


class PigImage(models.Model):
    """Unmanaged model cho bảng pig_images - lưu hình ảnh lợn"""
    class Meta:
        db_table = "pig_images"
        managed = False

    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField()  # URL hoặc path đến file ảnh
    pig_id = models.BigIntegerField(null=True, blank=True)  # Liên kết với bảng product_pig
    image_type = models.CharField(max_length=50, null=True, blank=True)  # 'main', 'gallery', 'thumbnail'
    file_size = models.IntegerField(null=True, blank=True)  # Size file tính bằng bytes
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto update on save
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on create
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp when deleted
    
    def __str__(self):
        return self.title or f"PigImage #{self.id}"

    def get_file_size_display(self):
        """Hiển thị kích thước file theo MB"""
        if self.file_size:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        return "N/A"

    def get_dimensions_display(self):
        """Hiển thị kích thước ảnh"""
        if self.width and self.height:
            return f"{self.width}×{self.height}"
        return "N/A"


class NewsCategory(models.Model):
    """Unmanaged model cho bảng news_categories - phân loại bài viết"""
    class Meta:
        db_table = "news_categories"
        managed = False

    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    slug = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)  # Hex color code
    icon = models.CharField(max_length=50, null=True, blank=True)  # CSS icon class
    parent_id = models.BigIntegerField(null=True, blank=True)  # Self-referencing cho nested categories
    sort_order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto update on save
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on create
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp when deleted
    
    def __str__(self):
        return self.name or f"Category #{self.id}"

    def get_full_path(self):
        """Lấy đường dẫn đầy đủ của danh mục"""
        path = [self.name]
        # Note: Trong unmanaged model, không thể dùng related fields
        # Nên method này chỉ trả về tên hiện tại
        return " > ".join(path)

    def get_color_display(self):
        """Hiển thị màu với preview"""
        if self.color:
            return f"🎨 {self.color}"
        return "Mặc định"


class NewsArticle(models.Model):
    """Unmanaged model cho bảng news_articles - bài viết tin tức"""
    class Meta:
        db_table = "news_articles"
        managed = False

    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    slug = models.TextField(unique=True)
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    featured_image = models.TextField(null=True, blank=True)  # URL hoặc path đến ảnh chính
    category_id = models.BigIntegerField(null=True, blank=True)  # Liên kết với news_categories
    author = models.CharField(max_length=255, null=True, blank=True)
    read_time = models.IntegerField(null=True, blank=True)  # Thời gian đọc tính bằng phút
    view_count = models.IntegerField(default=0)
    tags = models.TextField(null=True, blank=True)  # JSON string chứa array tags
    meta_title = models.CharField(max_length=255, null=True, blank=True)  # SEO title
    meta_description = models.TextField(null=True, blank=True)  # SEO description
    is_featured = models.BooleanField(default=False)  # Bài viết nổi bật
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Auto update on save
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on create
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp when deleted
    
    def __str__(self):
        return self.title or f"Article #{self.id}"

    def get_read_time_display(self):
        """Hiển thị thời gian đọc"""
        if self.read_time:
            return f"{self.read_time} phút đọc"
        return "N/A"

    def get_tags_list(self):
        """Chuyển đổi tags từ JSON string thành list"""
        import json
        try:
            if self.tags:
                return json.loads(self.tags)
            return []
        except:
            return []

    def get_view_count_display(self):
        """Hiển thị số lượt xem"""
        if self.view_count >= 1000:
            return f"{self.view_count/1000:.1f}k lượt xem"
        return f"{self.view_count} lượt xem"
