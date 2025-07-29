"""Layout detection service using PP-DocLayout_plus-L model."""

import os
import tempfile
import json
from typing import Any, Dict
from paddleocr import PPStructureV3
from ..config import LAYOUT_DETECTION_CONFIG, TEXT_DETECTION_CONFIG, TEXT_RECOGNITION_CONFIG


class LayoutDetectorSingleton:
    _instance = None
    _model = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize_model(self):
        """Initialize the PP-Structure model for layout detection"""
        if not self._is_initialized:
            try:
                self._model = PPStructureV3(
                    use_doc_orientation_classify=True,
                    use_doc_unwarping=False,
                    layout_detection_model_name=LAYOUT_DETECTION_CONFIG["model_name"],
                    layout_detection_model_dir=LAYOUT_DETECTION_CONFIG["model_dir"],
                    text_detection_model_name=TEXT_DETECTION_CONFIG["model_name"],
                    text_detection_model_dir=TEXT_DETECTION_CONFIG["model_dir"],
                    text_recognition_model_name=TEXT_RECOGNITION_CONFIG["model_name"],
                    text_recognition_model_dir=TEXT_RECOGNITION_CONFIG["model_dir"],
                    use_table_recognition=False,
                    use_seal_recognition=False,
                    use_chart_recognition=False,
                    use_formula_recognition=False,
                )
                self._is_initialized = True
                print("✅ Layout detection model initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing layout detection model: {str(e)}")
                raise e
    
    def get_model(self):
        """Get the initialized model instance"""
        if not self._is_initialized:
            raise RuntimeError("Model not initialized! Call initialize_model() first.")
        return self._model


# Global singleton instance
_detector = LayoutDetectorSingleton()

def initialize_layout_model():
    """Initialize the layout detection model"""
    _detector.initialize_model()

def _get_model():
    """Get the initialized model instance"""
    return _detector.get_model()

def detect_layout(
    image_path: str
) -> Dict[str, Any]:
    try:
        model = _get_model()
        print("Running layout detection prediction...")
        raw_output = model.predict(input=image_path)
        return str(raw_output)
        
    except Exception as e:
        error_msg = f"Error during layout detection: {str(e)}"
        return {
            "status": "error",
            "error_message": error_msg
        }

def detect_layout_from_bytes(
    image_bytes: bytes
) -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(image_bytes)
        tmp_img_path = tmp_file.name
    
    try:
        result = detect_layout(tmp_img_path)
        return result
    except Exception as e:
        raise e
    finally:
        if os.path.exists(tmp_img_path):
            os.remove(tmp_img_path)
