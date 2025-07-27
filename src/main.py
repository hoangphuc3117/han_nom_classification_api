from fastapi import FastAPI
from src.api.endpoints import router
from src.services.detect_layout import initialize_layout_model

app = FastAPI(title="Han Nom Classification API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    print("🚀 Starting server...")
    try:
        initialize_layout_model()
    except Exception as e:
        print(f"Error initializing models: {str(e)}")
        raise e

app.include_router(router)