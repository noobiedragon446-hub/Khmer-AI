import os
import base64
import secrets
from io import BytesIO
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY", "")
API_TOKEN = os.getenv("API_TOKEN", "")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gpt-image-1.5")

app = FastAPI(title="My Private AI Backend", docs_url=None, redoc_url=None)

def authorize(authorization: Optional[str]):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Backend API key is not configured.")
    if not API_TOKEN:
        raise HTTPException(status_code=500, detail="Backend API token is not configured.")
    expected = f"Bearer {API_TOKEN}"
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Unauthorized.")

def client():
    return OpenAI(api_key=API_KEY)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate")
def generate(
    prompt: str = Form(...),
    size: str = Form("1024x1024"),
    authorization: Optional[str] = Header(default=None),
):
    authorize(authorization)
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required.")
    if size not in {"1024x1024", "1536x1024", "1024x1536"}:
        size = "1024x1024"
    try:
        result = client().images.generate(
            model=IMAGE_MODEL,
            prompt=prompt.strip(),
            size=size,
            n=1,
        )
        b64 = result.data[0].b64_json
        if not b64:
            raise HTTPException(status_code=502, detail="No image returned by provider.")
        return JSONResponse({"image_base64": b64, "mime_type": "image/png"})
    except HTTPException:
        raise
    except Exception as exc:
        # Avoid returning secrets or full provider details to the app.
        raise HTTPException(status_code=502, detail=f"Image generation failed: {type(exc).__name__}")

@app.post("/edit")
async def edit(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    authorization: Optional[str] = Header(default=None),
):
    authorize(authorization)
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required.")
    content_type = image.content_type or ""
    if content_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise HTTPException(status_code=400, detail="Upload PNG, JPEG, or WebP.")
    data = await image.read()
    if len(data) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image must be 15 MB or smaller.")
    try:
        result = client().images.edit(
            model=IMAGE_MODEL,
            image=(image.filename or "input.png", BytesIO(data), content_type),
            prompt=prompt.strip(),
            size="1024x1024",
        )
        b64 = result.data[0].b64_json
        if not b64:
            raise HTTPException(status_code=502, detail="No image returned by provider.")
        return JSONResponse({"image_base64": b64, "mime_type": "image/png"})
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Image editing failed: {type(exc).__name__}")
