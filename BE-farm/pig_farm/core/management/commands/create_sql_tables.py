from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Tạo các bảng SQL cần thiết cho PigImage và NewsCategory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Xóa và tạo lại bảng nếu đã tồn tại',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Bắt đầu tạo các bảng SQL...')
        )

        try:
            with connection.cursor() as cursor:
                with transaction.atomic():
                    # Kiểm tra và tạo bảng pig_images
                    self.create_pig_images_table(cursor, force)
                    
                    # Kiểm tra và tạo bảng news_categories
                    self.create_news_categories_table(cursor, force)
                    
                    # Tạo indexes
                    self.create_indexes(cursor)
                    
                    # Tạo triggers
                    self.create_triggers(cursor)

            self.stdout.write(
                self.style.SUCCESS('✅ Tất cả bảng đã được tạo thành công!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Lỗi khi tạo bảng: {e}')
            )
            raise

    def table_exists(self, cursor, table_name):
        """Kiểm tra xem bảng có tồn tại không"""
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

    def create_pig_images_table(self, cursor, force):
        """Tạo bảng pig_images"""
        table_name = 'pig_images'
        
        if self.table_exists(cursor, table_name):
            if force:
                self.stdout.write(f'🗑️  Xóa bảng {table_name} hiện có...')
                cursor.execute(f'DROP TABLE IF EXISTS {table_name} CASCADE;')
            else:
                self.stdout.write(f'📋 Bảng {table_name} đã tồn tại, bỏ qua.')
                return

        self.stdout.write(f'🔨 Tạo bảng {table_name}...')
        
        cursor.execute("""
            CREATE TABLE pig_images (
                id BIGSERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                image_url TEXT NOT NULL,
                pig_id BIGINT,
                image_type VARCHAR(50) DEFAULT 'gallery',
                file_size INTEGER,
                width INTEGER,
                height INTEGER,
                is_published BOOLEAN DEFAULT FALSE,
                published_at TIMESTAMP WITH TIME ZONE,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Add foreign key constraint if product_pig table exists
        if self.table_exists(cursor, 'product_pig'):
            cursor.execute("""
                ALTER TABLE pig_images 
                ADD CONSTRAINT fk_pig_images_pig_id 
                FOREIGN KEY (pig_id) REFERENCES product_pig(id) 
                ON DELETE SET NULL;
            """)
            self.stdout.write('✅ Thêm foreign key constraint cho pig_id')

        self.stdout.write(f'✅ Bảng {table_name} đã được tạo')

    def create_news_categories_table(self, cursor, force):
        """Tạo bảng news_categories"""
        table_name = 'news_categories'
        
        if self.table_exists(cursor, table_name):
            if force:
                self.stdout.write(f'🗑️  Xóa bảng {table_name} hiện có...')
                cursor.execute(f'DROP TABLE IF EXISTS {table_name} CASCADE;')
            else:
                self.stdout.write(f'📋 Bảng {table_name} đã tồn tại, bỏ qua.')
                return

        self.stdout.write(f'🔨 Tạo bảng {table_name}...')
        
        cursor.execute("""
            CREATE TABLE news_categories (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                description TEXT,
                color VARCHAR(7) DEFAULT '#0066CC',
                icon VARCHAR(50) DEFAULT 'fa-folder',
                parent_id BIGINT,
                sort_order INTEGER DEFAULT 0,
                is_published BOOLEAN DEFAULT FALSE,
                published_at TIMESTAMP WITH TIME ZONE,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Add self-referencing foreign key
        cursor.execute("""
            ALTER TABLE news_categories 
            ADD CONSTRAINT fk_news_categories_parent_id 
            FOREIGN KEY (parent_id) REFERENCES news_categories(id) 
            ON DELETE SET NULL;
        """)

        self.stdout.write(f'✅ Bảng {table_name} đã được tạo')

    def create_indexes(self, cursor):
        """Tạo indexes để tăng performance"""
        self.stdout.write('🔍 Tạo indexes...')
        
        indexes = [
            # Pig Images indexes
            "CREATE INDEX IF NOT EXISTS idx_pig_images_pig_id ON pig_images(pig_id);",
            "CREATE INDEX IF NOT EXISTS idx_pig_images_type ON pig_images(image_type);",
            "CREATE INDEX IF NOT EXISTS idx_pig_images_published ON pig_images(is_published);",
            "CREATE INDEX IF NOT EXISTS idx_pig_images_created_at ON pig_images(created_at);",
            
            # News Categories indexes
            "CREATE INDEX IF NOT EXISTS idx_news_categories_parent ON news_categories(parent_id);",
            "CREATE INDEX IF NOT EXISTS idx_news_categories_slug ON news_categories(slug);",
            "CREATE INDEX IF NOT EXISTS idx_news_categories_published ON news_categories(is_published);",
            "CREATE INDEX IF NOT EXISTS idx_news_categories_sort ON news_categories(sort_order);",
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        self.stdout.write('✅ Indexes đã được tạo')

    def create_triggers(self, cursor):
        """Tạo triggers để auto-update updated_at"""
        self.stdout.write('⚡ Tạo triggers...')
        
        # Tạo function update timestamp
        cursor.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        
        # Tạo triggers cho các bảng
        triggers = [
            "DROP TRIGGER IF EXISTS update_pig_images_updated_at ON pig_images;",
            """CREATE TRIGGER update_pig_images_updated_at 
               BEFORE UPDATE ON pig_images
               FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();""",
            
            "DROP TRIGGER IF EXISTS update_news_categories_updated_at ON news_categories;",
            """CREATE TRIGGER update_news_categories_updated_at 
               BEFORE UPDATE ON news_categories
               FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();""",
        ]
        
        for trigger_sql in triggers:
            cursor.execute(trigger_sql)
        
        self.stdout.write('✅ Triggers đã được tạo')