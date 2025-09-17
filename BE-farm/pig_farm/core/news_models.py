from django.db import models, transaction, connection
from django.utils import timezone
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks, hooks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.models import Image
import json

# ===== Khối nội dung tin tức (dễ nhập cho low-tech) =====
NEWS_BLOCKS = [
    ("paragraph", blocks.RichTextBlock(features=["bold","italic","ol","ul","link","h2","h3"])),
    ("image", ImageChooserBlock()),
    ("embed", EmbedBlock(help_text="Dán URL YouTube/Facebook...")),
    ("quote", blocks.BlockQuoteBlock()),
]

class NewsIndexPage(Page):
    """Mục Tin tức – nơi biên tập viên bấm 'Add child' để tạo bài."""
    max_count = 1
    subpage_types = ["core.NewsPage"]
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]
    
    intro = RichTextField(blank=True, help_text="Giới thiệu về trang tin tức")

    class Meta:
        verbose_name = "News Index Page"
        verbose_name_plural = "News Index Pages"


class NewsPage(Page):
    """Bài Tin tức. Publish -> upsert sang bảng SQL cms_content_entry(kind='news').
    Xoá trong Wagtail = soft delete (ẩn trên web, vẫn còn trong DB).
    """
    # Liên kết tới row SQL (cms_content_entry.id)
    external_id = models.BigIntegerField(null=True, blank=True, editable=False)

    # Nội dung hiển thị
    cover = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    summary = models.CharField(max_length=300, blank=True, help_text="Tóm tắt ngắn cho danh sách")
    date = models.DateField(default=timezone.now, help_text="Ngày phát hành")
    slug_override = models.SlugField(max_length=255, blank=True, help_text="Để trống sẽ tự tạo từ tiêu đề")
    body = StreamField(NEWS_BLOCKS, use_json_field=True, blank=True)

    # SEO optional - Use Wagtail's built-in fields
    # seo_title = models.CharField(max_length=255, blank=True)  # Use Page.seo_title instead
    # seo_desc = models.CharField(max_length=300, blank=True)   # Use Page.search_description instead
    
    # Author info
    author_name = models.CharField(max_length=255, blank=True, help_text="Tên tác giả")

    content_panels = Page.content_panels + [
        FieldPanel("cover"),
        FieldPanel("summary"),
        FieldPanel("author_name"),
        FieldPanel("date"),
        FieldPanel("slug_override"),
        FieldPanel("body"),
        MultiFieldPanel([
            FieldPanel("seo_title"), 
            FieldPanel("search_description")
        ], heading="SEO"),
    ]

    parent_page_types = ["core.NewsIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    # ===== Helpers =====
    def _get_kind_id_news(self, cursor):
        cursor.execute("SELECT id FROM lu_content_kind WHERE code='news' LIMIT 1;")
        row = cursor.fetchone()
        if not row:
            raise RuntimeError("Thiếu seed lu_content_kind ('news') – chạy 10_lookups.sql")
        return row[0]

    def _slug_value(self):
        return (self.slug_override or self.slug or (self.title or "")).strip()

    def _body_json(self):
        if not self.body:
            return []
        
        # Convert StreamValue to JSON-serializable format
        try:
            body_data = []
            for block in self.body:
                block_data = {
                    "type": block.block_type,
                    "value": None
                }
                
                # Handle different block types
                if block.block_type == 'paragraph':
                    block_data["value"] = str(block.value)
                elif block.block_type == 'quote':
                    block_data["value"] = str(block.value)
                elif block.block_type == 'image':
                    if block.value:
                        block_data["value"] = {
                            "title": getattr(block.value, 'title', ''),
                            "url": getattr(block.value, 'url', '') if hasattr(block.value, 'url') else ''
                        }
                else:
                    # For other types, convert to string
                    block_data["value"] = str(block.value)
                
                body_data.append(block_data)
            
            return body_data
            
        except Exception as e:
            print(f"Error converting body to JSON: {e}")
            return []

    def _cover_id(self):
        return self.cover_id if self.cover_id else None

    def _render_body_html(self):
        """Convert StreamField to HTML for storage"""
        if not self.body:
            return ""
        
        html_parts = []
        for block in self.body:
            if block.block_type == 'paragraph':
                html_parts.append(str(block.value))
            elif block.block_type == 'image' and block.value:
                # Simple image HTML
                html_parts.append(f'<img src="{block.value.file.url}" alt="{block.value.title}">')
            elif block.block_type == 'quote':
                html_parts.append(f'<blockquote>{block.value}</blockquote>')
            # Add more block type handling as needed
        
        return '\n'.join(html_parts)


# ===== Hooks: Publish/Unpublish/Delete -> đồng bộ SQL =====

@hooks.register("after_publish_page")
def news_after_publish(request, page):
    if not isinstance(page, NewsPage):
        return
    
    with transaction.atomic(), connection.cursor() as cur:
        kind_id = page._get_kind_id_news(cur)
        slug = page._slug_value()
        title = page.title or ""
        summary = page.summary or None
        body_json = json.dumps(page._body_json()) if page._body_json() else None
        body_html = page._render_body_html()
        cover_image_id = page._cover_id()
        published_at = timezone.now()
        seo_title = page.seo_title or None
        seo_desc = page.search_description or None
        author_name = page.author_name or None

        if page.external_id:
            # UPDATE existing entry
            cur.execute(
                """
                UPDATE cms_content_entry
                SET slug=%s, title=%s, summary=%s, body_json=%s, body_html=%s,
                    cover_image_id=%s, published_at=%s, is_published=TRUE, is_deleted=FALSE,
                    seo_title=%s, seo_desc=%s, author_name=%s, updated_at=NOW()
                WHERE id=%s
                """,
                [slug, title, summary, body_json, body_html,
                 cover_image_id, published_at, seo_title, seo_desc, author_name, page.external_id],
            )
        else:
            # INSERT new entry
            cur.execute(
                """
                INSERT INTO cms_content_entry
                    (kind_id, slug, title, summary, body_json, body_html, cover_image_id,
                     published_at, is_published, is_deleted, seo_title, seo_desc, author_name, created_at, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s, TRUE, FALSE, %s, %s, %s, NOW(), NOW())
                RETURNING id
                """,
                [kind_id, slug, title, summary, body_json, body_html, cover_image_id,
                 published_at, seo_title, seo_desc, author_name],
            )
            page.external_id = cur.fetchone()[0]
            page.save(update_fields=["external_id"])

        print(f"✅ Synced NewsPage '{title}' to cms_content_entry (ID: {page.external_id})")


@hooks.register("after_unpublish_page")
def news_after_unpublish(request, page):
    if not isinstance(page, NewsPage) or not page.external_id:
        return
    with connection.cursor() as cur:
        cur.execute("UPDATE cms_content_entry SET is_published=FALSE WHERE id=%s", [page.external_id])
        print(f"📴 Unpublished NewsPage '{page.title}' in cms_content_entry")


@hooks.register("after_delete_page")
def news_after_delete(request, page):
    if not isinstance(page, NewsPage) or not page.external_id:
        return
    with connection.cursor() as cur:
        # Soft delete: ẩn khỏi web, vẫn giữ DB
        cur.execute("UPDATE cms_content_entry SET is_published=FALSE, is_deleted=TRUE WHERE id=%s", [page.external_id])
        print(f"🗑️  Soft deleted NewsPage '{page.title}' in cms_content_entry")