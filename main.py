from fastapi import FastAPI
from app.api import api_router

from app.services.constants import _VERSION, _API_PREFIX

app = FastAPI(
    title="NDLTD TW Papers Graph",
    description="API for NDLTD TW Papers Graph",
    version=_VERSION,
)
app.include_router(api_router, prefix=_API_PREFIX)

@app.get("/")
def read_root():
    return "Hello World"

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8777)
