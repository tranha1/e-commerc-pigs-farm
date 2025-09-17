from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from django.utils.html import format_html
from . import sql_models


class NoDeletePermissionHelper(PermissionHelper):
    """Permission helper that disables all delete actions in the UI."""

    def user_can_delete_obj(self, user, obj=None):
        return False

    def user_can_delete(self, user):
        return False

    def user_can_bulk_delete(self, user):
        return False


class MedicineAdmin(ModelAdmin):
    model = sql_models.Medicine
    menu_label = "Thuốc (SQL)"
    menu_icon = "doc-full-inverse"
    list_display = ("id", "name", "formatted_prices", "status_badge", "updated_at")
    list_filter = ("is_published", "is_deleted", "updated_at")
    search_fields = ("name", "packaging")
    ordering = ("-updated_at",)
    permission_helper_class = NoDeletePermissionHelper
    
    def get_queryset(self, request):
        """Chỉ hiển thị các bản ghi chưa bị soft delete cho admin thường"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superuser có thể thấy tất cả
            return qs
        # Admin thường chỉ thấy bản ghi chưa delete
        return qs.filter(is_deleted=False)
    
    def has_delete_permission(self, request, obj=None):
        """⛔ CHẶN TẤT CẢ USERS (kể cả superuser) - chỉ dev có thể xóa trong database"""
        return False
    
    def formatted_prices(self, obj):
        unit_price = f"{obj.price_unit:,.0f} VNĐ" if obj.price_unit else "N/A"
        total_price = f"{obj.price_total:,.0f} VNĐ" if obj.price_total else "N/A"
        return format_html(
            "Đơn vị: <strong>{}</strong><br>Tổng: <strong>{}</strong>",
            unit_price, total_price
        )
    formatted_prices.short_description = "Giá"
    
    def status_badge(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: red; font-weight: bold;">🗑️ Đã xóa</span>')
        elif obj.is_published:
            return format_html('<span style="color: green; font-weight: bold;">✅ Đã xuất bản</span>')
        return format_html('<span style="color: orange; font-weight: bold;">❌ Chưa xuất bản</span>')
    status_badge.short_description = "Trạng thái"


class PigAdmin(ModelAdmin):
    model = sql_models.Pig
    menu_label = "Lợn (SQL)"
    menu_icon = "snippet"  # Changed icon for compatibility
    list_display = ("id", "name", "formatted_price", "status_badge", "updated_at")
    list_filter = ("is_published", "is_deleted", "updated_at")
    search_fields = ("name",)
    ordering = ("-updated_at",)
    permission_helper_class = NoDeletePermissionHelper
    
    def get_queryset(self, request):
        """Chỉ hiển thị các bản ghi chưa bị soft delete cho admin thường"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)
    
    def has_delete_permission(self, request, obj=None):
        """⛔ CHẶN TẤT CẢ USERS (kể cả superuser) - chỉ dev có thể xóa trong database"""
        return False
    
    def formatted_price(self, obj):
        if obj.price:
            price_str = f"{obj.price:,.0f} VNĐ"
            return format_html("<strong>{}</strong>", price_str)
        return "N/A"
    formatted_price.short_description = "Giá"
    
    def status_badge(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: red; font-weight: bold;">🗑️ Đã xóa</span>')
        elif obj.is_published:
            return format_html('<span style="color: green; font-weight: bold;">✅ Đã xuất bản</span>')
        return format_html('<span style="color: orange; font-weight: bold;">❌ Chưa xuất bản</span>')
    status_badge.short_description = "Trạng thái"


class PigImageAdmin(ModelAdmin):
    model = sql_models.PigImage
    menu_label = "Hình ảnh lợn (SQL)"
    menu_icon = "image"
    list_display = ("id", "title", "image_preview", "image_type_badge", "pig_info", "dimensions", "status_badge", "updated_at")
    list_filter = ("image_type", "is_published", "is_deleted", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-updated_at",)
    permission_helper_class = NoDeletePermissionHelper
    
    def get_queryset(self, request):
        """Chỉ hiển thị các bản ghi chưa bị soft delete cho admin thường"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)
    
    def has_delete_permission(self, request, obj=None):
        """⛔ CHẶN TẤT CẢ USERS (kể cả superuser) - chỉ dev có thể xóa trong database"""
        return False
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image_url
            )
        return "Không có ảnh"
    image_preview.short_description = "Xem trước"
    
    def image_type_badge(self, obj):
        type_colors = {
            'main': '#007cba',
            'gallery': '#28a745',
            'thumbnail': '#ffc107',
            'profile': '#6f42c1',
        }
        color = type_colors.get(obj.image_type, '#6c757d')
        type_labels = {
            'main': 'Chính',
            'gallery': 'Thư viện',
            'thumbnail': 'Thu nhỏ',
            'profile': 'Hồ sơ',
        }
        label = type_labels.get(obj.image_type, obj.image_type or 'N/A')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, label
        )
    image_type_badge.short_description = "Loại"
    
    def pig_info(self, obj):
        if obj.pig_id:
            try:
                pig = sql_models.Pig.objects.get(id=obj.pig_id)
                return format_html("<strong>{}</strong><br><small>ID: {}</small>", pig.name, pig.id)
            except sql_models.Pig.DoesNotExist:
                return format_html('<span style="color: red;">Lợn không tồn tại (ID: {})</span>', obj.pig_id)
        return "Không liên kết"
    pig_info.short_description = "Lợn liên quan"
    
    def dimensions(self, obj):
        if obj.width and obj.height:
            size_display = obj.get_file_size_display()
            return format_html(
                "{}×{}<br><small>{}</small>",
                obj.width, obj.height, size_display
            )
        return "N/A"
    dimensions.short_description = "Kích thước"
    
    def status_badge(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: red; font-weight: bold;">🗑️ Đã xóa</span>')
        elif obj.is_published:
            return format_html('<span style="color: green; font-weight: bold;">✅ Đã xuất bản</span>')
        return format_html('<span style="color: orange; font-weight: bold;">❌ Chưa xuất bản</span>')
    status_badge.short_description = "Trạng thái"


class NewsCategoryAdmin(ModelAdmin):
    model = sql_models.NewsCategory
    menu_label = "Danh mục tin tức (SQL)"
    menu_icon = "list-ul"
    list_display = ("id", "name_with_hierarchy", "category_badge", "parent_info", "sort_order", "status_badge", "updated_at")
    list_filter = ("is_published", "is_deleted", "parent_id", "updated_at")
    search_fields = ("name", "description", "slug")
    ordering = ("sort_order", "name")
    permission_helper_class = NoDeletePermissionHelper
    
    def get_queryset(self, request):
        """Chỉ hiển thị các bản ghi chưa bị soft delete cho admin thường"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)
    
    def has_delete_permission(self, request, obj=None):
        """⛔ CHẶN TẤT CẢ USERS (kể cả superuser) - chỉ dev có thể xóa trong database"""
        return False
    
    def name_with_hierarchy(self, obj):
        # Tạo hierarchical display
        level_indicator = ""
        if obj.parent_id:
            level_indicator = "└── "
        
        return format_html(
            "{}<strong>{}</strong><br><small>Slug: {}</small>",
            level_indicator, obj.name, obj.slug
        )
    name_with_hierarchy.short_description = "Tên danh mục"
    
    def category_badge(self, obj):
        color = obj.color or "#0066CC"
        icon_class = obj.icon or "fa-folder"
        name_display = obj.name[:20] + "..." if len(obj.name) > 20 else obj.name
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; display: inline-block;">'
            '<i class="fa {}"></i> {}</span>',
            color, icon_class, name_display
        )
    category_badge.short_description = "Hiển thị"
    
    def parent_info(self, obj):
        if obj.parent_id:
            try:
                parent = sql_models.NewsCategory.objects.get(id=obj.parent_id)
                return format_html("<strong>{}</strong><br><small>ID: {}</small>", parent.name, parent.id)
            except sql_models.NewsCategory.DoesNotExist:
                return format_html('<span style="color: red;">Danh mục cha không tồn tại (ID: {})</span>', obj.parent_id)
        return "Danh mục gốc"
    parent_info.short_description = "Danh mục cha"
    
    def status_badge(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: red; font-weight: bold;">🗑️ Đã xóa</span>')
        elif obj.is_published:
            return format_html('<span style="color: green; font-weight: bold;">✅ Đã xuất bản</span>')
        return format_html('<span style="color: orange; font-weight: bold;">❌ Chưa xuất bản</span>')
    status_badge.short_description = "Trạng thái"

modeladmin_register(MedicineAdmin)
modeladmin_register(PigAdmin)
modeladmin_register(PigImageAdmin)
modeladmin_register(NewsCategoryAdmin)
