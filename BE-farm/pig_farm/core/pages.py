from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.text import slugify
from django.utils import timezone
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model
import re

Image = get_image_model()


class MedicineProductPage(Page):
    """Page mỏng để biên tập viên nhập thuốc; đồng bộ sang bảng SQL qua hooks."""
    external_id = models.BigIntegerField(null=True, editable=False)
    name = models.CharField(max_length=255)
    packaging = models.CharField(max_length=200, blank=True)
    price_unit = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    price_total = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("packaging"),
        FieldPanel("price_unit"),
        FieldPanel("price_total"),
    ]
    
    def delete(self, *args, **kwargs):
        """
        Override delete để chỉ cho phép superuser thực sự xóa.
        User thường chỉ có thể unpublish.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Kiểm tra user từ request nếu có
        user = getattr(self, '_deleting_user', None)
        if user:
            raise PermissionDenied("⛔ Không được phép xóa hoàn toàn. Chỉ Developer mới có thể xóa trực tiếp trong database. Hãy dùng 'Unpublish' để ẩn.")
        
        # Chỉ cho phép delete nếu không có user context (programmatic delete by developer)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"Medicine: {self.name}" if self.name else f"Medicine Page #{self.id}"

class PigPage(Page):
    """Page mỏng để biên tập viên nhập lợn; đồng bộ sang bảng SQL qua hooks."""
    external_id = models.BigIntegerField(null=True, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("price"),
    ]
    
    def delete(self, *args, **kwargs):
        """
        Override delete để chỉ cho phép superuser thực sự xóa.
        User thường chỉ có thể unpublish.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Kiểm tra user từ request nếu có
        user = getattr(self, '_deleting_user', None)
        if user:
            raise PermissionDenied("⛔ Không được phép xóa hoàn toàn. Chỉ Developer mới có thể xóa trực tiếp trong database. Hãy dùng 'Unpublish' để ẩn.")
        
        # Chỉ cho phép delete nếu không có user context (programmatic delete by developer)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"Pig: {self.name}" if self.name else f"Pig Page #{self.id}"


class PigImagePage(Page):
    """Page để quản lý hình ảnh lợn; đồng bộ sang bảng pig_images qua hooks."""
    external_id = models.BigIntegerField(null=True, blank=True, editable=False)
    
    # Thông tin cơ bản
    image = models.ForeignKey(
        Image, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="+",
        help_text="Chọn hình ảnh lợn"
    )
    description = models.TextField(
        blank=True, 
        help_text="Mô tả chi tiết về hình ảnh"
    )
    
    # Liên kết với lợn
    pig_reference = models.ForeignKey(
        'PigPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="images",
        help_text="Chọn lợn liên quan đến hình ảnh này"
    )
    
    # Phân loại hình ảnh
    IMAGE_TYPE_CHOICES = [
        ('main', 'Ảnh chính'),
        ('gallery', 'Ảnh thư viện'),
        ('thumbnail', 'Ảnh thu nhỏ'),
        ('profile', 'Ảnh hồ sơ'),
    ]
    image_type = models.CharField(
        max_length=50,
        choices=IMAGE_TYPE_CHOICES,
        default='gallery',
        help_text="Loại hình ảnh"
    )
    
    # Metadata tự động
    file_size = models.IntegerField(null=True, blank=True, editable=False)
    width = models.IntegerField(null=True, blank=True, editable=False)
    height = models.IntegerField(null=True, blank=True, editable=False)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("description"),
        ], heading="Thông tin hình ảnh"),
        
        MultiFieldPanel([
            FieldPanel("pig_reference"),
            FieldPanel("image_type"),
        ], heading="Phân loại"),
    ]

    def clean(self):
        super().clean()
        if not self.image:
            raise ValidationError({"image": "Vui lòng chọn một hình ảnh"})
        
        # Auto-generate title nếu chưa có
        if not self.title.strip():
            if self.pig_reference:
                self.title = f"Hình ảnh {self.pig_reference.name} - {self.get_image_type_display()}"
            else:
                self.title = f"Hình ảnh lợn - {self.get_image_type_display()}"

    def save(self, *args, **kwargs):
        # Auto-extract image metadata
        if self.image:
            self.file_size = getattr(self.image.file, 'size', None)
            self.width = self.image.width
            self.height = self.image.height
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete để chỉ cho phép superuser thực sự xóa.
        User thường chỉ có thể unpublish để soft delete.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Kiểm tra user từ request nếu có
        user = getattr(self, '_deleting_user', None)
        if user:
            raise PermissionDenied("⛔ Không được phép xóa hoàn toàn. Chỉ Developer mới có thể xóa trực tiếp trong database. Hãy dùng 'Unpublish' để ẩn.")
        
        # Chỉ cho phép delete nếu không có user context (programmatic delete by developer)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"PigImage: {self.title}" if self.title else f"PigImage Page #{self.id}"

    class Meta:
        verbose_name = "Hình ảnh lợn"
        verbose_name_plural = "Hình ảnh lợn"


