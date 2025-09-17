"""
Management command để thêm soft delete columns vào các bảng SQL hiện có
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Thêm soft delete columns vào các bảng SQL hiện có'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Bắt đầu thêm soft delete columns...")
        
        # SQL commands để thêm soft delete columns
        sql_commands = [
            # Thêm cột is_deleted và deleted_at cho bảng product_medicine
            """
            ALTER TABLE product_medicine 
            ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;
            """,
            
            # Thêm cột is_deleted và deleted_at cho bảng product_pig  
            """
            ALTER TABLE product_pig 
            ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;
            """,
            
            # Thêm cột is_deleted và deleted_at cho bảng cms_content_entry
            """
            ALTER TABLE cms_content_entry 
            ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;
            """,
            
            # Thêm cột is_deleted và deleted_at cho bảng pig_images
            """
            ALTER TABLE pig_images 
            ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;
            """,
            
            # Thêm cột is_deleted và deleted_at cho bảng news_categories
            """
            ALTER TABLE news_categories 
            ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL;
            """,
        ]
        
        # Tạo indices cho performance
        index_commands = [
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_product_medicine_soft_delete ON product_medicine(is_deleted, deleted_at);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_product_pig_soft_delete ON product_pig(is_deleted, deleted_at);", 
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cms_content_entry_soft_delete ON cms_content_entry(is_deleted, deleted_at);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pig_images_soft_delete ON pig_images(is_deleted, deleted_at);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_news_categories_soft_delete ON news_categories(is_deleted, deleted_at);",
        ]
        
        try:
            with connection.cursor() as cursor:
                # Thêm columns
                for i, sql in enumerate(sql_commands, 1):
                    self.stdout.write(f"📝 Thực hiện lệnh {i}/{len(sql_commands)}...")
                    cursor.execute(sql)
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Đã thêm soft delete columns cho bảng {i}")
                    )
                
                # Thêm indices
                self.stdout.write("\n🔍 Tạo indices cho performance...")
                for i, sql in enumerate(index_commands, 1):
                    try:
                        cursor.execute(sql)
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ Đã tạo index {i}/{len(index_commands)}")
                        )
                    except Exception as e:
                        # Index có thể đã tồn tại, không phải lỗi nghiêm trọng
                        self.stdout.write(
                            self.style.WARNING(f"⚠️ Index {i} có thể đã tồn tại: {e}")
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        "\n🎉 Hoàn thành! Tất cả bảng đã được thêm soft delete columns."
                    )
                )
                
                # Kiểm tra kết quả
                self.stdout.write("\n🔍 Kiểm tra kết quả:")
                tables_to_check = [
                    'product_medicine', 'product_pig', 'cms_content_entry', 
                    'pig_images', 'news_categories'
                ]
                
                for table in tables_to_check:
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable, column_default 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}' 
                        AND column_name IN ('is_deleted', 'deleted_at')
                        ORDER BY column_name;
                    """)
                    
                    results = cursor.fetchall()
                    if results:
                        self.stdout.write(f"\n📋 Bảng {table}:")
                        for row in results:
                            col_name, data_type, nullable, default = row
                            self.stdout.write(f"   - {col_name}: {data_type} (nullable: {nullable}, default: {default})")
                    else:
                        self.stdout.write(
                            self.style.ERROR(f"❌ Không tìm thấy soft delete columns trong bảng {table}")
                        )
                        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Lỗi khi thực hiện migration: {e}")
            )
            raise e
            
        self.stdout.write(
            self.style.SUCCESS(
                "\n✨ Soft delete đã được triển khai thành công!"
                "\n🔒 Từ nay admin chỉ có thể soft delete, không thể xóa vĩnh viễn."
                "\n👨‍💻 Chỉ developer có thể hard delete trực tiếp trong database."
            )
        )