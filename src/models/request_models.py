from pydantic import BaseModel
from typing import List, Dict, Optional

class TextRequest(BaseModel): 
    text: str

class ImageBase64Request(BaseModel): 
    image_base64: str
