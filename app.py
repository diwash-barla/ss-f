import os
import sys
from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx  # Async requests के लिए httpx ज्यादा स्टेबल है

app = FastAPI(title="Sparkling Gyan Frontend", docs_url=None, redoc_url=None)

# ==========================================
# 📂 DIRECTORY SETUP (Vercel Friendly)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# अगर तुम्हारे पास 'static' फोल्डर है, तो इसे अनकमेंट कर लेना
# app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ==========================================
# 🔐 SECRETS CONFIGURATION
# ==========================================
MY_API_KEY = os.getenv("SS_API_KEY", "my_custom_spark_key")
BACKEND_URL = os.getenv("BACKEND_URL", "https://diwash-barla-spark-search.hf.space").rstrip("/")
HF_TOKEN = os.getenv("API_SECRET_TOKEN", "sparkling_secret_123")

# Frontend Bearer token भेजता है, इसलिए HTTPBearer का यूज़ करना ज़रूरी है
security = HTTPBearer()

async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != MY_API_KEY:
        print(f"🔒 AUTH FAIL: Invalid API Key Try: '{credentials.credentials[:5]}...'", file=sys.stderr)
        raise HTTPException(status_code=403, detail="Invalid API Key. Access Denied!")
    return credentials.credentials

# ==========================================
# 🚀 VERCEL-SAFE PROXY HELPER (Ultimate Error Catcher)
# ==========================================
async def forward_to_backend(method: str, endpoint: str, payload: dict = None, params: dict = None):
    url = f"{BACKEND_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    
    try:
        # Timeout को 9.0s रखा है ताकि Vercel (10s limit) से पहले हमारा कोड ग्रेसफुली एरर दे सके
        async with httpx.AsyncClient(timeout=9.0, follow_redirects=True) as client:
            if method == "POST":
                response = await client.post(url, json=payload, headers=headers)
            else:
                response = await client.get(url, headers=headers, params=params)
                
            if response.status_code >= 400:
                error_text = response.text
                print(f"❌ BACKEND REJECTED ({response.status_code}) on {endpoint} | HF Response: {error_text}", file=sys.stderr)
                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Task not found or expired on backend.")
                raise HTTPException(status_code=response.status_code, detail=f"Backend Error: {error_text}")
            
            try:
                return response.json()
            except ValueError:
                print(f"⚠️ NON-JSON RESPONSE on {endpoint} | Status: {response.status_code}", file=sys.stderr)
                raise HTTPException(status_code=502, detail="Backend returned HTML. HF Space might be sleeping/paused.")

    except httpx.TimeoutException as e:
        # TimeoutException सभी तरह के टाइमआउट (Read, Connect, Write) को कैच कर लेगा
        print(f"⏱️ TIMEOUT ERROR on {endpoint} | ErrorType: {type(e).__name__}", file=sys.stderr)
        raise HTTPException(
            status_code=504, 
            detail="Hugging Face Space is taking too long to respond. It might be waking up from sleep. Please try again in 1-2 minutes."
        )
    except httpx.RequestError as e:
        # नेटवर्क से जुड़ी कोई भी दिक्कत (DNS, Connection Refused etc.)
        print(f"🔌 NETWORK ERROR on {endpoint} | ErrorType: {type(e).__name__} | Details: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=503, detail=f"Cannot connect to Hugging Face Backend: {type(e).__name__}")
    except Exception as e:
        # कोई भी अनजाना एरर
        print(f"💥 UNEXPECTED PROXY ERROR on {endpoint} | ErrorType: {type(e).__name__} | Details: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Unexpected Server Error: {str(e)}")

# ==========================================
# 🌐 UI & PWA ROUTES
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/docs-ui", response_class=HTMLResponse)
async def read_docs(request: Request):
    return templates.TemplateResponse(request=request, name="docs.html")

@app.get("/manifest.json")
async def serve_manifest():
    return FileResponse(os.path.join(BASE_DIR, "manifest.json"), media_type="application/manifest+json")

@app.get("/service-worker.js")
async def serve_sw():
    return FileResponse(os.path.join(BASE_DIR, "service-worker.js"), media_type="application/javascript")

# ==========================================
# ⚡ SPARKLING GYAN API ROUTES (Polling Ready)
# ==========================================

@app.post("/api/fast-search")
async def fast_search(request: Request, api_key: str = Depends(get_api_key)):
    payload = await request.json()
    return await forward_to_backend("POST", "/api/fast-search", payload=payload)

@app.post("/api/deep-search")
async def deep_search(request: Request, api_key: str = Depends(get_api_key)):
    payload = await request.json()
    return await forward_to_backend("POST", "/api/deep-search", payload=payload)

@app.post("/api/extract")
async def extract(request: Request, api_key: str = Depends(get_api_key)):
    payload = await request.json()
    return await forward_to_backend("POST", "/api/extract", payload=payload)

@app.post("/api/research/start")
async def research_start(request: Request, api_key: str = Depends(get_api_key)):
    payload = await request.json()
    return await forward_to_backend("POST", "/api/research/start", payload=payload)

@app.get("/api/research/status/{task_id}")
async def research_status(task_id: str, api_key: str = Depends(get_api_key)):
    return await forward_to_backend("GET", f"/api/research/status/{task_id}")

@app.get("/api/history")
async def get_history(q: str = None, api_key: str = Depends(get_api_key)):
    # Params सपोर्ट ताकि सर्च क्वेरी बैकएंड तक जा सके
    params = {"q": q} if q else {}
    try:
        return await forward_to_backend("GET", "/api/history", params=params)
    except:
        return [] # एरर आने पर UI क्रैश न हो, खाली एरे लौटाये

@app.post("/api/generate-script")
async def generate_script(request: Request, api_key: str = Depends(get_api_key)):
    # ⚠️ ध्यान दें: अगर स्क्रिप्ट जनरेशन में 10 सेकंड से ज्यादा लगता है, 
    # तो बैकएंड (HF) को भी /api/generate-script/start और status वाला पोलिंग लॉजिक इस्तेमाल करना होगा।
    payload = await request.json()
    return await forward_to_backend("POST", "/api/generate-script", payload=payload)

@app.post("/api/dispatch-to-creator")
async def dispatch_to_creator(request: Request, api_key: str = Depends(get_api_key)):
    payload = await request.json()
    return await forward_to_backend("POST", "/api/dispatch-to-creator", payload=payload)

@app.post("/api/synthesize")
async def synthesize(request: Request, api_key: str = Depends(get_api_key)):
    payload = await request.json()
    return await forward_to_backend("POST", "/api/synthesize", payload=payload)
