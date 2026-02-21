from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.enrich_router import router

print(">>> MAIN.PY LOADED <<<")

app = FastAPI()

# ============================
# CORS FIX (REQUIRED FOR FRONTEND)
# ============================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://optimaai-underwriter-ui.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # MUST be explicit, cannot be "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(router)