class NewsCategoryPage(Page):
    """Page để quản lý danh mục tin tức; đồng bộ sang bảng news_categories qua hooks."""
    external_id = models.BigIntegerField(null=True, blank=True, editable=False)
    
    # Thông tin cơ bản
    description = models.TextField(
        blank=True, 
        help_text="Mô tả chi tiết về danh mục này"
    )
    
    # Tùy chỉnh giao diện
    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Mã màu hex (ví dụ: #FF0000 cho màu đỏ)",
        default="#0066CC"
    )
    
    ICON_CHOICES = [
        ('fa-newspaper', 'Báo chí'),
        ('fa-bullhorn', 'Thông báo'),
        ('fa-calendar', 'Sự kiện'),
        ('fa-star', 'Nổi bật'),
        ('fa-tag', 'Thẻ'),
        ('fa-folder', 'Thư mục'),
        ('fa-heart', 'Yêu thích'),
        ('fa-fire', 'Hot'),
    ]
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='fa-folder',
        help_text="Biểu tượng hiển thị cho danh mục"
    )
    
    # Phân cấp danh mục
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
        help_text="Danh mục cha (để trống nếu là danh mục gốc)"
    )
    
    # Thứ tự sắp xếp
    sort_order = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Số thứ tự (0-1000, số nhỏ hiển thị trước)"
    )
    
    # SEO
    slug_override = models.SlugField(
        max_length=255, 
        blank=True, 
        help_text="URL slug tùy chỉnh (để trống sẽ tự tạo từ tiêu đề)"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("description"),
        ], heading="Thông tin cơ bản"),
        
        MultiFieldPanel([
            FieldPanel("color"),
            FieldPanel("icon"),
        ], heading="Giao diện"),
        
        MultiFieldPanel([
            FieldPanel("parent_category"),
            FieldPanel("sort_order"),
        ], heading="Phân cấp"),
        
        MultiFieldPanel([
            FieldPanel("slug_override"),
        ], heading="SEO"),
    ]

    def clean(self):
        super().clean()
        
        # Validate color hex code
        if self.color and not re.match(r'^#[0-9A-Fa-f]{6}$', self.color):
            raise ValidationError({"color": "Mã màu phải có định dạng #RRGGBB (ví dụ: #FF0000)"})
        
        # Validate slug_override
        if self.slug_override and not re.match(r'^[a-z0-9\-]+$', self.slug_override):
            raise ValidationError({"slug_override": "Slug chỉ được chứa chữ thường, số và dấu gạch ngang"})
        
        # Prevent circular parent reference
        if self.parent_category:
            current = self.parent_category
            while current:
                if current == self:
                    raise ValidationError({"parent_category": "Không thể chọn chính mình hoặc danh mục con làm danh mục cha"})
                current = current.parent_category

    def _slug_value(self):
        """Generate clean, SEO-friendly slug"""
        slug_candidate = (
            self.slug_override or 
            self.slug or 
            slugify(self.title or "category", allow_unicode=False)
        ).strip()
        
        # Clean up and validate
        slug_candidate = re.sub(r'[^a-z0-9\-]', '', slug_candidate.lower())
        slug_candidate = re.sub(r'-+', '-', slug_candidate).strip('-')
        
        if not slug_candidate:
            slug_candidate = f"category-{self.id or 'new'}"
            
        return slug_candidate[:255]

    def get_children_count(self):
        """Đếm số danh mục con"""
        return self.subcategories.filter(live=True).count()

    def get_full_path(self):
        """Lấy đường dẫn đầy đủ của danh mục"""
        path = [self.title]
        current = self.parent_category
        while current:
            path.insert(0, current.title)
            current = current.parent_category
        return " > ".join(path)

    def delete(self, *args, **kwargs):
        """
        Override delete để chỉ cho phép superuser thực sự xóa.
        User thường chỉ có thể unpublish để soft delete.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Kiểm tra user từ request nếu có
        user = getattr(self, '_deleting_user', None)
        if user:
            raise PermissionDenied("⛔ Không được phép xóa hoàn toàn. Chỉ Developer mới có thể xóa trực tiếp trong database. Hãy dùng 'Unpublish' để ẩn.")
        
        # Chỉ cho phép delete nếu không có user context (programmatic delete by developer)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"NewsCategory: {self.get_full_path()}"

    class Meta:
        verbose_name = "Danh mục tin tức"
        verbose_name_plural = "Danh mục tin tức"