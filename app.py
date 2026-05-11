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

@app.post("/api/deep-search")
async def deep_search(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/deep-search",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/extract")
async def extract(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/extract",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/synthesize")
async def synthesize(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/synthesize",
                json=payload,
                headers=headers,
                timeout=180.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/research/start")
async def research_start(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/research/start",
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

@app.get("/api/research/status/{task_id}")
async def research_status(task_id: str):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/api/research/status/{task_id}",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/api/history",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-script")
async def generate_script(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/generate-script",
                json=payload,
                headers=headers,
                timeout=120.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/dispatch-to-creator")
async def dispatch_to_creator(request: Request):
    payload = await request.json()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/dispatch-to-creator",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
