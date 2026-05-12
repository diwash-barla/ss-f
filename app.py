from fastapi import FastAPI, Request, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import httpx
import os
import sys

app = FastAPI(title="Sparkling Gyan Frontend")
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

# ==========================================
# 🔐 SECRETS CONFIGURATION
# ==========================================
BACKEND_URL = os.getenv("BACKEND_URL", "https://diwash-barla-spark-search.hf.space")
HF_TOKEN = os.getenv("API_SECRET_TOKEN", "sparkling_secret_123")
FRONTEND_CUSTOM_API_KEY = os.getenv("SS_API_KEY", "my_custom_spark_key")

# ==========================================
# 🚨 SMART EXCEPTION LOGGER
# यह हर एरर को तुम्हारे टर्मिनल में डिटेल के साथ प्रिंट करेगा
# ==========================================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    print(f"🔴 HTTP ERROR {exc.status_code} | Path: {request.url.path} | Reason: {exc.detail}", file=sys.stderr)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# ==========================================
# 🛡️ SECURITY LAYER
# ==========================================
def verify_frontend_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != FRONTEND_CUSTOM_API_KEY:
        print(f"🔒 AUTH FAIL: Kisi ne galat API key try ki: '{credentials.credentials[:5]}...'", file=sys.stderr)
        raise HTTPException(status_code=403, detail="Invalid SS_API_KEY. Access Denied.")
    return credentials.credentials

# ==========================================
# 🚀 ELITE PROXY HELPER
# सारे राउट्स का हैवी काम यह अकेला फंक्शन करेगा और बैकएंड एरर्स को भी प्रिंट करेगा
# ==========================================
async def forward_to_backend(method: str, endpoint: str, payload: dict = None, timeout: float = 60.0):
    url = f"{BACKEND_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        async with httpx.AsyncClient() as client:
            if method == "POST":
                response = await client.post(url, json=payload, headers=headers, timeout=timeout)
            else:
                response = await client.get(url, headers=headers, timeout=timeout)
                
            # अगर बैकएंड (HF Space) से कोई एरर आता है
            if response.status_code >= 400:
                error_body = response.text
                print(f"❌ BACKEND REJECTED ({response.status_code}) on {endpoint} | HF Response: {error_body}", file=sys.stderr)
                raise HTTPException(status_code=response.status_code, detail=f"Backend Error: {error_body}")
                
            return response.json()
            
    except httpx.RequestError as e:
        print(f"💥 CONNECTION CRASH on {endpoint} | Error: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Backend is unreachable: {str(e)}")

# ==========================================
# 🌐 UI & PWA ROUTES
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

@app.get("/docs-ui")
async def read_docs(request: Request):
    return templates.TemplateResponse(request=request, name="docs.html")

# ==========================================
# ⚡ PROXY API ROUTES
# ==========================================
@app.post("/api/fast-search", dependencies=[Depends(verify_frontend_api_key)])
async def fast_search(request: Request):
    return await forward_to_backend("POST", "/api/fast-search", await request.json(), timeout=30.0)

@app.post("/api/deep-search", dependencies=[Depends(verify_frontend_api_key)])
async def deep_search(request: Request):
    return await forward_to_backend("POST", "/api/deep-search", await request.json(), timeout=60.0)

@app.post("/api/extract", dependencies=[Depends(verify_frontend_api_key)])
async def extract(request: Request):
    return await forward_to_backend("POST", "/api/extract", await request.json(), timeout=60.0)

@app.post("/api/synthesize", dependencies=[Depends(verify_frontend_api_key)])
async def synthesize(request: Request):
    return await forward_to_backend("POST", "/api/synthesize", await request.json(), timeout=180.0)

@app.post("/api/research/start", dependencies=[Depends(verify_frontend_api_key)])
async def research_start(request: Request):
    return await forward_to_backend("POST", "/api/research/start", await request.json(), timeout=30.0)

@app.get("/api/research/status/{task_id}", dependencies=[Depends(verify_frontend_api_key)])
async def research_status(task_id: str):
    return await forward_to_backend("GET", f"/api/research/status/{task_id}", timeout=30.0)

@app.get("/api/history", dependencies=[Depends(verify_frontend_api_key)])
async def get_history():
    return await forward_to_backend("GET", "/api/history", timeout=30.0)

@app.post("/api/generate-script", dependencies=[Depends(verify_frontend_api_key)])
async def generate_script(request: Request):
    return await forward_to_backend("POST", "/api/generate-script", await request.json(), timeout=120.0)

@app.post("/api/dispatch-to-creator", dependencies=[Depends(verify_frontend_api_key)])
async def dispatch_to_creator(request: Request):
    return await forward_to_backend("POST", "/api/dispatch-to-creator", await request.json(), timeout=60.0)
