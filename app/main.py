from fastapi import FastAPI
from app.api import auth
from app.routers import files
 

app = FastAPI(title="Distributed File Storage System")

app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "Distributed File Storage System is running"}

@app.get("/health")
def health():
    return {"status": "OK"}
