#!/usr/bin/env python3
"""
Script to download PaddleOCR models for Han Nom Classification API using Kaggle Hub
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import kagglehub

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model configurations for Kaggle Hub
MODEL_CONFIGS = {
    "layout_detection": {
        "name": "PP-DocLayout-L",
        "kaggle_model": "phuchoangnguyen/model_paddle_layout_nhom_nhan/pyTorch/default",
        "extract_dir": "models/layout_detection",
        "required_files": ["inference.pdiparams", "inference.pdmodel"]
    },
    "text_detection": {
        "name": "PP-OCRv5_server_det", 
        "kaggle_model": "phuchoangnguyen/model_paddle_text_detection/pyTorch/default",
        "extract_dir": "models/text_detection",
        "required_files": ["inference.pdiparams", "inference.pdmodel"]
    },
    "text_recognition": {
        "name": "PP-OCRv5_server_rec",
        "kaggle_model": "phuchoangnguyen/model_paddle_text_recognition/pyTorch/default", 
        "extract_dir": "models/text_recognition",
        "required_files": ["inference.pdiparams", "inference.pdmodel"]
    }
}

def download_model_from_kaggle(kaggle_model: str, target_dir: str) -> bool:
    """Download model from Kaggle Hub"""
    try:
        logger.info(f"Downloading model from Kaggle: {kaggle_model}")
        
        # Download model from Kaggle Hub
        downloaded_path = kagglehub.model_download(kaggle_model)
        logger.info(f"Model downloaded to: {downloaded_path}")
        
        # Create target directory
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy files from downloaded path to target directory
        if os.path.exists(downloaded_path):
            # Copy all files from downloaded directory to target
            for item in os.listdir(downloaded_path):
                src_path = os.path.join(downloaded_path, item)
                dst_path = os.path.join(target_dir, item)
                
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dst_path)
                    logger.info(f"Copied: {item} to {target_dir}")
                elif os.path.isdir(src_path):
                    if os.path.exists(dst_path):
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                    logger.info(f"Copied directory: {item} to {target_dir}")
            
            return True
        else:
            logger.error(f"Downloaded path does not exist: {downloaded_path}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to download model {kaggle_model}: {e}")
        return False

def create_config_files(model_dir: str, model_name: str):
    """Create inference configuration files"""
    try:
        # Create inference.yml if not exists
        yml_path = os.path.join(model_dir, "inference.yml")
        if not os.path.exists(yml_path):
            yml_content = f"""
model_name: {model_name}
model_dir: {model_dir}
use_gpu: false
gpu_mem: 500
cpu_threads: 4
enable_mkldnn: true
"""
            with open(yml_path, 'w') as f:
                f.write(yml_content.strip())
            logger.info(f"Created config: {yml_path}")
        
        # Create inference.json if not exists
        json_path = os.path.join(model_dir, "inference.json")
        if not os.path.exists(json_path):
            json_content = f"""{{
    "model_name": "{model_name}",
    "model_dir": "{model_dir}",
    "use_gpu": false,
    "gpu_mem": 500,
    "cpu_threads": 4,
    "enable_mkldnn": true
}}"""
            with open(json_path, 'w') as f:
                f.write(json_content)
            logger.info(f"Created config: {json_path}")
            
    except Exception as e:
        logger.error(f"Failed to create config files: {e}")

def download_models():
    """Download all required models from Kaggle Hub"""
    logger.info("Starting model download process from Kaggle Hub...")
    
    # Create base models directory
    os.makedirs("models", exist_ok=True)
    
    success_count = 0
    total_models = len(MODEL_CONFIGS)
    
    for model_type, config in MODEL_CONFIGS.items():
        logger.info(f"\n=== Processing {model_type} ===")
        
        model_dir = config["extract_dir"]
        
        # Skip if model already exists
        if os.path.exists(model_dir) and os.listdir(model_dir):
            logger.info(f"Model {model_type} already exists, skipping...")
            success_count += 1
            continue
        
        # Download model from Kaggle Hub
        if download_model_from_kaggle(config["kaggle_model"], model_dir):
            # Create config files
            create_config_files(model_dir, config["name"])
            success_count += 1
            logger.info(f"✓ Successfully processed {model_type}")
        else:
            logger.error(f"✗ Failed to download {model_type}")
    
    # Summary
    logger.info(f"\n=== Download Summary ===")
    logger.info(f"Successfully downloaded: {success_count}/{total_models} models")
    
    if success_count == total_models:
        logger.info("🎉 All models downloaded successfully!")
        return True
    else:
        logger.error(f"⚠️ {total_models - success_count} models failed to download")
        return False

def verify_models():
    """Verify that all model files exist"""
    logger.info("\n=== Verifying Model Files ===")
    
    all_good = True
    for model_type, config in MODEL_CONFIGS.items():
        model_dir = config["extract_dir"]
        logger.info(f"\nChecking {model_type} in {model_dir}:")
        
        if not os.path.exists(model_dir):
            logger.error(f"  ✗ Directory not found: {model_dir}")
            all_good = False
            continue
        
        # Check for required files
        for required_file in config["required_files"]:
            file_path = os.path.join(model_dir, required_file)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                logger.info(f"  ✓ {required_file} ({file_size:,} bytes)")
            else:
                logger.error(f"  ✗ Missing: {required_file}")
                all_good = False
        
        # Check for any additional files
        if os.path.exists(model_dir):
            all_files = os.listdir(model_dir)
            additional_files = [f for f in all_files if f not in config["required_files"] and not f.startswith('.')]
            if additional_files:
                logger.info(f"  ℹ Additional files: {', '.join(additional_files)}")
    
    if all_good:
        logger.info("\n🎉 All model files verified successfully!")
    else:
        logger.error("\n⚠️ Some model files are missing!")
    
    return all_good

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download PaddleOCR models")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing models")
    parser.add_argument("--force", action="store_true", help="Force re-download even if models exist")
    
    args = parser.parse_args()
    
    if args.verify_only:
        verify_models()
    else:
        if args.force:
            # Remove existing models
            import shutil
            for config in MODEL_CONFIGS.values():
                if os.path.exists(config["extract_dir"]):
                    shutil.rmtree(config["extract_dir"])
                    logger.info(f"Removed existing model: {config['extract_dir']}")
        
        success = download_models()
        verify_models()
        
        if not success:
            exit(1)
