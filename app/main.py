from fastapi import FastAPI
from .database import Base, _engine
from .routers import users, categories, transactions

app = FastAPI(title="Finance Tracker API", version="0.1.0")

Base.metadata.create_all(bind=_engine)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"ok": True, "service": "finance-tracker-api"}
