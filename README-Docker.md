# 🐷 Pig Farm Project - Docker Setup

Dự án full-stack với Django backend và React frontend, được containerized với Docker.

## 🚀 Khởi động nhanh

### Windows:
```cmd
.\run.bat up
```

### Linux/Mac:
```bash
chmod +x run.sh
./run.sh up
```

## 🌐 Địa chỉ truy cập

- **Frontend (React)**: http://localhost:8080
- **Backend (Django)**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Database**: localhost:5432
├── .env                       # Environment variables
├── run.sh                     # Linux/Mac script
└── run.bat                    # Windows script
```

## Yêu cầu hệ thống

- Docker Desktop
- Docker Compose
- 4GB RAM trở lên
- 10GB dung lượng ổ cứng

## Cách chạy dự án

### Trên Windows:
```bash
# Khởi động toàn bộ dự án
.\run.bat up

# Hoặc sử dụng docker-compose trực tiếp
docker-compose up -d
```

### Trên Linux/Mac:
```bash
# Cấp quyền thực thi
chmod +x run.sh

# Khởi động toàn bộ dự án
./run.sh up

# Hoặc sử dụng docker-compose trực tiếp
docker-compose up -d
```

## Các lệnh hữu ích

| Lệnh | Mô tả |
|------|-------|
| `run.bat up` | Khởi động toàn bộ services |
| `run.bat down` | Dừng toàn bộ services |
| `run.bat build` | Build lại images |
| `run.bat rebuild` | Build lại và khởi động |
| `run.bat logs` | Xem logs của tất cả services |
| `run.bat shell` | Mở shell trong backend container |
| `run.bat migrate` | Chạy Django migrations |
| `run.bat superuser` | Tạo Django superuser |
| `run.bat clean` | Dọn dẹp containers và volumes |

## Địa chỉ truy cập

- **Frontend (React)**: http://localhost:3000
- **Backend (Django)**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **API**: http://localhost:8000/api
- **Database**: localhost:5432

## Services được khởi chạy

1. **PostgreSQL Database** - Port 5432
2. **Django Backend** - Port 8000
3. **React Frontend** - Port 3000
4. **Redis Cache** - Port 6379

## Cấu hình environment

### Development (.env.development):
- DEBUG=True
- Database: PostgreSQL trong Docker
- CORS: Cho phép localhost:3000

### Production (.env.production):
- DEBUG=False  
- Database: PostgreSQL trong Docker
- CORS: Cấu hình cho domain thật

## Troubleshooting

### Lỗi port đã được sử dụng:
```bash
# Kiểm tra process sử dụng port
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :5432

# Kill process nếu cần
taskkill /PID <process_id> /F
```

### Lỗi database connection:
```bash
# Reset database
run.bat down
docker volume rm pig_farm_postgres_data
run.bat up
```

### Lỗi build frontend:
```bash
# Xóa node_modules và build lại
run.bat down
docker image rm pig_farm_frontend
run.bat build
```

### Xem logs chi tiết:
```bash
# Logs của tất cả services
run.bat logs

# Logs của service cụ thể
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## Cấu hình SSL cho Production

Để deploy production, cần:

1. Cập nhật `.env.production` với domain thật
2. Thêm SSL certificate
3. Cấu hình reverse proxy (nginx)
4. Sử dụng managed database service

## Backup & Restore

### Backup database:
```bash
docker-compose exec db pg_dump -U pig_farm_user pig_farm_db > backup.sql
```

### Restore database:
```bash
docker-compose exec -T db psql -U pig_farm_user pig_farm_db < backup.sql
```

## Development

### Thay đổi code:
- Backend: Code được mount vào container, tự động reload
- Frontend: Cần build lại image sau khi thay đổi

### Chạy migrations:
```bash
run.bat migrate
```

### Tạo superuser:
```bash
run.bat superuser
```

### Vào shell Django:
```bash
run.bat shell
python manage.py shell
```