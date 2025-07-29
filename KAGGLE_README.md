# Hướng dẫn sử dụng Kaggle Hub để tải models

## Cài đặt

1. Cài đặt kagglehub:
```bash
pip install kagglehub
```

2. Thiết lập Kaggle credentials (tùy chọn):
```bash
# Đặt biến môi trường
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"

# Hoặc tạo file ~/.kaggle/kaggle.json
mkdir -p ~/.kaggle
echo '{"username":"your_username","key":"your_api_key"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

## Sử dụng

### 1. Test tải model đơn lẻ
```bash
python test_kaggle_download.py
```

### 2. Tải tất cả models
```bash
python scripts/download_models.py
```

### 3. Kiểm tra models đã tải
```bash
python scripts/download_models.py --verify-only
```

### 4. Buộc tải lại models
```bash
python scripts/download_models.py --force
```

## Cấu hình Models

Script hiện tại được cấu hình để tải 3 models:

1. **Layout Detection**: `phuchoangnguyen/model_paddle_layout_nhom_nhan/pyTorch/default`
2. **Text Detection**: `phuchoangnguyen/model_paddle_text_detection/pyTorch/default` 
3. **Text Recognition**: `phuchoangnguyen/model_paddle_text_recognition/pyTorch/default`

## Docker

Models sẽ được tải tự động trong quá trình build Docker:

```bash
docker build -t han-nom-api .
```

Để set Kaggle credentials trong Docker:
```bash
docker build --build-arg KAGGLE_USERNAME=your_username --build-arg KAGGLE_KEY=your_key -t han-nom-api .
```

## Cấu trúc thư mục sau khi tải

```
models/
├── layout_detection/
│   ├── inference.pdiparams
│   ├── inference.pdmodel
│   ├── inference.json
│   └── inference.yml
├── text_detection/
│   ├── inference.pdiparams
│   ├── inference.pdmodel
│   ├── inference.json
│   └── inference.yml
└── text_recognition/
    ├── inference.pdiparams
    ├── inference.pdmodel
    ├── inference.json
    └── inference.yml
```
