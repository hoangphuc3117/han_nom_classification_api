from fastapi import APIRouter, UploadFile, File
from src.services.detect_layout import detect_layout_from_bytes
router = APIRouter()
    
@router.post("/detect-layout")
async def detect_layout(file: UploadFile = File(...)):
    try:
        # Read image file from multipart
        image_data = await file.read()
    
        layout_result = detect_layout_from_bytes(image_data)
        
        return layout_result
    except Exception as e:
        return {"error": "Cannot detect layout"}