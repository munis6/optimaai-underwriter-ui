from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.enrich_router import router

print(">>> MAIN.PY LOADED <<<")

# ============================
# CORS MUST BE APPLIED BEFORE ROUTES
# ============================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://optimaai-underwriter-ui.onrender.com"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# ROUTES MUST BE INCLUDED AFTER CORS
# ============================
app.include_router(router)
