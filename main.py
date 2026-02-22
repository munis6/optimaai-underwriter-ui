from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print(">>> MAIN.PY LOADED <<<")

# ============================
# CORS MUST BE DECLARED BEFORE ROUTER IMPORT
# ============================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://optimaai-underwriter-ui.onrender.com"
]

# Create FastAPI app
app = FastAPI()

# Apply CORS middleware BEFORE importing routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import router AFTER CORS is applied
from app.routers.enrich_router import router

# Register routes
app.include_router(router)
