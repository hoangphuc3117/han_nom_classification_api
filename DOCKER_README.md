# Han Nom Classification API - Docker Setup

API phân loại Hán Nôm với khả năng phát hiện layout và nhận dạng văn bản.

## 🚀 Quick Start với Docker

### 1. Development Mode (Khuyến nghị cho testing)

```bash
# Build và chạy development container
./quick-docker.sh dev

# Hoặc sử dụng Makefile
make quick-dev
```

### 2. Production Mode

```bash
# Build và chạy production containers
./quick-docker.sh prod

# Hoặc sử dụng Makefile
make quick-prod
```

### 3. Sử dụng Docker Compose trực tiếp

```bash
# Development
docker-compose up -d

# Production với nginx
docker-compose --profile production up -d
```

## 📋 API Endpoints

### Health Check
```bash
GET /health
```

### Layout Detection
```bash
POST /detect-layout
Content-Type: multipart/form-data

# Upload file
curl -X POST "http://localhost:8000/detect-layout" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

### Sino-Nom Classification
```bash
POST /classify-sino-nom
Content-Type: application/json

{
    "text": "你的文本内容"
}
```

## 📊 JSON Response Format

### Layout Detection Response
```json
{
    "status": "success",
    "image_path": "uploaded_image",
    "layout_elements": [
        {
            "type": "text",
            "bbox": [x1, y1, x2, y2],
            "confidence": 0.95,
            "text": "Detected text content",
            "area": 10000.0,
            "center": [200.0, 225.0]
        }
    ],
    "text_content": "All detected text combined",
    "metadata": {
        "total_elements": 5,
        "element_counts": {
            "text": 3,
            "title": 1,
            "figure": 1
        },
        "confidence_stats": {
            "average": 0.92,
            "min": 0.85,
            "max": 0.98
        }
    }
}
```

## 🛠️ Available Commands

### Makefile Commands
```bash
make help        # Xem tất cả commands
make build       # Build production image
make build-dev   # Build development image
make run         # Chạy production containers
make dev         # Chạy development container
make stop        # Dừng containers
make clean       # Xóa containers và images
make logs        # Xem logs
make test        # Chạy tests
make shell       # Mở shell trong container
make health      # Kiểm tra health
```

### Quick Script Commands
```bash
./quick-docker.sh dev    # Development mode
./quick-docker.sh prod   # Production mode
```

## 🏗️ Architecture

```
han_nom_classification_api/
├── src/
│   ├── api/endpoints.py          # API routes
│   ├── services/
│   │   ├── detect_layout.py      # Layout detection service
│   │   └── classify_sino_nom.py  # Text classification
│   ├── models/request_models.py  # Pydantic models
│   └── config.py                 # Configuration
├── models/                       # Model files
├── Dockerfile                    # Production image
├── Dockerfile.dev               # Development image
├── docker-compose.yml           # Container orchestration
└── quick-docker.sh             # Quick setup script
```

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH=/app`
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`

### Model Configuration
Models được mount từ thư mục `./models` vào container tại `/app/models`

## 🐛 Troubleshooting

### Container không start
```bash
# Kiểm tra logs
docker-compose logs -f

# Kiểm tra container status
docker-compose ps
```

### Port conflict
```bash
# Thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Thay vì 8000:8000
```

### Model files missing
```bash
# Đảm bảo models folder tồn tại
ls -la models/

# Kiểm tra mount trong container
docker-compose exec han-nom-api ls -la /app/models/
```

## 📝 Testing

### Test Layout Detection JSON Format
```bash
# Chạy test script
python test_layout_json.py

# Hoặc trong container
make test
```

### Manual API Testing
```bash
# Health check
curl http://localhost:8000/health

# Upload image for layout detection
curl -X POST "http://localhost:8000/detect-layout" \
     -F "file=@test_image.jpg"
```

## 🌐 Access Points

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Nginx (Production)**: http://localhost:80

## 🔒 Security Features

- Non-root user trong container
- Multi-stage build để giảm image size
- Health checks tự động
- Security headers với nginx
- File size limits cho uploads

## 📈 Performance

- Multi-stage Docker build tối ưu size
- Model caching với singleton pattern
- Background process support
- Automatic restarts
- Resource monitoring với health checks
