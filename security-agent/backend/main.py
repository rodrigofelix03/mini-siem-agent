from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.modules.infrastructure import get_infra_data
from backend.modules.network import get_network_data
from backend.modules.security import get_security_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/infrastructure")
def infra(date: str = None):
    return get_infra_data(date)

@app.get("/network")
def network(date: str = None):
    return get_network_data(date)

@app.get("/security")
def security(date: str = None):
    return get_security_data(date)