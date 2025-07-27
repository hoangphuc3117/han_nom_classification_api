from fastapi import APIRouter, UploadFile, File
from src.models.request_models import TextRequest, ImageBase64Request
from src.services.classify_sino_nom import classify_sino_nom, ScriptType
from src.services.detect_layout import detect_layout_from_bytes
from src.config import NOM_THRESHOLD_TXT, NOM_THRESHOLD_IMG
import base64
import io
from PIL import Image
router = APIRouter()

@router.post("/classify-sino-nom")
async def classify_sino_nom(request: TextRequest):
    try:
        result = classify_sino_nom(request.text, NOM_THRESHOLD_TXT)
        return {"type": result.str_value, "type_id": result.int_value}
    except Exception as e:
        return {"error": "Cannot classify text"}

@router.post("/classify-sino-nom-img")
async def classify_sino_nom_image(file: UploadFile = File(...)):
    try:
        # Read image file from multipart
        image_data = await file.read()
        print("Image data:", image_data)
        image = Image.open(io.BytesIO(image_data))
        
        # OCR image to extract text
        text = ""
        result = classify_sino_nom(text, NOM_THRESHOLD_IMG)
        return {
            "type": result.str_value,
            "type_id": result.int_value,
        }
    except Exception as e:
        return {"error": "Cannot classify image"}
    
@router.post("/detect-layout")
async def detect_layout(file: UploadFile = File(...)):
    try:
        # Read image file from multipart
        image_data = await file.read()
    
        layout_result = detect_layout_from_bytes(image_data)
        
        return layout_result
    except Exception as e:
        return {"error": "Cannot detect layout"}