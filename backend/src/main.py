from fastapi import FastAPI

from src.routes import departamentos, trabajadores

app = FastAPI(title="StaffSync HRMS", version="0.1.0")

app.include_router(departamentos.router)
app.include_router(trabajadores.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "staffsync-backend"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
