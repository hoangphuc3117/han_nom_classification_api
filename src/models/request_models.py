from pydantic import BaseModel

class TextRequest(BaseModel): text: str
class ImageBase64Request(BaseModel): image_base64: str