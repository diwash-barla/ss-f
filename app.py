from fastapi import FastAPI, Request, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import httpx
import os

app = FastAPI(title="Sparkling Gyan Frontend")
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

# ==========================================
# 🔐 SECRETS CONFIGURATION
# ==========================================
# 1. Backend URL (Private HF Space)
BACKEND_URL = os.getenv("BACKEND_URL", "https://diwash-barla-spark-search.hf.space")

# 2. HF Token: Used by THIS frontend to securely talk to the backend. 
# DO NOT share this. It stays hidden in the environment.
HF_TOKEN = os.getenv("API_SECRET_TOKEN", "sparkling_secret_123")

# 3. Custom Frontend API Key: Used by users in the UI to access THIS frontend.
# You can share this with friends.
FRONTEND_CUSTOM_API_KEY = os.getenv("SS_API_KEY", "my_custom_spark_key")

# ==========================================
# 🛡️ SECURITY LAYER FOR FRONTEND
# ==========================================
def verify_frontend_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verifies the custom API key sent from the browser/UI."""
    if credentials.credentials != FRONTEND_CUSTOM_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid SS_API_KEY")
    return credentials.credentials

# Helper function to get the headers needed for the Backend
def get_backend_headers():
    """Returns the authorization header using the secret HF Token."""
    return {"Authorization": f"Bearer {HF_TOKEN}"}


# ==========================================
# 🌐 UI & PWA ROUTES (No API Key Required here)
# ==========================================
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("manifest.json")

@app.get("/service-worker.js")
async def get_sw():
    return FileResponse("service-worker.js")


# ==========================================
# 🚀 API PROXY ROUTES (Secured by verify_frontend_api_key)
# ==========================================
@app.post("/api/fast-search", dependencies=[Depends(verify_frontend_api_key)])
async def fast_search(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/fast-search",
                json=payload,
                headers=get_backend_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/deep-search", dependencies=[Depends(verify_frontend_api_key)])
async def deep_search(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/deep-search",
                json=payload,
                headers=get_backend_headers(),
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/extract", dependencies=[Depends(verify_frontend_api_key)])
async def extract(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/extract",
                json=payload,
                headers=get_backend_headers(),
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/synthesize", dependencies=[Depends(verify_frontend_api_key)])
async def synthesize(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/synthesize",
                json=payload,
                headers=get_backend_headers(),
                timeout=180.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/research/start", dependencies=[Depends(verify_frontend_api_key)])
async def research_start(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/research/start",
                json=payload,
                headers=get_backend_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/api/research/status/{task_id}", dependencies=[Depends(verify_frontend_api_key)])
async def research_status(task_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/api/research/status/{task_id}",
                headers=get_backend_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/api/history", dependencies=[Depends(verify_frontend_api_key)])
async def get_history():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/api/history",
                headers=get_backend_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-script", dependencies=[Depends(verify_frontend_api_key)])
async def generate_script(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/generate-script",
                json=payload,
                headers=get_backend_headers(),
                timeout=120.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/dispatch-to-creator", dependencies=[Depends(verify_frontend_api_key)])
async def dispatch_to_creator(request: Request):
    payload = await request.json()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/dispatch-to-creator",
                json=payload,
                headers=get_backend_headers(),
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
