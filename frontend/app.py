from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI(title="Sparkling Gyan Frontend")
templates = Jinja2Templates(directory="templates")

BACKEND_URL = os.getenv("BACKEND_URL", "https://diwash-barla-spark-backend.hf.space")
HF_TOKEN = os.getenv("API_SECRET_TOKEN", "sparkling_secret_123")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/fast-search")
async def fast_search(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/fast-search",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
