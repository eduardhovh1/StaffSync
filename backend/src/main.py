from fastapi import FastAPI

from src.routes import departments, employees

app = FastAPI(title="StaffSync HRMS", version="0.1.0")

app.include_router(departments.router)
app.include_router(employees.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "staffsync-backend"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
