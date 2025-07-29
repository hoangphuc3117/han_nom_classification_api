#!/bin/bash

# Script to build Docker image with Kaggle models

echo "🐳 Building Han Nom Classification API with Kaggle models..."

# Check if Kaggle credentials are provided
if [ -z "$KAGGLE_USERNAME" ] || [ -z "$KAGGLE_KEY" ]; then
    echo "⚠️ Warning: KAGGLE_USERNAME and KAGGLE_KEY not set"
    echo "Models will be downloaded without authentication (may work for public models)"
    echo ""
    echo "To set credentials:"
    echo "export KAGGLE_USERNAME=your_username"
    echo "export KAGGLE_KEY=your_api_key"
    echo ""
fi

# Build Docker image
docker build \
    --build-arg KAGGLE_USERNAME="$KAGGLE_USERNAME" \
    --build-arg KAGGLE_KEY="$KAGGLE_KEY" \
    -t han-nom-api:latest \
    .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the container:"
    echo "docker run -p 8000:8000 han-nom-api:latest"
else
    echo "❌ Docker build failed!"
    exit 1
fi
