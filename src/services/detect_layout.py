"""Layout detection service using PP-DocLayout_plus-L model."""

import os
import tempfile
import json
from typing import Optional, List, Any, Dict
from paddlex import create_model
from ..config import LAYOUT_DETECTION_CONFIG


class LayoutDetectorSingleton:
    _instance = None
    _model = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize_model(self):
        if not self._is_initialized:
            model_dir = LAYOUT_DETECTION_CONFIG["model_dir"]
            device = LAYOUT_DETECTION_CONFIG["device"]
            model_name = LAYOUT_DETECTION_CONFIG["model_name"]
            
            print(f"Loading layout detection model: {model_name}")
            
            self._model = create_model(
                model_name=model_name,
                model_dir=model_dir,
                device=device
            )
            self._is_initialized = True
    
    def get_model(self):
        if not self._is_initialized:
            raise RuntimeError("Model not initialized!")
        return self._model


# Global singleton instance
_detector = LayoutDetectorSingleton()

def initialize_layout_model():
    _detector.initialize_model()

def _get_model():
    return _detector.get_model()

def detect_layout(
    image_path: str,
    batch_size: int = 1,
    layout_nms: bool = True,
) -> Dict[str, Any]:
    model = _get_model()
    output = model.predict(image_path, batch_size=batch_size, layout_nms=layout_nms)
    
    # Convert output to JSON structure
    json_data = {}
    if output:
        with tempfile.NamedTemporaryFile(mode='w', suffix=".json", delete=False) as tmp_json:
            tmp_json_path = tmp_json.name
            
        try:
            for res in output:
                res.save_to_json(tmp_json_path)
                break  
                
            with open(tmp_json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                
        finally:
            if os.path.exists(tmp_json_path):
                os.remove(tmp_json_path)
    
    return json_data

def detect_layout_from_bytes(
    image_bytes: bytes,
    batch_size: int = 1,
    layout_nms: bool = True,
) -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(image_bytes)
        tmp_img_path = tmp_file.name
    
    try:
        return detect_layout(tmp_img_path, batch_size, layout_nms)
    finally:
        os.remove(tmp_img_path)
