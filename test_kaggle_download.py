#!/usr/bin/env python3
"""
Test script to download a single model from Kaggle Hub
"""

import os
import kagglehub
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_download():
    """Test downloading a model from Kaggle Hub"""
    try:
        # Download latest version
        model_path = "phuchoangnguyen/model_paddle_layout_nhom_nhan/pyTorch/default"
        logger.info(f"Downloading model: {model_path}")
        
        downloaded_path = kagglehub.model_download(model_path)
        logger.info(f"Model downloaded to: {downloaded_path}")
        
        # List downloaded files
        if os.path.exists(downloaded_path):
            logger.info("Downloaded files:")
            for item in os.listdir(downloaded_path):
                item_path = os.path.join(downloaded_path, item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    logger.info(f"  📄 {item} ({size:,} bytes)")
                elif os.path.isdir(item_path):
                    logger.info(f"  📁 {item}/")
                    # List files in subdirectory
                    for subitem in os.listdir(item_path):
                        subitem_path = os.path.join(item_path, subitem)
                        if os.path.isfile(subitem_path):
                            size = os.path.getsize(subitem_path)
                            logger.info(f"    📄 {subitem} ({size:,} bytes)")
        
        logger.info("✅ Test completed successfully!")
        return downloaded_path
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    test_download()
